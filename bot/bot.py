from telebot import TeleBot
from .config import Config as conf
from .modules.database import Database
from .modules.message import Message


bot = TeleBot(conf.BOT_TOKEN)
db = Database(conf.DB_NAME)
messages = Message()
db.create_db()


@bot.message_handler(commands=['start'])
def command_start(message):
    """Start work after starting the bot."""
    # Get user info
    user_id = message.from_user.id
    is_bot = message.from_user.is_bot
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    language_code = message.from_user.language_code
    is_premium = message.from_user.is_premium
    # Insert user into db
    db.insert_user(
        user_id=user_id,
        is_bot=is_bot,
        first_name=first_name,
        last_name=last_name,
        username=username,
        language_code=language_code,
        is_premium=is_premium,
    )
    text = messages.start
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['random_word'])
def command_random_word(message):
    """."""
    random_word = db.get_random_word()
    text = 'Что означает слово '+random_word[0]+'?'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, check_random_word, random_word)


def check_random_word(message, random_word):
    if message.text == random_word[1]:
        text = 'Правильно'
    else:
        text = 'Нет, это не '+message.text+', а '+random_word[1]
    bot.send_message(message.chat.id, text)
