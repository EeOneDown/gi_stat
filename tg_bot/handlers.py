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
@bot.message_handler(func=BotTextCommands.BACK.as_func())
def bot_command_start(message: Message) -> None:
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    bot.send_message(user.chat_id, BotMessages.START, reply_markup=BotKeyboards.MAIN_MENU)


@bot.message_handler(func=BotTextCommands.TODAY.as_func())
def bot_text_command_today(message: Message) -> None:
    days = Days.get_by_weekday(timezone.now().weekday())
    user_characters = UserCharacter.get_for_today(message.chat.id, days)
    text = BotMessages.create_today_message(user_characters)
    bot.send_message(message.chat.id, text, reply_markup=BotKeyboards.INLINE_SHOW_ALL_TODAY)


@bot.message_handler(func=BotTextCommands.WEEK.as_func())
def bot_text_command_week(message: Message) -> None:
    user_characters = UserCharacter.get_for_week(message.chat.id)
    text = BotMessages.create_week_message(user_characters)
    bot.send_message(message.chat.id, text, reply_markup=BotKeyboards.INLINE_SHOW_ALL_WEEK)


@bot.message_handler(func=BotTextCommands.WEEKLY_BOSSES.as_func())
def bot_text_command_weekly_bosses(message: Message) -> None:
    user_characters = UserCharacter.get_for_weekly_bosses(message.chat.id)
    text = BotMessages.create_weekly_bosses_message(user_characters)
    bot.send_message(message.chat.id, text, reply_markup=BotKeyboards.INLINE_SHOW_ALL_WEEKLY_BOSSES)


@bot.message_handler(func=BotTextCommands.DAILY_SUBSCRIPTION.as_func())
def bot_text_command_daily_subscription(message: Message) -> None:
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    keyboard = BotKeyboards.create_inline_change_daily_subscription_keyboard(user)
    bot.send_message(user.chat_id, BotMessages.DAILY_SUBSCRIPTION, reply_markup=keyboard)


@bot.message_handler(func=BotTextCommands.MANAGE_CHARACTERS.as_func())
@bot.message_handler(func=BotTextCommands.CANCEL.as_func())
def bot_text_command_manage_characters(message: Message) -> None:
    bot.send_message(message.chat.id, BotMessages.MANAGE_CHARACTERS, reply_markup=BotKeyboards.MANAGE_CHARACTERS)


@bot.message_handler(func=BotTextCommands.CHARACTER_LIST.as_func())
def bot_text_command_character_list(message: Message) -> None:
    user_characters = (
        UserCharacter.objects.filter(user__chat_id=message.chat.id)
        .select_related("character")
        .order_by("character__name")
        .all()
    )
    bot.send_message(message.chat.id, BotMessages.create_character_list_message(user_characters))


@bot.message_handler(func=BotTextCommands.FOLLOW_CHARACTERS.as_func())
def bot_text_command_follow_characters(message: Message) -> None:
    characters = Character.objects.exclude(users__chat_id=message.chat.id).order_by("-release_date").all()
    keyboard = BotKeyboards.create_follow_characters_keyboard(characters)
    bot.send_message(message.chat.id, BotMessages.FOLLOW_CHARACTERS, reply_markup=keyboard)


@bot.message_handler(func=BotTextCommands.CHARACTER_TALENTS_INSTRUCTION.as_func())
def bot_text_command_character_talents_instruction(message: Message) -> None:
    bot.send_message(message.chat.id, BotMessages.CHARACTER_TALENTS_INSTRUCTION)


@bot.message_handler(func=BotTextCommands.UNFOLLOW_CHARACTERS.as_func())
def bot_text_command_unfollow_characters(message: Message) -> None:
    characters = Character.objects.filter(users__chat_id=message.chat.id).order_by("-release_date").all()
    keyboard = BotKeyboards.create_unfollow_characters_keyboard(characters)
    bot.send_message(message.chat.id, BotMessages.UNFOLLOW_CHARACTERS, reply_markup=keyboard)


