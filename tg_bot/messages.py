import re
from itertools import groupby
from typing import Iterable

from django.utils import timezone

from .commands import BotTextCommands
from .models import UserCharacter, Days


class BotMessages:
    WEEKDAY_LABELS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

    START = "Привет\n\nСервер бота: <b>Европа</b>"
    DAILY_SUBSCRIPTION = "Ежедневная рассылка <i>без звука</i> в <b>6 утра (МСК)</b>"
    MANAGE_CHARACTERS = "Выбери, что ты хочешь сделать"
    FOLLOW_CHARACTERS = "Выбери, кого ты хочешь добавить"
    UNFOLLOW_CHARACTERS = "Выбери, кого ты хочешь удалить"
    SUCCESSFULLY_FOLLOW_CHARACTER = "<b>{name}</b> теперь в списке твоих персонажей"
    SUCCESSFULLY_UNFOLLOW_CHARACTER = "<s>{name}</s> больше не в списке твоих персонажей"
    SUCCESSFULLY_UNFOLLOW_ALL_CHARACTERS = "Ты удалил всех своих персонажей"
    SUCCESSFULLY_UPDATED_CHARACTER_TALENTS = "Обновил персонажа <b>{name}</b>"
    NO_FARM = f"Некого фармить. Если кого-то упустил, настрой в: <code>{BotTextCommands.MANAGE_CHARACTERS}</code>"
    CHARACTER_NOT_FOUND = "Если это персонаж, то я такого не нашел"
    CHARACTER_TALENTS_INSTRUCTION = (
        "Чтобы добавить или обновить таланты, ответь на <b>свое</b> сообщение с именем персонажа, "
        "указав уровни талантов через пробел: <code>4 10 2</code>; "
        "или в любой момент напиши: <code>Эмбер 6 4 1</code>\n\n"
    )
    EMPTY_CHARACTER_LIST = "Твой список персонажей <u>пуст</u>"
    CHARACTER_LIST_LABEL = "Вот список твоих персонажей:\n\n"

    @classmethod
    def create_today_message(cls, user_characters: Iterable[UserCharacter]) -> str:
        def key(user_character: UserCharacter) -> str:
            return user_character.character.talent_domain.region.name

        if not user_characters:
            return cls.NO_FARM

        day_label = cls.WEEKDAY_LABELS[timezone.now().weekday()]

        return f"<u>{day_label}</u>\n" + "\n\n".join(
            f"<b>{region_name}</b>: {', '.join(map(cls.format_user_character, g_user_characters))}"
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
                text += f"<b>{region_name}</b>: {', '.join(map(cls.format_user_character, region_g_user_characters))}\n"
            text += "\n"
        return text

    @classmethod
    def create_bosses_message(cls, user_characters: Iterable[UserCharacter]) -> str:
        def key(user_character: UserCharacter) -> str:
            return user_character.character.weekly_boss.name

        if not user_characters:
            return cls.NO_FARM

        return "\n\n".join(
            f"<u><b>{weekly_boss_name}</b></u>: {', '.join(map(cls.format_user_character, g_user_characters))}"
            for weekly_boss_name, g_user_characters in groupby(user_characters, key)
        )

    @classmethod
    def create_character_list_message(cls, user_characters: Iterable[UserCharacter]) -> str:
        if not user_characters:
            return cls.EMPTY_CHARACTER_LIST

        return cls.CHARACTER_LIST_LABEL + "\n".join(map(cls.format_user_character, user_characters))

    # helpers
    @staticmethod
    def format_user_character(user_character: UserCharacter) -> str:
        """Returns a character name with talents if so: `name (x, x, x)` or `name`"""
        if user_character.normal_attack == user_character.elemental_skill == user_character.elemental_burst == 0:
            return user_character.character.name
        return (
            f"{user_character.character.name}"
            f" <i>({user_character.normal_attack},"
            f" {user_character.elemental_skill},"
            f" {user_character.elemental_burst})</i>"
        )


class BotRegexps:
    FOLLOW_CHARACTER = re.compile(r"^(?P<name>[а-яА-Я]+(?:[ -][а-яА-Я()]+)?)(?P<talents>(?: \d\d?){3})?$")
    UNFOLLOW_CHARACTER = re.compile(r"^- ?(?P<name>[а-яА-Я]+(?: [а-яА-Я]+)?)$")
    CHARACTER_TALENTS = re.compile(r"^\d\d? \d\d? \d\d?$")

    @classmethod
    def parse_follow_message(cls, text: str) -> tuple[str, dict[str, int]]:
        """Returns a character name and talents dict"""
        match = cls.FOLLOW_CHARACTER.match(text)
        character_name = match.groupdict()["name"]
        talents = match.groupdict()["talents"]
        return character_name, cls.parse_character_talents_message(talents)

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

        normal_attack, elemental_skill, elemental_burst = 0, 0, 0
        if text:
            normal_attack, elemental_skill, elemental_burst = map(limit_talent, text.split())
        return {
            "normal_attack": normal_attack,
            "elemental_skill": elemental_skill,
            "elemental_burst": elemental_burst,
        }
