from bs4 import BeautifulSoup
import requests
import telebot
import time
from telebot import types

bot_token = '6943956480:AAHhHUWlsqA9L0aEjowQPqcjkmFvBEUrjik'
chat_id = '5375662513'
def parse():
    url = 'https://ru.myfin.by/currency/usd/omsk'
    page = requests.get(url)
    print (page.status_code)
    soup = BeautifulSoup(page.text, "html.parser")
    block = soup.findAll('div',class_='currency-rates-tile header__сurrency-rate header__сurrency-rate--cb')
    description = ''
    for data in block:
        if data.find('a'):
            description = data.text
        description = description [21:28]
    float_number = float(description)
    print(float_number)
    return float_number
def bot():
    bot = telebot.TeleBot(bot_token)
    @bot.message_handler(commands = ['start'])
    def start_message(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Задать верхнюю границу")
        button2 = types.KeyboardButton("Задать нижнюю границу")
        markup.add(button1,button2)
        bot.send_message(message.chat.id,text="Задайте нужные границы на курс доллара".format(message.from_user),reply_markup=markup)
    @bot.message_handler(content_types=['text'])
    def func(message):
        if message.text == "Задать верхнюю границу":
            msg = bot.send_message(message.chat.id, text="Напишите циферку для верхней границы")
            bot.register_next_step_handler(msg, after_text_1)
        elif message.text == "Задать нижнюю границу":
            msg = bot.send_message(message.chat.id, text="Напишите циферку для нижней границы")
            lower_barrier = message.text
            bot.register_next_step_handler(msg, after_text_2)
        elif message.text == "Вернуться в главное меню":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("Задать верхнюю границу")
            button2 = types.KeyboardButton("Задать нижнюю границу")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(button1, button2, back)
            bot.send_message(message.chat.id, text="Вы вернулись в главное меню".format(message.from_user), reply_markup=markup)

    def check_number(barrier):
        try:
            float(barrier)
            return True
        except ValueError:
            return False

    def after_text_1(message):
        upper_barrier = message.text
        if check_number(upper_barrier):
            upper_barrier = float(upper_barrier)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Сбросить значения")
            markup.add(back)
            bot.send_message(message.chat.id, text=f'Значение {upper_barrier} установлено'.format(message.from_user), reply_markup=markup)
            check_upper(upper_barrier)
            if message.text == "Сбросить значения": start_message(message)
        else:
            bot.send_message(message.chat.id, text="Это не циферка")
            start_message(message)

    def after_text_2(message):
        lower_barrier = message.text
        if check_number(lower_barrier):
            lower_barrier = float(lower_barrier)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Сбросить значения")
            markup.add(back)
            bot.send_message(message.chat.id, text=f'Значение {lower_barrier} установлено'.format(message.from_user),reply_markup=markup)
            check_lower(lower_barrier)
        else:
            bot.send_message(message.chat.id, text="Это не циферка")
            start_message(message)

    def frequency(message):
        bot.send_message(message.chat.id, text="Как часто отправлять вам уведомления? Введите кол-во секунд")
        frequency_val = int(message.text)
        return frequency_val
    def check_lower(lower_barrier):
        frequency_val = frequency(message)
        while True:
            new_value = parse()
            if new_value < lower_barrier:
                notification_message = f'Курс доллара к рублю упал ниже установленной границы. Текущее значение: {new_value}'
                bot.send_message(chat_id, notification_message)
                time.sleep(frequency_val)

    def check_upper(upper_barrier):
        frequency_val = frequency(message)
        while True:
            new_value = parse()
            if new_value > upper_barrier:
                message = f'Курс доллара к рублю поднялся выше установленной границы. Текущее значение: {new_value}'
                bot.send_message(chat_id, message)
                time.sleep(frequency_val)

    bot.infinity_polling()

parse()
bot()