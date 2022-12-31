import logging
from urllib.parse import urljoin

from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from telebot.types import Update  # noqa

from .handlers import bot

logger = logging.getLogger(__name__)


def set_tg_bot_webhook(request: HttpRequest):
    bot.set_webhook(
        url=urljoin(f"https://{settings.BASE_DOMAIN}", reverse("tg_bot_webhook")),
        secret_token=settings.TELEGRAM_BOT_SECRET_TOKEN,
    )
    return HttpResponse(b"OK", status=200)


@csrf_exempt
def tg_bot_webhook(request: HttpRequest):
    if (
        request.method != "POST"
        and request.content_type != "application/json"
        and request.headers.get("X-Telegram-Bot-Api-Secret-Token") != settings.TELEGRAM_BOT_SECRET_TOKEN
    ):
        return HttpResponseForbidden()
    try:
        bot.process_new_updates([Update.de_json(request.body.decode())])
    except Exception as err:
        logger.error(str(err), exc_info=True)
    return HttpResponse(b"OK", status=200)
