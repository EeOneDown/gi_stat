from datetime import datetime
from unittest.mock import patch, Mock

from django.contrib.auth.models import User as DjangoUser
from django.test import TestCase, override_settings
from django.urls import reverse

from tg_bot.models import User, Region, WeeklyBoss, Domain, Character, Days


@override_settings(TELEGRAM_BOT_SECRET_TOKEN="test-token")
class TelegramBotTestCase(TestCase):
    def setUp(self) -> None:
        self.from_user = {
            "id": 1234567890,
            "is_bot": False,
            "first_name": "Test",
            "last_name": "User",
            "username": "test-username",
            "language_code": "en",
            "is_premium": True,
        }
        self.from_bot = {
            "id": 987654321,
            "is_bot": True,
            "first_name": "Bot",
            "username": "test_bot",
        }
        self.bot_message_id = 9999
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

        # test users and m2m
        u1 = User.objects.create(chat_id=1234)
        u2 = User.objects.create(chat_id=5678)
        u1.characters.set(Character.objects.all(), through_defaults={})
        u2.characters.set(Character.objects.all(), through_defaults={})

    def make_asserted_bot_request(self, data: dict, secret_token: str = None, expected_status_code: int = 200):
        response = self.client.post(
            reverse("tg_bot_webhook"),
            data=data,
            content_type="application/json",
            HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN=secret_token or "test-token",
        )
        self.assertEqual(response.status_code, expected_status_code)
        return response

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

    def create_user_callback_query_data(self, data: str) -> dict:
        return {
            "update_id": 842895974,
            "callback_query": {
                "id": "860998169111195948",
                "from": self.from_user,
                "message": {
                    "message_id": self.bot_message_id,
                    "from": self.from_bot,
                    "chat": self.chat,
                    "date": 1672710369,
                    "text": "some-test",
                    "entities": [],
                    "reply_markup": {"inline_keyboard": [[{"text": "btn", "callback_data": data}]]},
                },
                "chat_instance": "-4263294929375246591",
                "data": data,
            },
        }

    def assertKeyboard(self, first, second: list[list[str]]):
        self.assertListEqual([[btn["text"] for btn in row] for row in first.keyboard], second)

    def assertInlineKeyboard(self, first, second: list[list[tuple[str, str]]]):
        self.assertListEqual([[(btn.text, btn.callback_data) for btn in row] for row in first.keyboard], second)


class ForbiddenRequestTestCase(TelegramBotTestCase):
    def test_no_secret_key(self):
        self.make_asserted_bot_request(
            self.create_user_command_message_data("/start"), secret_token="bad", expected_status_code=403
        )

    def test_get_request(self):
        response = self.client.get(reverse("tg_bot_webhook"))
        self.assertEqual(response.status_code, 403)


@patch("telebot.TeleBot.send_message")
class StartCommandTestCase(TelegramBotTestCase):
    def test_start_command(self, mocked_send_message: Mock):
        self.make_asserted_bot_request(self.create_user_command_message_data("/start"))
        mocked_send_message.assert_called_once()
        called_args, called_kwargs = mocked_send_message.call_args
        self.assertTupleEqual(called_args, (self.chat["id"], "Привет\n\nСервер бота: <b>Европа</b>"))
        self.assertKeyboard(
            called_kwargs["reply_markup"], [["Неделя", "Сегодня", "Боссы"], ["Рассылка", "Управлять персонажами"]]
        )

    def test_back_text_command(self, mocked_send_message: Mock):
        self.assertTrue(User.objects.create(chat_id=self.chat["id"]))
        self.make_asserted_bot_request(self.create_user_text_message_data("Назад"))
        mocked_send_message.assert_called_once()
        called_args, called_kwargs = mocked_send_message.call_args
        self.assertTupleEqual(called_args, (self.chat["id"], "Привет\n\nСервер бота: <b>Европа</b>"))
        self.assertKeyboard(
            called_kwargs["reply_markup"], [["Неделя", "Сегодня", "Боссы"], ["Рассылка", "Управлять персонажами"]]
        )