@bot.message_handler(func=BotTextCommands.UNFOLLOW_ALL_CHARACTERS.as_func())
def bot_text_command_unfollow_all_characters(message: Message) -> None:
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    user.characters.clear()

    text = BotMessages.SUCCESSFULLY_UNFOLLOW_ALL_CHARACTERS
    bot.send_message(user.chat_id, text, reply_markup=BotKeyboards.MANAGE_CHARACTERS)


@bot.message_handler(regexp=BotRegexps.FOLLOW_CHARACTER.pattern)
@handle_character_not_found
def bot_regexp_follow_character(message: Message) -> None:
    character_name, talents_dict = BotRegexps.parse_follow_message(message.text)

    character = Character.objects.get(name=character_name)
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    user_character, _ = UserCharacter.objects.update_or_create(user=user, character=character, defaults=talents_dict)

    text = BotMessages.create_successfully_follow_character_message(user_character)
    bot.send_message(user.chat_id, text, reply_markup=BotKeyboards.MANAGE_CHARACTERS)


@bot.message_handler(regexp=BotRegexps.UNFOLLOW_CHARACTER.pattern)
@handle_character_not_found
def bot_regexp_unfollow_character(message: Message) -> None:
    character_name = BotRegexps.parse_unfollow_message(message.text)

    character = Character.objects.get(name=character_name)
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    user.characters.remove(character)

    text = BotMessages.create_successfully_unfollow_character_message(character)
    bot.send_message(user.chat_id, text, reply_markup=BotKeyboards.MANAGE_CHARACTERS)


@bot.message_handler(
    # new talents
    regexp=BotRegexps.CHARACTER_TALENTS.pattern,
    # replies to added character
    func=lambda message: (
        message.reply_to_message
        and message.from_user.id == message.reply_to_message.from_user.id
        and BotRegexps.FOLLOW_CHARACTER.match(message.reply_to_message.text)
    ),
)
@handle_character_not_found
def bot_regexp_character_talents(message: Message) -> None:
    talents_dict = BotRegexps.parse_character_talents_message(message.text)
    character_name, _ = BotRegexps.parse_follow_message(message.reply_to_message.text)

    character = Character.objects.get(name=character_name)
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    user_character, _ = UserCharacter.objects.update_or_create(user=user, character=character, defaults=talents_dict)

    bot.send_message(user.chat_id, BotMessages.create_successfully_updated_character_talents_message(user_character))


@bot.callback_query_handler(func=BotCallbackCommands.SUBSCRIBE_DAILY.as_func())
@bot.callback_query_handler(func=BotCallbackCommands.UNSUBSCRIBE_DAILY.as_func())
def bot_callback_daily_subscription(callback: CallbackQuery) -> None:
    user, _ = User.objects.get_or_create(chat_id=callback.message.chat.id)
    user.is_subscribed = not user.is_subscribed
    user.save(update_fields=["is_subscribed"])

    keyboard = BotKeyboards.create_inline_change_daily_subscription_keyboard(user)
    bot.edit_message_reply_markup(user.chat_id, callback.message.id, reply_markup=keyboard)


@bot.callback_query_handler(func=BotCallbackCommands.SHOW_ALL_TODAY.as_func())
def bot_callback_show_all_today(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.id, reply_markup=None)
    days = Days.get_by_weekday(timezone.now().weekday())
    characters = Character.get_for_today(days)
    bot.send_message(callback.message.chat.id, BotMessages.create_all_today_message(characters))


@bot.callback_query_handler(func=BotCallbackCommands.SHOW_ALL_WEEK.as_func())
def bot_callback_show_all_week(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.id, reply_markup=None)
    characters = Character.get_for_week()
    bot.send_message(callback.message.chat.id, BotMessages.create_all_week_message(characters))


@bot.callback_query_handler(func=BotCallbackCommands.SHOW_ALL_WEEKLY_BOSSES.as_func())
def bot_callback_show_all_weekly_bosses(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.id, reply_markup=None)
    characters = Character.get_for_weekly_bosses()
    bot.send_message(callback.message.chat.id, BotMessages.create_all_weekly_bosses_message(characters))
