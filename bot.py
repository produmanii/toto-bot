import telebot

import telebot
from telebot import types

# Замените 'YOUR_TOKEN_HERE' на токен, который вы получили от BotFather
bot = telebot.TeleBot('7625412447:AAEkzfmO_qmKD8UhvuN42tQOcflnf9RHuNU')

# Удаление вебхука
bot.remove_webhook()

# Словарь для хранения состояния пользователей
user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_states[chat_id] = 'waiting_for_name'
    bot.send_message(chat_id, "Добро пожаловать! Как вас зовут?")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_name')
def get_name(message):
    chat_id = message.chat.id
    user_name = message.text
    user_states[chat_id] = 'waiting_for_phone'
    bot.send_message(chat_id, f"Приятно познакомиться, {user_name}! Теперь введите ваш номер телефона.")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_phone')
def get_phone(message):
    chat_id = message.chat.id
    user_phone = message.text
    user_states[chat_id] = 'waiting_for_message'
    bot.send_message(chat_id, "Введите ваше сообщение (не обязательно):")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_message')
def get_message(message):
    chat_id = message.chat.id
    user_message = message.text
    user_states[chat_id] = 'waiting_for_file'
    bot.send_message(chat_id, "Загрузите файл (не обязательно):")

@bot.message_handler(content_types=['document'], func=lambda message: user_states.get(message.chat.id) == 'waiting_for_file')
def get_file(message):
    chat_id = message.chat.id
    if message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
        bot.send_message(chat_id, "Файл успешно загружен.")
    else:
        file_url = None
        bot.send_message(chat_id, "Файл не загружен.")

    # Здесь вы можете сохранить данные в базу данных или отправить их на ваш сервер
    bot.send_message(chat_id, "В ближайшее время с Вами свяжутся!")

    # Пример вывода данных
    print(f"Имя: {user_states[chat_id]['name']}")
    print(f"Телефон: {user_states[chat_id]['phone']}")
    print(f"Сообщение: {user_states[chat_id]['message']}")
    print(f"Файл: {file_url}")

    # Очистка состояния пользователя
    del user_states[chat_id]