@patch("telebot.TeleBot.send_message")
class TodayTextCommandTestCase(TelegramBotTestCase):
    def test_no_farm(self, mocked_send_message: Mock):
        self.make_asserted_bot_request(self.create_user_text_message_data("Сегодня"))
        mocked_send_message.assert_called_once()
        called_args, called_kwargs = mocked_send_message.call_args
        self.assertTupleEqual(
            called_args,
            (self.chat["id"], "Некого фармить. Если кого-то упустил, настрой в: <code>Управлять персонажами</code>"),
        )
        self.assertInlineKeyboard(called_kwargs["reply_markup"], [[("Показать всех", "show_all_today")]])

    @patch("django.utils.timezone.now", lambda: datetime(2023, 1, 3))
    def test_valid_message__tuesday(self, mocked_send_message: Mock):
        self.populate_test_data()

        user = User.objects.create(chat_id=self.chat["id"])
        user.characters.set(
            Character.objects.filter(
                name__in=["c_mt_d1_wb1", "c_tf_d1_wb1", "c_ws_d2_wb1", "c_a_d2_wb1", "c_a_d3_wb4"]
            ).all(),
            through_defaults={"normal_attack": 1, "elemental_skill": 1, "elemental_burst": 1},
        )
        self.assertEqual(user.characters.all().count(), 5)

        self.make_asserted_bot_request(self.create_user_text_message_data("Сегодня"))
        mocked_send_message.assert_called_once()
        called_args, called_kwargs = mocked_send_message.call_args
        good_text = (
            "<u>Вторник</u>\n"
            "<b>r1</b>: c_tf_d1_wb1 <i>(1, 1, 1)</i>\n\n"
            "<b>r2</b>: c_a_d2_wb1 <i>(1, 1, 1)</i>\n\n"
            "<b>r3</b>: c_a_d3_wb4 <i>(1, 1, 1)</i>"
        )
        self.assertTupleEqual(called_args, (self.chat["id"], good_text))
        self.assertInlineKeyboard(called_kwargs["reply_markup"], [[("Показать всех", "show_all_today")]])

    @patch("django.utils.timezone.now", lambda: datetime(2023, 1, 1))
    def test_valid_message__sunday(self, mocked_send_message: Mock):
        self.populate_test_data()

        user = User.objects.create(chat_id=self.chat["id"])
        user.characters.set(
            Character.objects.filter(name__in=["c_mt_d1_wb1", "c_tf_d2_wb1", "c_ws_d3_wb1", "c_a_d4_wb1"]).all(),
            through_defaults={"normal_attack": 1, "elemental_skill": 1, "elemental_burst": 1},
        )
        self.assertEqual(user.characters.all().count(), 4)

        self.make_asserted_bot_request(self.create_user_text_message_data("Сегодня"))
        mocked_send_message.assert_called_once()
        called_args, called_kwargs = mocked_send_message.call_args
        good_text = (
            "<u>Воскресенье</u>\n"
            "<b>r1</b>: c_mt_d1_wb1 <i>(1, 1, 1)</i>\n\n"
            "<b>r2</b>: c_tf_d2_wb1 <i>(1, 1, 1)</i>\n\n"
            "<b>r3</b>: c_ws_d3_wb1 <i>(1, 1, 1)</i>\n\n"
            "<b>r4</b>: c_a_d4_wb1 <i>(1, 1, 1)</i>"
        )
        self.assertTupleEqual(called_args, (self.chat["id"], good_text))
        self.assertInlineKeyboard(called_kwargs["reply_markup"], [[("Показать всех", "show_all_today")]])


