from bs4 import BeautifulSoup
import requests
import telebot
import time

bot_token = '6943956480:AAHhHUWlsqA9L0aEjowQPqcjkmFvBEUrjik'
chat_id = '5375662513'
def Parse():
    url = 'https://ru.myfin.by/currency/usd/omsk'
    page = requests.get(url)
    print (page.status_code)
    soup = BeautifulSoup(page.text, "html.parser")
    block = soup.findAll('div',class_='currency-rates-tile header__сurrency-rate header__сurrency-rate--cb')
    description = ''
    for data in block:
        if data.find('a'):  # находим тег <p>
            description = data.text # записываем в переменную содержание тега
        description = description [21:28]
    float_number = float(description)
    print(float_number)
    return float_number
def Bot():
    bot = telebot.TeleBot('6943956480:AAHhHUWlsqA9L0aEjowQPqcjkmFvBEUrjik')
    @bot.message_handler(commands = ['start'])
    def main(message):
        bot.send_message(message.chat.id, 'Жди уведомления!')
    bot.polling(non_stop=True)
    while True:
        new_value = Parse()

        if new_value < 92.3891:
            message = f'Курс доллара к рублю упал ниже 92.3891. Текущее значение: {new_value}'
            bot.send_message(chat_id, message)

        if new_value > 92.3893:
            message = f'Курс доллара к рублю поднялся выше 92.3893. Текущее значение: {new_value}'
            bot.send_message(chat_id, message)
        time.sleep(60)
Parse()
Bot()


