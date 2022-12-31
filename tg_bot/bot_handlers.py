import dataclasses
import re
from itertools import groupby
from typing import Iterable

from django.conf import settings
from django.utils import timezone
from telebot import TeleBot  # noqa
from telebot.types import (  # noqa
    Message,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from tg_bot.models import User, Days, Character, UserCharacter

bot = TeleBot(token=settings.TELEGRAM_BOT_RELEASE_TOKEN, threaded=False, parse_mode="HTML")


class BotTextCommands:
    TODAY = "Сегодня"
    WEEK = "Неделя"
    WEEKLY_BOSSES = "Боссы"
    DAILY_SUBSCRIPTION = "Рассылка"
    MANAGE_CHARACTERS = "Управлять персонажами"
    FOLLOW_CHARACTERS = "Следить"
    UNFOLLOW_CHARACTERS = "Отписаться"
    UNFOLLOW_ALL_CHARACTERS = "Отписаться от всех"
    BACK = "Назад"
    CANCEL = "Отменить"

    @staticmethod
    def as_regexp(text: str) -> str:
        return f"^{text}$"


class BotCallbackCommands:
    @dataclasses.dataclass
    class CallbackCommand:
        text: str
        callback_data: str

        def as_inline_button(self) -> InlineKeyboardButton:
            return InlineKeyboardButton(self.text, callback_data=self.callback_data)

    SUBSCRIBE_DAILY = CallbackCommand("Включить", "en_daily_sub")
    UNSUBSCRIBE_DAILY = CallbackCommand("Отключить", "dis_daily_sub")

    @staticmethod
    def as_func(callback_command: CallbackCommand) -> callable:
        return lambda callback: callback.data == callback_command.callback_data


class BotMessages:
    WEEKDAY_LABELS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

    START = "Привет\n\n<b>Бот только для европейского сервера</b>"
    DAILY_SUBSCRIPTION = "Ежедневная рассылка в 6 утра"
    MANAGE_CHARACTERS = "Выбери, что ты хочешь сделать"
    FOLLOW_CHARACTERS = "Выбери, за кем ты хочешь следить"
    UNFOLLOW_CHARACTERS = "Выбери, от кого ты хочешь отписаться"
    SUCCESSFULLY_FOLLOW_CHARACTER = (
        "<b>{name}</b> теперь в списке твоих персонажей\n"
        "По желанию, чтобы добавить или обновить таланты, ответь на свое сообщение выше: <code>4 10 2</code>; "
        "или в любой момент напиши: <code>{name} 6 4 1</code>\n\n"
        + MANAGE_CHARACTERS
    )
    SUCCESSFULLY_UNFOLLOW_CHARACTER = "<s>{name}</s> больше не в списке твоих персонажей\n\n" + MANAGE_CHARACTERS
    SUCCESSFULLY_UNFOLLOW_ALL_CHARACTER = "Ты отписался от всех персонажей\n\n" + MANAGE_CHARACTERS
    SUCCESSFULLY_UPDATED_CHARACTER_TALENTS = "Обновил таланты для персонажа <b>{name}</b>"
    NO_FARM = f"Некого фармить. Если кого-то упустил, настрой в: <code>{BotTextCommands.MANAGE_CHARACTERS}</code>"
    CHARACTER_NOT_FOUND = "Если это персонаж, то я такого не нашел"

    @classmethod
    def create_today_message(cls, user_characters: Iterable[UserCharacter]) -> str:
        def key(user_character: UserCharacter) -> str:
            return user_character.character.talent_domain.region.name

        if not user_characters:
            return cls.NO_FARM

        day_label = cls.WEEKDAY_LABELS[timezone.now().weekday()]

        return f"<u>{day_label}</u>\n" + "\n\n".join(
            f"<b>{region_name}</b>: {', '.join(map(cls._format_user_character, g_user_characters))}"
            for region_name, g_user_characters in groupby(user_characters, key)
        )

    @classmethod
    def create_week_message(cls, user_characters: Iterable[UserCharacter]) -> str:
        def key_talent_days(user_character: UserCharacter) -> int:
            return user_character.character.talent_days

        def key_region_name(user_character: UserCharacter) -> str:
            return user_character.character.talent_domain.region.name

        if not user_characters:
            return cls.NO_FARM

        text = ""
        for day, day_g_user_characters in groupby(user_characters, key_talent_days):
            text += f"<u>{dict(Days.choices)[day]}</u>\n"
            for region_name, region_g_user_characters in groupby(day_g_user_characters, key_region_name):
                text += (
                    f"<b>{region_name}</b>: {', '.join(map(cls._format_user_character, region_g_user_characters))}\n"
                )
            text += "\n"
        return text

    @classmethod
    def create_bosses_message(cls, user_characters: Iterable[UserCharacter]) -> str:
        def key(user_character: UserCharacter) -> str:
            return user_character.character.weekly_boss.name

        if not user_characters:
            return cls.NO_FARM

        return "\n\n".join(
            f"<u><b>{weekly_boss_name}</b></u>: {', '.join(map(cls._format_user_character, g_user_characters))}"
            for weekly_boss_name, g_user_characters in groupby(user_characters, key)
        )

    # helpers
    @staticmethod
    def _format_user_character(user_character: UserCharacter) -> str:
        """Returns a character name with talents if so: `name (x, x, x)` or `name`"""
        if user_character.normal_attack == user_character.elemental_skill == user_character.elemental_burst == 0:
            return user_character.character.name
        return (
            f"{user_character.character.name}"
            f" <i>({user_character.normal_attack},"
            f" {user_character.elemental_skill},"
            f" {user_character.elemental_burst})</i>"
        )


class BotKeyboards:
    MAIN_MENU = (
        ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        .row(BotTextCommands.WEEK, BotTextCommands.WEEKLY_BOSSES, BotTextCommands.TODAY)
        .row(BotTextCommands.DAILY_SUBSCRIPTION, BotTextCommands.MANAGE_CHARACTERS)
    )
    MANAGE_CHARACTERS = (
        ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        .row(BotTextCommands.FOLLOW_CHARACTERS, BotTextCommands.UNFOLLOW_CHARACTERS)
        .row(BotTextCommands.BACK)
    )

    @staticmethod
    def create_follow_characters_keyboard(characters: Iterable[Character]) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
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


class BotRegexps:
    FOLLOW_CHARACTER = re.compile(r"^(?P<name>[а-яА-Я]+(?:[ -][а-яА-Я()]+)?)(?P<talents>(?: \d\d?){3})?$")
    UNFOLLOW_CHARACTER = re.compile(r"^- ?(?P<name>[а-яА-Я]+(?: [а-яА-Я]+)?)$")
    CHARACTER_TALENTS = re.compile(r"^\d\d? \d\d? \d\d?$")

    @classmethod
    def parse_follow_message(cls, text: str) -> tuple[str, dict[str, int]]:
        """Returns a character name and talents dict (or empty dict)"""
        match = cls.FOLLOW_CHARACTER.match(text)
        character_name = match.groupdict()["name"]
        talents = match.groupdict()["talents"]
        return character_name, cls.parse_character_talents_message(talents) if talents else {}

    @classmethod
    def parse_unfollow_message(cls, text: str) -> str:
        """Returns a character name"""
        match = cls.UNFOLLOW_CHARACTER.match(text)
        return match.groupdict()["name"]

    @classmethod
    def parse_character_talents_message(cls, text: str) -> dict:
        """Returns a character talents dict"""

        def limit_talent(x: str) -> int:
            # 0 <= x <= 15
            return max(min(int(x), 15), 0)

        normal_attack, elemental_skill, elemental_burst = map(limit_talent, text.split())
        return {
            "normal_attack": normal_attack,
            "elemental_skill": elemental_skill,
            "elemental_burst": elemental_burst,
        }


def handle_character_not_found(function: callable) -> callable:
    def wrapper(message: Message) -> None:
        try:
            function(message)
        except Character.DoesNotExist:
            bot.reply_to(message, BotMessages.CHARACTER_NOT_FOUND)

    return wrapper


@bot.message_handler(commands=["start"])
@bot.message_handler(regexp=BotTextCommands.as_regexp(BotTextCommands.BACK))
def bot_command_start(message: Message) -> None:
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    bot.send_message(user.chat_id, BotMessages.START, reply_markup=BotKeyboards.MAIN_MENU)


@bot.message_handler(regexp=BotTextCommands.as_regexp(BotTextCommands.DAILY_SUBSCRIPTION))
def bot_command_daily_subscription(message: Message) -> None:
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    keyboard = BotKeyboards.create_inline_change_daily_subscription_keyboard(user)
    bot.send_message(user.chat_id, BotMessages.DAILY_SUBSCRIPTION, reply_markup=keyboard)


@bot.message_handler(regexp=BotTextCommands.as_regexp(BotTextCommands.MANAGE_CHARACTERS))
@bot.message_handler(regexp=BotTextCommands.as_regexp(BotTextCommands.CANCEL))
def bot_text_command_manage_characters(message: Message):
    bot.send_message(message.chat.id, BotMessages.MANAGE_CHARACTERS, reply_markup=BotKeyboards.MANAGE_CHARACTERS)


@bot.message_handler(regexp=BotTextCommands.as_regexp(BotTextCommands.FOLLOW_CHARACTERS))
def bot_text_command_follow_characters(message: Message):
    characters = Character.objects.exclude(users__chat_id=message.chat.id).all()
    keyboard = BotKeyboards.create_follow_characters_keyboard(characters)
    bot.send_message(message.chat.id, BotMessages.FOLLOW_CHARACTERS, reply_markup=keyboard)


@bot.message_handler(regexp=BotTextCommands.as_regexp(BotTextCommands.UNFOLLOW_CHARACTERS))
def bot_text_command_unfollow_characters(message: Message):
    characters = Character.objects.filter(users__chat_id=message.chat.id).all()
    keyboard = BotKeyboards.create_unfollow_characters_keyboard(characters)
    bot.send_message(message.chat.id, BotMessages.UNFOLLOW_CHARACTERS, reply_markup=keyboard)


@bot.message_handler(regexp=BotTextCommands.as_regexp(BotTextCommands.UNFOLLOW_ALL_CHARACTERS))
def bot_unfollow_all_character(message: Message) -> None:
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    user.characters.clear()
    bot.send_message(
        user.chat_id, BotMessages.SUCCESSFULLY_UNFOLLOW_ALL_CHARACTER, reply_markup=BotKeyboards.MANAGE_CHARACTERS
    )


@bot.message_handler(regexp=BotTextCommands.as_regexp(BotTextCommands.TODAY))
def bot_text_command_today(message: Message) -> None:
    days = Days.get_by_weekday(timezone.now().weekday())
    user_characters = (
        UserCharacter.objects.filter(user__chat_id=message.chat.id, character__talent_days__in=days)
        .select_related("character__talent_domain__region")
        # order by region for in-code 'group by'
        .order_by("character__talent_domain__region_id")
        .all()
    )
    bot.send_message(
        message.chat.id, BotMessages.create_today_message(user_characters), reply_markup=BotKeyboards.MAIN_MENU
    )


@bot.message_handler(regexp=BotTextCommands.as_regexp(BotTextCommands.WEEK))
def bot_text_command_week(message: Message) -> None:
    user_characters = (
        UserCharacter.objects.filter(user__chat_id=message.chat.id)
        .select_related("character__talent_domain__region")
        # order by region for in-code 'group by'
        .order_by("character__talent_days", "character__talent_domain__region_id")
        .all()
    )
    bot.send_message(
        message.chat.id, BotMessages.create_week_message(user_characters), reply_markup=BotKeyboards.MAIN_MENU
    )


@bot.message_handler(regexp=BotTextCommands.as_regexp(BotTextCommands.WEEKLY_BOSSES))
def bot_text_command_weekly_bosses(message: Message) -> None:
    user_characters = (
        UserCharacter.objects.filter(user__chat_id=message.chat.id)
        .select_related("character__weekly_boss")
        .order_by("character__weekly_boss_id")  # order by region for the next 'group by'
        .all()
    )
    bot.send_message(
        message.chat.id, BotMessages.create_bosses_message(user_characters), reply_markup=BotKeyboards.MAIN_MENU
    )


@bot.message_handler(regexp=BotRegexps.FOLLOW_CHARACTER.pattern)
@handle_character_not_found
def bot_follow_character(message: Message) -> None:
    character_name, talents_dict = BotRegexps.parse_follow_message(message.text)
    character = Character.objects.get(name=character_name)
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    user.characters.remove(character)
    user.characters.add(character, through_defaults=talents_dict)
    bot.send_message(
        user.chat_id,
        BotMessages.SUCCESSFULLY_FOLLOW_CHARACTER.format(name=character.name),
        reply_markup=BotKeyboards.MANAGE_CHARACTERS,
    )


@bot.message_handler(regexp=BotRegexps.UNFOLLOW_CHARACTER.pattern)
@handle_character_not_found
def bot_unfollow_character(message: Message) -> None:
    character_name = BotRegexps.parse_unfollow_message(message.text)
    character = Character.objects.get(name=character_name)
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    user.characters.remove(character)
    bot.send_message(
        user.chat_id,
        BotMessages.SUCCESSFULLY_UNFOLLOW_CHARACTER.format(name=character.name),
        reply_markup=BotKeyboards.MANAGE_CHARACTERS,
    )


@bot.message_handler(
    # new talents
    regexp=BotRegexps.CHARACTER_TALENTS.pattern,
    # replies to added character
    func=lambda message: message.reply_to_message and BotRegexps.FOLLOW_CHARACTER.match(message.reply_to_message.text),
)
@handle_character_not_found
def bot_character_talents(message: Message) -> None:
    talents_dict = BotRegexps.parse_character_talents_message(message.text)
    character_name, _ = BotRegexps.parse_follow_message(message.reply_to_message.text)
    character = Character.objects.get(name=character_name)
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    user.characters.remove(character)
    user.characters.add(character, through_defaults=talents_dict)
    bot.send_message(user.chat_id, BotMessages.SUCCESSFULLY_UPDATED_CHARACTER_TALENTS.format(name=character.name))


@bot.callback_query_handler(func=BotCallbackCommands.as_func(BotCallbackCommands.SUBSCRIBE_DAILY))
@bot.callback_query_handler(func=BotCallbackCommands.as_func(BotCallbackCommands.UNSUBSCRIBE_DAILY))
def bot_change_daily_subscription(callback: CallbackQuery) -> None:
    user, _ = User.objects.get_or_create(chat_id=callback.message.chat.id)
    user.is_subscribed = not user.is_subscribed
    user.save(update_fields=["is_subscribed"])
    keyboard = BotKeyboards.create_inline_change_daily_subscription_keyboard(user)
    bot.edit_message_reply_markup(user.chat_id, callback.message.id, reply_markup=keyboard)
