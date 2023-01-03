from datetime import datetime
from functools import partial
from unittest.mock import patch, Mock

from django.test import TestCase, override_settings
from django.urls import reverse

from tg_bot.models import User, Region, WeeklyBoss, Domain, Character, Days


class TelegramBotTestCase(TestCase):
    def setUp(self) -> None:
        self.client.post = partial(
            self.client.post, content_type="application/json", HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN="test-token"
        )
        self.from_user = {
            "id": 1234567890,
            "is_bot": False,
            "first_name": "Test",
            "last_name": "User",
            "username": "test-username",
            "language_code": "en",
            "is_premium": True,
        }
        self.chat = {
            "id": self.from_user["id"],
            "first_name": "Test",
            "last_name": "User",
            "username": "test-username",
            "type": "private",
        }

    @staticmethod
    def populate_test_data():
        r1 = Region.objects.create(name="r1")
        r2 = Region.objects.create(name="r2")
        r3 = Region.objects.create(name="r3")
        r4 = Region.objects.create(name="r4")

        wb1 = WeeklyBoss.objects.create(name="wb1", region=r1)
        wb2 = WeeklyBoss.objects.create(name="wb2", region=r2)
        wb3 = WeeklyBoss.objects.create(name="wb3", region=r3)
        wb4 = WeeklyBoss.objects.create(name="wb4", region=r4)

        d1 = Domain.objects.create(name="d1", region=r1)
        d2 = Domain.objects.create(name="d2", region=r2)
        d3 = Domain.objects.create(name="d3", region=r3)
        d4 = Domain.objects.create(name="d4", region=r4)

        Character.objects.create(name="c_mt_d1_wb1", talent_days=Days.MON_THU, talent_domain=d1, weekly_boss=wb1)
        Character.objects.create(name="c_mt_d1_wb2", talent_days=Days.MON_THU, talent_domain=d1, weekly_boss=wb2)
        Character.objects.create(name="c_mt_d1_wb3", talent_days=Days.MON_THU, talent_domain=d1, weekly_boss=wb3)
        Character.objects.create(name="c_mt_d1_wb4", talent_days=Days.MON_THU, talent_domain=d1, weekly_boss=wb4)
        Character.objects.create(name="c_mt_d2_wb1", talent_days=Days.MON_THU, talent_domain=d2, weekly_boss=wb1)
        Character.objects.create(name="c_mt_d2_wb2", talent_days=Days.MON_THU, talent_domain=d2, weekly_boss=wb2)
        Character.objects.create(name="c_mt_d2_wb3", talent_days=Days.MON_THU, talent_domain=d2, weekly_boss=wb3)
        Character.objects.create(name="c_mt_d2_wb4", talent_days=Days.MON_THU, talent_domain=d2, weekly_boss=wb4)
        Character.objects.create(name="c_mt_d3_wb1", talent_days=Days.MON_THU, talent_domain=d3, weekly_boss=wb1)
        Character.objects.create(name="c_mt_d3_wb2", talent_days=Days.MON_THU, talent_domain=d3, weekly_boss=wb2)
        Character.objects.create(name="c_mt_d3_wb3", talent_days=Days.MON_THU, talent_domain=d3, weekly_boss=wb3)
        Character.objects.create(name="c_mt_d3_wb4", talent_days=Days.MON_THU, talent_domain=d3, weekly_boss=wb4)
        Character.objects.create(name="c_mt_d4_wb1", talent_days=Days.MON_THU, talent_domain=d4, weekly_boss=wb1)
        Character.objects.create(name="c_mt_d4_wb2", talent_days=Days.MON_THU, talent_domain=d4, weekly_boss=wb2)
        Character.objects.create(name="c_mt_d4_wb3", talent_days=Days.MON_THU, talent_domain=d4, weekly_boss=wb3)
        Character.objects.create(name="c_mt_d4_wb4", talent_days=Days.MON_THU, talent_domain=d4, weekly_boss=wb4)

        Character.objects.create(name="c_tf_d1_wb1", talent_days=Days.TUE_FRI, talent_domain=d1, weekly_boss=wb1)
        Character.objects.create(name="c_tf_d1_wb2", talent_days=Days.TUE_FRI, talent_domain=d1, weekly_boss=wb2)
        Character.objects.create(name="c_tf_d1_wb3", talent_days=Days.TUE_FRI, talent_domain=d1, weekly_boss=wb3)
        Character.objects.create(name="c_tf_d1_wb4", talent_days=Days.TUE_FRI, talent_domain=d1, weekly_boss=wb4)
        Character.objects.create(name="c_tf_d2_wb1", talent_days=Days.TUE_FRI, talent_domain=d2, weekly_boss=wb1)
        Character.objects.create(name="c_tf_d2_wb2", talent_days=Days.TUE_FRI, talent_domain=d2, weekly_boss=wb2)
        Character.objects.create(name="c_tf_d2_wb3", talent_days=Days.TUE_FRI, talent_domain=d2, weekly_boss=wb3)
        Character.objects.create(name="c_tf_d2_wb4", talent_days=Days.TUE_FRI, talent_domain=d2, weekly_boss=wb4)
        Character.objects.create(name="c_tf_d3_wb1", talent_days=Days.TUE_FRI, talent_domain=d3, weekly_boss=wb1)
        Character.objects.create(name="c_tf_d3_wb2", talent_days=Days.TUE_FRI, talent_domain=d3, weekly_boss=wb2)
        Character.objects.create(name="c_tf_d3_wb3", talent_days=Days.TUE_FRI, talent_domain=d3, weekly_boss=wb3)
        Character.objects.create(name="c_tf_d3_wb4", talent_days=Days.TUE_FRI, talent_domain=d3, weekly_boss=wb4)
        Character.objects.create(name="c_tf_d4_wb1", talent_days=Days.TUE_FRI, talent_domain=d4, weekly_boss=wb1)
        Character.objects.create(name="c_tf_d4_wb2", talent_days=Days.TUE_FRI, talent_domain=d4, weekly_boss=wb2)
        Character.objects.create(name="c_tf_d4_wb3", talent_days=Days.TUE_FRI, talent_domain=d4, weekly_boss=wb3)
        Character.objects.create(name="c_tf_d4_wb4", talent_days=Days.TUE_FRI, talent_domain=d4, weekly_boss=wb4)

        Character.objects.create(name="c_ws_d1_wb1", talent_days=Days.WED_SAT, talent_domain=d1, weekly_boss=wb1)
        Character.objects.create(name="c_ws_d1_wb2", talent_days=Days.WED_SAT, talent_domain=d1, weekly_boss=wb2)
        Character.objects.create(name="c_ws_d1_wb3", talent_days=Days.WED_SAT, talent_domain=d1, weekly_boss=wb3)
        Character.objects.create(name="c_ws_d1_wb4", talent_days=Days.WED_SAT, talent_domain=d1, weekly_boss=wb4)
        Character.objects.create(name="c_ws_d2_wb1", talent_days=Days.WED_SAT, talent_domain=d2, weekly_boss=wb1)
        Character.objects.create(name="c_ws_d2_wb2", talent_days=Days.WED_SAT, talent_domain=d2, weekly_boss=wb2)
        Character.objects.create(name="c_ws_d2_wb3", talent_days=Days.WED_SAT, talent_domain=d2, weekly_boss=wb3)
        Character.objects.create(name="c_ws_d2_wb4", talent_days=Days.WED_SAT, talent_domain=d2, weekly_boss=wb4)
        Character.objects.create(name="c_ws_d3_wb1", talent_days=Days.WED_SAT, talent_domain=d3, weekly_boss=wb1)
        Character.objects.create(name="c_ws_d3_wb2", talent_days=Days.WED_SAT, talent_domain=d3, weekly_boss=wb2)
        Character.objects.create(name="c_ws_d3_wb3", talent_days=Days.WED_SAT, talent_domain=d3, weekly_boss=wb3)
        Character.objects.create(name="c_ws_d3_wb4", talent_days=Days.WED_SAT, talent_domain=d3, weekly_boss=wb4)
        Character.objects.create(name="c_ws_d4_wb1", talent_days=Days.WED_SAT, talent_domain=d4, weekly_boss=wb1)
        Character.objects.create(name="c_ws_d4_wb2", talent_days=Days.WED_SAT, talent_domain=d4, weekly_boss=wb2)
        Character.objects.create(name="c_ws_d4_wb3", talent_days=Days.WED_SAT, talent_domain=d4, weekly_boss=wb3)
        Character.objects.create(name="c_ws_d4_wb4", talent_days=Days.WED_SAT, talent_domain=d4, weekly_boss=wb4)

        Character.objects.create(name="c_a_d1_wb1", talent_days=Days.ALWAYS, talent_domain=d1, weekly_boss=wb1)
        Character.objects.create(name="c_a_d1_wb2", talent_days=Days.ALWAYS, talent_domain=d1, weekly_boss=wb2)
        Character.objects.create(name="c_a_d1_wb3", talent_days=Days.ALWAYS, talent_domain=d1, weekly_boss=wb3)
        Character.objects.create(name="c_a_d1_wb4", talent_days=Days.ALWAYS, talent_domain=d1, weekly_boss=wb4)
        Character.objects.create(name="c_a_d2_wb1", talent_days=Days.ALWAYS, talent_domain=d2, weekly_boss=wb1)
        Character.objects.create(name="c_a_d2_wb2", talent_days=Days.ALWAYS, talent_domain=d2, weekly_boss=wb2)
        Character.objects.create(name="c_a_d2_wb3", talent_days=Days.ALWAYS, talent_domain=d2, weekly_boss=wb3)
        Character.objects.create(name="c_a_d2_wb4", talent_days=Days.ALWAYS, talent_domain=d2, weekly_boss=wb4)
        Character.objects.create(name="c_a_d3_wb1", talent_days=Days.ALWAYS, talent_domain=d3, weekly_boss=wb1)
        Character.objects.create(name="c_a_d3_wb2", talent_days=Days.ALWAYS, talent_domain=d3, weekly_boss=wb2)
        Character.objects.create(name="c_a_d3_wb3", talent_days=Days.ALWAYS, talent_domain=d3, weekly_boss=wb3)
        Character.objects.create(name="c_a_d3_wb4", talent_days=Days.ALWAYS, talent_domain=d3, weekly_boss=wb4)
        Character.objects.create(name="c_a_d4_wb1", talent_days=Days.ALWAYS, talent_domain=d4, weekly_boss=wb1)
        Character.objects.create(name="c_a_d4_wb2", talent_days=Days.ALWAYS, talent_domain=d4, weekly_boss=wb2)
        Character.objects.create(name="c_a_d4_wb3", talent_days=Days.ALWAYS, talent_domain=d4, weekly_boss=wb3)
        Character.objects.create(name="c_a_d4_wb4", talent_days=Days.ALWAYS, talent_domain=d4, weekly_boss=wb4)

    def create_user_command_message_data(self, command: str) -> dict:
        return {
            "update_id": 842895972,
            "message": {
                "message_id": 1111,
                "from": self.from_user,
                "chat": self.chat,
                "date": 1672684427,
                "text": command,
                "entities": [{"offset": 0, "length": len(command), "type": "bot_command"}],
            },
        }

    def create_user_text_message_data(self, text: str) -> dict:
        return {
            "update_id": 842895966,
            "message": {
                "message_id": 1111,
                "from": self.from_user,
                "chat": self.chat,
                "date": 1672674133,
                "text": text,
            },
        }

    def assertKeyboard(self, first, second: list[list[str]]):
        self.assertListEqual([[btn["text"] for btn in row] for row in first.keyboard], second)


