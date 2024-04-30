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

    def reset_values():
        global upper_barrier, frequency_checked, lower_barrier
        upper_barrier = None
        frequency_checked = None
        lower_barrier = None

    @bot.message_handler(commands = ['start'])
    def start_message(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Задать верхнюю границу")
        button2 = types.KeyboardButton("Задать нижнюю границу")
        markup.add(button1,button2)
        bot.send_message(message.chat.id,text="Задайте нужные границы на курс доллара".format(message.from_user),reply_markup=markup)

    @bot.message_handler(regexp='Сбросить значение')
    def back(message):
        bot.send_message(message.chat.id, text="Значение сброшено. Напишите /start для перехода в начало")
        reset_values()
    @bot.message_handler(content_types=['text'])
    def func(message):
        if message.text == "Задать верхнюю границу":
            msg = bot.send_message(message.chat.id, text="Напишите циферку для верхней границы")
            bot.register_next_step_handler(msg, after_text_1)
        elif message.text == "Задать нижнюю границу":
            msg = bot.send_message(message.chat.id, text="Напишите циферку для нижней границы")
            bot.register_next_step_handler(msg, after_text_2)

    def check_number(barrier):
        try:
            float(barrier)
            return True
        except ValueError:
            return False


    def after_text_1(message):
        global upper_barrier
        upper_barrier = message.text
        if check_number(upper_barrier):
            upper_barrier = float(upper_barrier)
            bot.send_message(message.chat.id, text=f'Значение {upper_barrier} установлено'.format(message.from_user))
            msg = bot.send_message(message.chat.id, text='Как часто отправлять вам уведомления? Напишите кол-во секунд')
            bot.register_next_step_handler(msg, frequency_upper)
        else:
            bot.send_message(message.chat.id, text="Это не циферка")
            start_message(message)

    def frequency_upper(message):
        frequency_val = message.text
        check_number (frequency_val)
        if check_number(frequency_val):
            global frequency_checked
            frequency_checked = float(frequency_val)
            msg = bot.send_message(message.chat.id, text=f'Отлично, раз в {frequency_checked} секунд отправлю вам уведомление. Напишите "+" для начала отправки'.format(message.from_user))
            bot.register_next_step_handler(msg,check_upper)
        else:
            bot.send_message(message.chat.id, text="Это не циферка")
            after_text_1(message)
    def after_text_2(message):
        global lower_barrier
        lower_barrier = message.text
        if check_number(lower_barrier):
            lower_barrier = float(lower_barrier)
            bot.send_message(message.chat.id, text=f'Значение {lower_barrier} установлено'.format(message.from_user))
            msg = bot.send_message(message.chat.id, text='Как часто отправлять вам уведомления? Напишите кол-во секунд')
            bot.register_next_step_handler(msg, frequency_lower)
        else:
            bot.send_message(message.chat.id, text="Это не циферка")
            start_message(message)

    def frequency_lower(message):
        frequency_val = message.text
        check_number (frequency_val)
        if check_number(frequency_val):
            global frequency_checked
            frequency_checked = float(frequency_val)
            msg = bot.send_message(message.chat.id, text=f'Отлично, раз в {frequency_checked} секунд отправлю вам уведомление. Напишите "+" для начала отправки'.format(message.from_user))
            bot.register_next_step_handler(msg, check_lower)
        else:
            bot.send_message(message.chat.id, text="Это не циферка")
            after_text_2(message)

    def check_lower(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Сбросить значение")
        markup.add(button1)
        bot.send_message(message.chat.id, text="Подсказка: для сброса значения вы всегда можете нажать на кнопку ;)",reply_markup=markup)
        while True:
            new_value = parse()
            if new_value < lower_barrier:
                message = f'Курс доллара к рублю упал ниже установленной границы. Текущее значение: {new_value}'
                bot.send_message(chat_id, message)
                time.sleep(frequency_checked)


    def check_upper(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Сбросить значение")
        markup.add(button1)
        bot.send_message(message.chat.id, text="Подсказка: для сброса значения вы всегда можете нажать на кнопку ;)", reply_markup=markup)
        while True:
            new_value = parse()
            if new_value > upper_barrier:
                message = f'Курс доллара к рублю поднялся выше установленной границы. Текущее значение: {new_value}'
                bot.send_message(chat_id, message)
                time.sleep(frequency_checked)

    bot.infinity_polling()

parse()
bot()