@patch("telebot.TeleBot.send_message")
class WeeklyBossesTextCommandTestCase(TelegramBotTestCase):
    def test_no_farm(self, mocked_send_message: Mock):
        self.make_asserted_bot_request(self.create_user_text_message_data("Боссы"))
        mocked_send_message.assert_called_once()
        called_args, called_kwargs = mocked_send_message.call_args
        self.assertTupleEqual(
            called_args,
            (self.chat["id"], "Некого фармить. Если кого-то упустил, настрой в: <code>Управлять персонажами</code>"),
        )
        self.assertInlineKeyboard(called_kwargs["reply_markup"], [[("Показать всех", "show_all_wb")]])

    def test_valid_message(self, mocked_send_message: Mock):
        self.populate_test_data()

        user = User.objects.create(chat_id=self.chat["id"])
        user.characters.set(
            Character.objects.filter(name__in=["c_ws_d2_wb1", "c_a_d2_wb3", "c_a_d3_wb4"]).all(),
            through_defaults={},
        )
        self.assertEqual(user.characters.all().count(), 3)

        self.make_asserted_bot_request(self.create_user_text_message_data("Боссы"))
        mocked_send_message.assert_called_once()
        called_args, called_kwargs = mocked_send_message.call_args
        good_text = "<u><b>wb1</b></u>: c_ws_d2_wb1\n\n<u><b>wb3</b></u>: c_a_d2_wb3\n\n<u><b>wb4</b></u>: c_a_d3_wb4"
        self.assertTupleEqual(called_args, (self.chat["id"], good_text))
        self.assertInlineKeyboard(called_kwargs["reply_markup"], [[("Показать всех", "show_all_wb")]])


@patch("telebot.TeleBot.send_message")
class WeekTextCommandTestCase(TelegramBotTestCase):
    def test_no_farm(self, mocked_send_message: Mock):
        self.make_asserted_bot_request(self.create_user_text_message_data("Неделя"))
        mocked_send_message.assert_called_once()
        called_args, called_kwargs = mocked_send_message.call_args
        self.assertTupleEqual(
            called_args,
            (self.chat["id"], "Некого фармить. Если кого-то упустил, настрой в: <code>Управлять персонажами</code>"),
        )
        self.assertInlineKeyboard(called_kwargs["reply_markup"], [[("Показать всех", "show_all_week")]])

    def test_valid_message(self, mocked_send_message: Mock):
        self.populate_test_data()

        user = User.objects.create(chat_id=self.chat["id"])
        user.characters.set(
            Character.objects.filter(
                name__in=["c_mt_d1_wb1", "c_tf_d1_wb1", "c_ws_d2_wb1", "c_a_d2_wb1", "c_a_d3_wb4"]
            ).all(),
            through_defaults={},
        )
        self.assertEqual(user.characters.all().count(), 5)

        self.make_asserted_bot_request(self.create_user_text_message_data("Неделя"))
        mocked_send_message.assert_called_once()
        called_args, called_kwargs = mocked_send_message.call_args
        good_text = (
            "<u>Всегда</u>\n"
            "<b>r2</b>: c_a_d2_wb1\n"
            "<b>r3</b>: c_a_d3_wb4\n\n"
            "<u>Понедельник/Четверг</u>\n"
            "<b>r1</b>: c_mt_d1_wb1\n\n"
            "<u>Вторник/Пятница</u>\n"
            "<b>r1</b>: c_tf_d1_wb1\n\n"
            "<u>Среда/Суббота</u>\n"
            "<b>r2</b>: c_ws_d2_wb1"
        )
        self.assertTupleEqual(called_args, (self.chat["id"], good_text))
        self.assertInlineKeyboard(called_kwargs["reply_markup"], [[("Показать всех", "show_all_week")]])


@patch("telebot.TeleBot.send_message")
class DailySubscriptionTextCommandTestCase(TelegramBotTestCase):
    def test_not_subscribed(self, mocked_send_message: Mock):
        self.make_asserted_bot_request(self.create_user_text_message_data("Рассылка"))
        mocked_send_message.assert_called_once()
        called_args, called_kwargs = mocked_send_message.call_args
        self.assertTupleEqual(
            called_args, (self.chat["id"], "Ежедневная рассылка <i>без звука</i> в <b>6 утра (МСК)</b>")
        )
        self.assertInlineKeyboard(called_kwargs["reply_markup"], [[("Включить", "en_daily_sub")]])

    def test_subscribed(self, mocked_send_message: Mock):
        User.objects.create(chat_id=self.chat["id"], is_subscribed=True)
        self.make_asserted_bot_request(self.create_user_text_message_data("Рассылка"))
        mocked_send_message.assert_called_once()
        called_args, called_kwargs = mocked_send_message.call_args
        self.assertTupleEqual(
            called_args, (self.chat["id"], "Ежедневная рассылка <i>без звука</i> в <b>6 утра (МСК)</b>")
        )
        self.assertInlineKeyboard(called_kwargs["reply_markup"], [[("Отключить", "dis_daily_sub")]])


