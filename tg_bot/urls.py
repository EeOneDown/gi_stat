from django.urls import path

from . import views

urlpatterns = [
    path("enable", views.set_tg_bot_webhook, name="set_webhook"),
    path("webhook", views.tg_bot_webhook, name="tg_bot_webhook"),
]
