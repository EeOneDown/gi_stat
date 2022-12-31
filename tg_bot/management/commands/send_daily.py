from itertools import groupby

from django.core.management.base import BaseCommand
from django.utils import timezone
from telebot.apihelper import ApiException  # noqa

from tg_bot.handlers import bot
from tg_bot.messages import BotMessages
from tg_bot.models import UserCharacter, Days


class Command(BaseCommand):
    def handle(self, *args, **options):
        days = Days.get_by_weekday(timezone.now().weekday())
        all_user_characters = (
            UserCharacter.objects.filter(user__is_subscribed=True, character__talent_days__in=days)
            .select_related("user", "character__talent_domain__region")
            # order by region for in-code 'group by'
            .order_by("user_id", "character__talent_domain__region_id")
            .all()
        )
        for user, user_characters in groupby(all_user_characters, lambda user_character: user_character.user):
            try:
                text = BotMessages.create_today_message(user_characters)
                bot.send_message(user.chat_id, text, disable_notification=True)
            except ApiException as err:
                if err.result.status_code == 403:
                    user.delete()
                self.stderr(str(err))
                continue
            except Exception as err:  # noqa
                self.stderr(str(err))
                continue