@override_settings(TELEGRAM_BOT_SECRET_TOKEN="new-test-token")
class ForbiddenRequestTestCase(TelegramBotTestCase):
    def test_no_secret_key(self):
        response = self.client.post(reverse("tg_bot_webhook"), data=self.create_user_command_message_data("/start"))
        self.assertEqual(response.status_code, 403)

    def test_get_request(self):
        response = self.client.get(reverse("tg_bot_webhook"))
        self.assertEqual(response.status_code, 403)


@override_settings(TELEGRAM_BOT_SECRET_TOKEN="test-token")
@patch("telebot.TeleBot.send_message")
class StartCommandTestCase(TelegramBotTestCase):
    def test_start_command(self, mocked_send_message: Mock):
        self.client.post(reverse("tg_bot_webhook"), data=self.create_user_command_message_data("/start"))
        mocked_send_message.assert_called_once()
        called_args, called_kwargs = mocked_send_message.call_args
        self.assertTupleEqual(called_args, (self.chat["id"], "Привет\n\nСервер бота: <b>Европа</b>"))
        self.assertKeyboard(
            called_kwargs["reply_markup"], [["Неделя", "Сегодня", "Боссы"], ["Рассылка", "Управлять персонажами"]]
        )

    def test_back_text_command(self, mocked_send_message: Mock):
        self.assertTrue(User.objects.create(chat_id=self.chat["id"]))
        self.client.post(reverse("tg_bot_webhook"), data=self.create_user_text_message_data("Назад"))
        mocked_send_message.assert_called_once()
        called_args, called_kwargs = mocked_send_message.call_args
        self.assertTupleEqual(called_args, (self.chat["id"], "Привет\n\nСервер бота: <b>Европа</b>"))
        self.assertKeyboard(
            called_kwargs["reply_markup"], [["Неделя", "Сегодня", "Боссы"], ["Рассылка", "Управлять персонажами"]]
        )


