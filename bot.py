import config
import telebot
import requests
import json
from utils import generate_markup
from dbworker import *

bot = telebot.TeleBot(config.token)

host = "http://tele2-hackday-2017.herokuapp.com/api/"
@bot.message_handler(commands=["start"]) #реагирование на начало
def start(message):
    bot.send_message(message.chat.id, "Вас приветствует Телебот!) \nВыберите, что хотите сделать?)\n1)Залогиниться 2)Узнать, все обо мне)")
    set_state(message.chat.id, config.States.S_START.value)

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == config.States.S_START.value)
def user_takes_decision(message):
    print(message.text.find('логин'))
    if message.text.find('логин') + 1 or message.text.find("1 ") + 1:
        bot.send_message(message.chat.id, "Вы выбрали пункт залогиниться. Теперь введите телефон")
        set_state(message.chat.id, config.States.S_ENTER_TEL.value)
    elif message.text.find('Обо мне') + 1 or message.text.find("2") + 1:
        bot.send_message(message.chat.id, "Я бот команды Hahaton Team. Меня писали люди, кт хотят повеситься(((")
    else :
        bot.send_message(message.chat.id, "Я не могу разобрать, что Вы сказали(((")

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == config.States.S_ENTER_TEL.value)
def user_entering_tel(message):
    if len(message.text) == 11 and message.text.isdigit():
        set_msisdn(message.chat.id, message.text)
        bot.send_message(message.chat.id, "Отличный телефон! \nА теперь парольное слово")
        set_state(message.chat.id, config.States.S_ENTER_PAS.value)
    else:
        bot.send_message(message.chat.id, "Неправильный номер((")

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == config.States.S_ENTER_PAS.value)
def pas(message):
    headers = {'accept': 'application/json', 'X-API-Token':message.text}
    r = requests.get(host + "subscribers/" + get_msisdn(message.chat.id) + "/balance", headers=headers)
    inf = json.loads(r.text)
    if r.status_code == 200:
        set_token(message.chat.id, message.text)
        mes = "Вы успешно авторизировались!) \nВаш баланс: {} \nВаши остатки по пакетам: \n\tсмс: {} \n\tинтернет: {} \n\tминуты: {}\nЧто вы хотите сделать?".format(inf["data"]["money"],
                                                                                                                                         inf["data"]["sms"],
                                                                                                                                         inf["data"]["internet"],
                                                                                                                                 inf["data"]["call"])
        markup = generate_markup("Profile.txt")
        bot.send_message(message.chat.id, mes, reply_markup=markup)
        set_state(message.chat.id, config.States.S_PROFILE.value)
    else:
        bot.send_message(message.chat.id, "Неправильный пароль(( ")

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == config.States.S_PROFILE.value)
def profile(message):
    keyboard_hider = telebot.types.ReplyKeyboardRemove()
    if message.text == "Выйти":
        set_state(message.chat.id, config.States.S_START.value)
        bot.send_message(message.chat.id, 'Я буду скучать( \nНо вы можете еще раз 1) Залогиниться или 2) Узнать обо мне', reply_markup=keyboard_hider)
    elif message.text.find("тариф") + 1:
        bot.send_message(message.chat.id, 'Вы хотите узнать что-то про тарифы?', reply_markup=keyboard_hider)

if __name__ == '__main__':
    bot.polling(none_stop=True)