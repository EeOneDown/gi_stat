from django.conf import settings
from django.utils import timezone
from telebot import TeleBot  # noqa
from telebot.types import Message, CallbackQuery  # noqa

from .commands import BotSlashCommands, BotTextCommands, BotCallbackCommands
from .messages import BotMessages, BotRegexps
from .keyboards import BotKeyboards
from .models import User, Days, Character, UserCharacter

bot = TeleBot(token=settings.TELEGRAM_BOT_RELEASE_TOKEN, threaded=False, parse_mode="HTML")


def handle_character_not_found(function: callable) -> callable:
    def wrapper(message: Message) -> None:
        try:
            function(message)
        except Character.DoesNotExist:
            bot.reply_to(message, BotMessages.CHARACTER_NOT_FOUND)

    return wrapper


@bot.message_handler(commands=[BotSlashCommands.START])
@bot.message_handler(regexp=BotTextCommands.BACK.as_regexp())
def bot_command_start(message: Message) -> None:
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    bot.send_message(user.chat_id, BotMessages.START, reply_markup=BotKeyboards.MAIN_MENU)


@bot.message_handler(regexp=BotTextCommands.TODAY.as_regexp())
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


@bot.message_handler(regexp=BotTextCommands.WEEK.as_regexp())
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


@bot.message_handler(regexp=BotTextCommands.WEEKLY_BOSSES.as_regexp())
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


@bot.message_handler(regexp=BotTextCommands.DAILY_SUBSCRIPTION.as_regexp())
def bot_text_command_daily_subscription(message: Message) -> None:
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    keyboard = BotKeyboards.create_inline_change_daily_subscription_keyboard(user)
    bot.send_message(user.chat_id, BotMessages.DAILY_SUBSCRIPTION, reply_markup=keyboard)


@bot.message_handler(regexp=BotTextCommands.MANAGE_CHARACTERS.as_regexp())
@bot.message_handler(regexp=BotTextCommands.CANCEL.as_regexp())
def bot_text_command_manage_characters(message: Message) -> None:
    bot.send_message(message.chat.id, BotMessages.MANAGE_CHARACTERS, reply_markup=BotKeyboards.MANAGE_CHARACTERS)


@bot.message_handler(regexp=BotTextCommands.CHARACTER_LIST.as_regexp())
def bot_text_command_character_list(message: Message) -> None:
    user_characters = (
        UserCharacter.objects.filter(user__chat_id=message.chat.id)
        .select_related("character")
        .order_by("character__name")
        .all()
    )
    bot.send_message(message.chat.id, BotMessages.create_character_list_message(user_characters))


@bot.message_handler(regexp=BotTextCommands.FOLLOW_CHARACTERS.as_regexp())
def bot_text_command_follow_characters(message: Message) -> None:
    characters = Character.objects.exclude(users__chat_id=message.chat.id).all()
    keyboard = BotKeyboards.create_follow_characters_keyboard(characters)
    bot.send_message(message.chat.id, BotMessages.FOLLOW_CHARACTERS, reply_markup=keyboard)


@bot.message_handler(regexp=BotTextCommands.CHARACTER_TALENTS_INSTRUCTION.as_regexp())
def bot_text_command_character_talents_instruction(message: Message) -> None:
    bot.send_message(message.chat.id, BotMessages.CHARACTER_TALENTS_INSTRUCTION)


@bot.message_handler(regexp=BotTextCommands.UNFOLLOW_CHARACTERS.as_regexp())
def bot_text_command_unfollow_characters(message: Message) -> None:
    characters = Character.objects.filter(users__chat_id=message.chat.id).all()
    keyboard = BotKeyboards.create_unfollow_characters_keyboard(characters)
    bot.send_message(message.chat.id, BotMessages.UNFOLLOW_CHARACTERS, reply_markup=keyboard)


@bot.message_handler(regexp=BotTextCommands.UNFOLLOW_ALL_CHARACTERS.as_regexp())
def bot_text_command_unfollow_all_characters(message: Message) -> None:
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    user.characters.clear()
    bot.send_message(
        user.chat_id, BotMessages.SUCCESSFULLY_UNFOLLOW_ALL_CHARACTERS, reply_markup=BotKeyboards.MANAGE_CHARACTERS
    )


@bot.message_handler(regexp=BotRegexps.FOLLOW_CHARACTER.pattern)
@handle_character_not_found
def bot_regexp_follow_character(message: Message) -> None:
    character_name, talents_dict = BotRegexps.parse_follow_message(message.text)
    character = Character.objects.get(name=character_name)
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    user_character, _ = UserCharacter.objects.update_or_create(user=user, character=character, defaults=talents_dict)
    bot.send_message(
        user.chat_id,
        BotMessages.SUCCESSFULLY_FOLLOW_CHARACTER.format(name=BotMessages.format_user_character(user_character)),
        reply_markup=BotKeyboards.MANAGE_CHARACTERS,
    )


@bot.message_handler(regexp=BotRegexps.UNFOLLOW_CHARACTER.pattern)
@handle_character_not_found
def bot_regexp_unfollow_character(message: Message) -> None:
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
def bot_regexp_character_talents(message: Message) -> None:
    talents_dict = BotRegexps.parse_character_talents_message(message.text)
    character_name, _ = BotRegexps.parse_follow_message(message.reply_to_message.text)
    character = Character.objects.get(name=character_name)
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    user_character, _ = UserCharacter.objects.update_or_create(user=user, character=character, defaults=talents_dict)
    bot.send_message(
        user.chat_id,
        BotMessages.SUCCESSFULLY_UPDATED_CHARACTER_TALENTS.format(
            name=BotMessages.format_user_character(user_character)
        ),
    )


@bot.callback_query_handler(func=BotCallbackCommands.SUBSCRIBE_DAILY.as_func())
@bot.callback_query_handler(func=BotCallbackCommands.UNSUBSCRIBE_DAILY.as_func())
def bot_callback_daily_subscription(callback: CallbackQuery) -> None:
    user, _ = User.objects.get_or_create(chat_id=callback.message.chat.id)
    user.is_subscribed = not user.is_subscribed
    user.save(update_fields=["is_subscribed"])
    keyboard = BotKeyboards.create_inline_change_daily_subscription_keyboard(user)
    bot.edit_message_reply_markup(user.chat_id, callback.message.id, reply_markup=keyboard)
