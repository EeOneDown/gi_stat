from typing import Iterable

from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup  # noqa

from .commands import BotTextCommands, BotCallbackCommands
from .models import Character, User


class BotKeyboards:
    MAIN_MENU = (
        ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        .row(BotTextCommands.WEEK, BotTextCommands.TODAY, BotTextCommands.WEEKLY_BOSSES)
        .row(BotTextCommands.DAILY_SUBSCRIPTION, BotTextCommands.MANAGE_CHARACTERS)
    )
    MANAGE_CHARACTERS = (
        ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        .row(BotTextCommands.CHARACTER_LIST, BotTextCommands.FOLLOW_CHARACTERS, BotTextCommands.UNFOLLOW_CHARACTERS)
        .row(BotTextCommands.BACK)
    )

    INLINE_SHOW_ALL_TODAY = InlineKeyboardMarkup().row(BotCallbackCommands.SHOW_ALL_TODAY.as_inline_button())
    INLINE_SHOW_ALL_WEEK = InlineKeyboardMarkup().row(BotCallbackCommands.SHOW_ALL_WEEK.as_inline_button())
    INLINE_SHOW_ALL_WEEKLY_BOSSES = InlineKeyboardMarkup().row(
        BotCallbackCommands.SHOW_ALL_WEEKLY_BOSSES.as_inline_button()
    )

    @staticmethod
    def create_follow_characters_keyboard(characters: Iterable[Character]) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        keyboard.row(BotTextCommands.CHARACTER_TALENTS_INSTRUCTION)
        keyboard.add(*map(lambda character: character.name, characters), row_width=2)
        return keyboard.row(BotTextCommands.CANCEL)

    @staticmethod
    def create_unfollow_characters_keyboard(characters: Iterable[Character]) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        keyboard.row(BotTextCommands.UNFOLLOW_ALL_CHARACTERS)
        keyboard.add(*map(lambda character: f"- {character.name}", characters), row_width=2)
        return keyboard.row(BotTextCommands.CANCEL)

    @staticmethod
    def create_inline_change_daily_subscription_keyboard(user: User) -> InlineKeyboardMarkup:
        command = BotCallbackCommands.UNSUBSCRIBE_DAILY if user.is_subscribed else BotCallbackCommands.SUBSCRIBE_DAILY
        return InlineKeyboardMarkup().row(command.as_inline_button())
