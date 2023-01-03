import dataclasses

from telebot.types import InlineKeyboardButton  # noqa


class BotSlashCommands:
    START = "start"


class BotTextCommands:
    class BotTextCommand(str):
        def as_func(self) -> callable:
            return lambda message: message.text == self

    _ = BotTextCommand

    TODAY = _("Сегодня")
    WEEK = _("Неделя")
    WEEKLY_BOSSES = _("Боссы")
    DAILY_SUBSCRIPTION = _("Рассылка")
    MANAGE_CHARACTERS = _("Управлять персонажами")
    CHARACTER_LIST = _("Мои персонажи")
    FOLLOW_CHARACTERS = _("Добавить")
    CHARACTER_TALENTS_INSTRUCTION = _("Добавить таланты")
    UNFOLLOW_CHARACTERS = _("Удалить")
    UNFOLLOW_ALL_CHARACTERS = _("Удалить всех")
    BACK = _("Назад")
    CANCEL = _("Отменить")


class BotCallbackCommands:
    @dataclasses.dataclass
    class CallbackCommand:
        text: str
        callback_data: str

        def as_inline_button(self) -> InlineKeyboardButton:
            return InlineKeyboardButton(self.text, callback_data=self.callback_data)

        def as_func(self) -> callable:
            return lambda callback: callback.data == self.callback_data

    _ = CallbackCommand

    SUBSCRIBE_DAILY = _("Включить", "en_daily_sub")
    UNSUBSCRIBE_DAILY = _("Отключить", "dis_daily_sub")
    SHOW_ALL_TODAY = _("Показать всех", "show_all_today")
    SHOW_ALL_WEEK = _("Показать всех", "show_all_week")
    SHOW_ALL_WEEKLY_BOSSES = _("Показать всех", "show_all_wb")
