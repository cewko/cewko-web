from django.urls import path
from . import views

app_name = "hangout"

urlpatterns = [
    path("", views.hangout_view, name="hangout"),
]