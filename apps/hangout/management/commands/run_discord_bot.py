import asyncio
from django.core.management.base import BaseCommand
from apps.hangout.discord_bot import HangoutDiscord


class Command(BaseCommand):
    help = 'run the discord bot for real-time chat'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("starting discord bot..."))
        
        async def run_bot():
            bot = HangoutDiscord()
            try:
                await bot.start()
            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING("\nshutting down Discord bot..."))
            finally:
                await bot.stop()
        
        try:
            asyncio.run(run_bot())
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\nbot stopped"))
        except Exception as error:
            self.stdout.write(self.style.ERROR(f"error running bot: {error}"))
            raise