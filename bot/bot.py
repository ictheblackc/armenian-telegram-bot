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
    """Ask for the translation of a random word."""
    random_word = db.get_random_word()
    text = 'Что означает слово '+random_word[0]+'?'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, check_random_word, random_word)


def check_random_word(message, random_word):
    """Check the translation of a random word."""
    if message.text == random_word[1]:
        text = 'Правильно'
    else:
        text = 'Нет, это не '+message.text+', а '+random_word[1]
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['insert_word'])
def command_insert_word(message):
    """Command handler for adding a new word."""
    text = 'Введите новое слово и его перевод через дефис'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, insert_word)


def insert_word(message):
    """Add new word to dictionary."""
    word_and_translation = message.text.split('-')
    word = word_and_translation[0]
    translation = word_and_translation[1]
    db.insert_word(word, translation)
    text = 'Слово '+word+' успешно добавлено'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['start_test'])
def command_start_test(message):
    """."""
    random_words = db.get_random_words()
    text = ''
    for random_word in random_words:
        text += random_word[0]+'\n'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, check_test, random_words)


def check_test(message, random_words):
    """."""
    answers = message.text.split('\n')
    wrong_answers = []
    i = 0
    for word in random_words:
        if not word[1] == answers[i]:
            print('check '+word[1]+' and '+answers[i])
            wrong_answers.append(word[0]+' - '+word[1])
        i += 1
    score = str(len(random_words) - len(wrong_answers))+'/'+str(len(random_words))
    if len(wrong_answers) == 0:
        text = 'Ошибок нет\n\nОценка '+score
    else:
        text = 'Ошибок '+str(len(wrong_answers))+'\n\nОценка '+score+'\n\n'
        text += 'Вот правильные ответы:\n\n'
        for wrong_answer in wrong_answers:
            print(wrong_answer)
            text += wrong_answer+'\n'

    bot.send_message(message.chat.id, text)
