import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import Message


class HangoutConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = "hangout_main"

    async def connect(self):
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        recent_messages = await self.get_recent_messages()
        for message in recent_messages:
            await self.send(text_data=json.dumps({
                "type": "message",
                "nickname": message["nickname"],
                "content": message["content"],
                "timestamp": message["timestamp"]
            }))

        await self.send(text_data=json.dumps({
            "type": "system",
            "message": "Connected to hangout"
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data): 
        try:
            data = json.loads(text_data)
            message_type = data.get("type", "message")

            if message_type == "message":
                nickname = data.get("nickname", "anonymous")
                content = data.get("content", "")

                if not content.strip():
                    return

                ip_address = self.scope.get("client", ["", ""])[0]

                message = await self.save_message(
                    nickname, content, ip_address
                )

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "message_handler",
                        "nickname": nickname,
                        "content": content,
                        "timestamp": message["timestamp"]
                    }
                )
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": "an error occured"
            }))
        except Exception as error:
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": "an error occured"
            }))

    async def message_handler(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'nickname': event['nickname'],
            'content': event['content'],
            'timestamp': event['timestamp'],
        }))

    @database_sync_to_async
    def save_message(self, nickname, content, ip_address):
        message = Message.objects.create(
            nickname=nickname,
            content=content,
            ip_address=ip_address
        )
        return message.to_dict()

    @database_sync_to_async
    def get_recent_messages(self, limit=50):
        messages = Message.objects.order_by("-timestamp")[:limit]
        return [message.to_dict() for message in reversed(messages)]