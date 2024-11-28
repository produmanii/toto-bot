import telebot
from telebot import types

# Замените 'YOUR_TOKEN_HERE' на токен, который вы получили от BotFather
bot = telebot.TeleBot('7625412447:AAEkzfmO_qmKD8UhvuN42tQOcflnf9RHuNU')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Как вас зовут?")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_name = message.text
    bot.send_message(message.chat.id, f"Приятно познакомиться, {user_name}! Теперь введите ваш номер телефона.")
    bot.register_next_step_handler(message, get_phone, user_name)

def get_phone(message, user_name):
    user_phone = message.text
    bot.send_message(message.chat.id, "Введите ваше сообщение (не обязательно):")
    bot.register_next_step_handler(message, get_message, user_name, user_phone)

def get_message(message, user_name, user_phone):
    user_message = message.text
    bot.send_message(message.chat.id, "Загрузите файл (не обязательно):")
    bot.register_next_step_handler(message, get_file, user_name, user_phone, user_message)

def get_file(message, user_name, user_phone, user_message):
    if message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
        bot.send_message(message.chat.id, "Файл успешно загружен.")
    else:
        file_url = None
        bot.send_message(message.chat.id, "Файл не загружен.")

    # Здесь вы можете сохранить данные в базу данных или отправить их на ваш сервер
    bot.send_message(message.chat.id, "В ближайшее время с Вами свяжутся!")

    # Пример вывода данных
    print(f"Имя: {user_name}")
    print(f"Телефон: {user_phone}")
    print(f"Сообщение: {user_message}")
    print(f"Файл: {file_url}")

bot.polling()