@override_settings(TELEGRAM_BOT_SECRET_TOKEN="test-token")
@patch("telebot.TeleBot.send_message")
class TodayTextCommandTestCase(TelegramBotTestCase):
    def test_no_farm(self, mocked_send_message: Mock):
        self.client.post(reverse("tg_bot_webhook"), data=self.create_user_text_message_data("Сегодня"))
        mocked_send_message.assert_called_once()
        called_args, called_kwargs = mocked_send_message.call_args
        self.assertTupleEqual(
            called_args,
            (self.chat["id"], "Некого фармить. Если кого-то упустил, настрой в: <code>Управлять персонажами</code>"),
        )
        self.assertKeyboard(
            called_kwargs["reply_markup"], [["Неделя", "Сегодня", "Боссы"], ["Рассылка", "Управлять персонажами"]]
        )

    @patch("django.utils.timezone.now", lambda: datetime(2023, 1, 3))
    def test_valid_message__tuesday(self, mocked_send_message: Mock):
        self.populate_test_data()
        # other users
        u1 = User.objects.create(chat_id=1234)
        u2 = User.objects.create(chat_id=5678)
        u1.characters.set(Character.objects.all(), through_defaults={})
        u2.characters.set(Character.objects.all(), through_defaults={})

        user = User.objects.create(chat_id=self.chat["id"])
        user.characters.set(
            Character.objects.filter(
                name__in=["c_mt_d1_wb1", "c_tf_d1_wb1", "c_ws_d2_wb1", "c_a_d2_wb1", "c_a_d3_wb4"]
            ).all(),
            through_defaults={"normal_attack": 1, "elemental_skill": 1, "elemental_burst": 1},
        )
        self.assertEqual(user.characters.all().count(), 5)

        self.client.post(reverse("tg_bot_webhook"), data=self.create_user_text_message_data("Сегодня"))
        mocked_send_message.assert_called_once()
        called_args, called_kwargs = mocked_send_message.call_args
        good_text = (
            "<u>Вторник</u>\n"
            "<b>r1</b>: c_tf_d1_wb1 <i>(1, 1, 1)</i>\n\n"
            "<b>r2</b>: c_a_d2_wb1 <i>(1, 1, 1)</i>\n\n"
            "<b>r3</b>: c_a_d3_wb4 <i>(1, 1, 1)</i>"
        )
        self.assertTupleEqual(called_args, (self.chat["id"], good_text))
        self.assertKeyboard(
            called_kwargs["reply_markup"], [["Неделя", "Сегодня", "Боссы"], ["Рассылка", "Управлять персонажами"]]
        )