@patch("telebot.TeleBot.send_message")
class ManageCharactersTextCommandTestCase(TelegramBotTestCase):
    def test_manage_characters_command(self, mocked_send_message: Mock):
        self.make_asserted_bot_request(self.create_user_text_message_data("Управлять персонажами"))
        mocked_send_message.assert_called_once()
        called_args, called_kwargs = mocked_send_message.call_args
        self.assertTupleEqual(called_args, (self.chat["id"], "Выбери, что ты хочешь сделать"))
        self.assertKeyboard(called_kwargs["reply_markup"], [["Мои персонажи", "Добавить", "Удалить"], ["Назад"]])

    def test_cancel_command(self, mocked_send_message: Mock):
        self.make_asserted_bot_request(self.create_user_text_message_data("Отменить"))
        mocked_send_message.assert_called_once()
        called_args, called_kwargs = mocked_send_message.call_args
        self.assertTupleEqual(called_args, (self.chat["id"], "Выбери, что ты хочешь сделать"))
        self.assertKeyboard(called_kwargs["reply_markup"], [["Мои персонажи", "Добавить", "Удалить"], ["Назад"]])


@patch("telebot.TeleBot.edit_message_reply_markup")
class DailySubscriptionCallbackTestCase(TelegramBotTestCase):
    def test_subscribe(self, mocked_send_message: Mock):
        self.make_asserted_bot_request(self.create_user_callback_query_data("en_daily_sub"))
        mocked_send_message.assert_called_once()
        called_args, called_kwargs = mocked_send_message.call_args
        self.assertTupleEqual(called_args, (self.chat["id"], self.bot_message_id))
        self.assertInlineKeyboard(called_kwargs["reply_markup"], [[("Отключить", "dis_daily_sub")]])
        self.assertTrue(User.objects.filter(chat_id=self.chat["id"], is_subscribed=True).exists())

    def test_unsubscribe(self, mocked_send_message: Mock):
        User.objects.create(chat_id=self.chat["id"], is_subscribed=True)
        self.make_asserted_bot_request(self.create_user_callback_query_data("dis_daily_sub"))
        mocked_send_message.assert_called_once()
        called_args, called_kwargs = mocked_send_message.call_args
        self.assertTupleEqual(called_args, (self.chat["id"], self.bot_message_id))
        self.assertInlineKeyboard(called_kwargs["reply_markup"], [[("Включить", "en_daily_sub")]])
        self.assertTrue(User.objects.filter(chat_id=self.chat["id"], is_subscribed=False).exists())


@patch("logging.Logger.error")
class HandlerFailedTestCase(TelegramBotTestCase):
    def test_log_called(self, mocked_logger_error: Mock):
        with patch("telebot.TeleBot.process_new_updates", side_effect=Exception):
            response = self.make_asserted_bot_request({"test": "test"})

        self.assertEqual(response.status_code, 200)
        mocked_logger_error.assert_called_once()


@override_settings(BASE_DOMAIN="test.com")
@override_settings(TELEGRAM_BOT_SECRET_TOKEN="test-secret-token")
@patch("telebot.TeleBot.set_webhook")
class SetWebhookTestCase(TestCase):
    def setUp(self) -> None:
        self.admin_user = DjangoUser.objects.create(username="test-admin", email="test@test.com", is_staff=True)
        self.admin_user.set_password("test-password")
        self.admin_user.save()

    def test_bot_called(self, mocked_set_webhook: Mock):
        self.assertTrue(self.client.login(username=self.admin_user.username, password="test-password"))
        response = self.client.get(reverse("set_webhook"))
        self.assertEqual(response.status_code, 200)
        mocked_set_webhook.assert_called_once()
        called_args, called_kwargs = mocked_set_webhook.call_args
        self.assertTupleEqual(called_args, ())
        self.assertEqual(called_kwargs["url"], "https://test.com/tg_bot/webhook")
        self.assertEqual(called_kwargs["secret_token"], "test-secret-token")

    def test_login_required(self, mocked_set_webhook: Mock):
        response = self.client.get(reverse("set_webhook"))
        self.assertEqual(response.status_code, 302)
        mocked_set_webhook.assert_not_called()
