import config
import telebot
import requests
import json
from utils import generate_markup
from dbworker import *
from Tele2_methods import Tele2_methods as api
import datetime

bot = telebot.TeleBot(config.token)

host = "http://tele2-hackday-2017.herokuapp.com/api/"
@bot.message_handler(commands=["start"]) #реагирование на начало
def start(message):
    keyboard_hider = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Приветствую тебя, абонент. Мы не знакомы, но ты стоишь на развилке дороги. Есть два пути. \n1.Залогиниться. \n2.Узнать меня поближе.", reply_markup=keyboard_hider)
    set_state(message.chat.id, config.States.S_START.value)

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == config.States.S_START.value)
def user_takes_decision(message):
    print(message.text.find('логин'))
    if message.text.find('логин') + 1 or message.text.find("1") + 1:
        bot.send_message(message.chat.id, "Введи телефонный номер в формате 7 **********. Плюсик можешь оставить себе, сладенький.")

        set_state(message.chat.id, config.States.S_ENTER_TEL.value)
    elif message.text.find('узнать') + 1 or message.text.find("2") + 1:
        bot.send_message(message.chat.id, "Приятно познакомиться, я Телеграм-бот Tele2Bot. Меня создали голодные студенты ВМК МГУ. Без меня твоё путешествие по лабиринту твоих тарифов и платежей было бы невыносимо тяжким. Меня создали не ради тебя, но всё же я тебе помогу в твоём нелёгком пути к познанию баланса своего счёта. Я немногословен.")
    else :
        bot.send_message(message.chat.id, "Я не могу разобрать, что Вы сказали(((")

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == config.States.S_ENTER_TEL.value)
def user_entering_tel(message):
    if len(message.text) == 11 and message.text.isdigit():
        set_msisdn(message.chat.id, message.text)
        bot.send_message(message.chat.id, "Отлично, номер верен, но есть ли ты в списке? Введи пароль:")
        set_state(message.chat.id, config.States.S_ENTER_PAS.value)
    else:
        bot.send_message(message.chat.id, "Извини, но тебе придётся попробовать снова.")

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == config.States.S_ENTER_PAS.value)
def pas(message):
    headers = {'accept': 'application/json', 'X-API-Token':message.text}
    r = requests.get(host + "subscribers/" + get_msisdn(message.chat.id) + "/balance", headers=headers)
    inf = r.json()
    if r.status_code == 200:
        set_token(message.chat.id, message.text)
        mes = "Отлично, ты в списке. Можешь пройти. \nТвой баланс: {} \nТвои остатки по пакетам: \n\tсмс: {} \n\tинтернет: {} \n\tминуты: {}\nЧто ты хочешь узнать?".format(inf["data"]["money"],
                                                                                                                                         inf["data"]["sms"],
                                                                                                                                         inf["data"]["internet"],
                                                                                                                                 inf["data"]["call"])
        markup = generate_markup("Profile.txt")
        bot.send_message(message.chat.id, mes, reply_markup=markup)
        set_state(message.chat.id, config.States.S_PROFILE.value)
    else:
        bot.send_message(message.chat.id, "Извини, но я начинаю подозревать в тебе самозванца...")

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == config.States.S_PROFILE.value)
def profile(message):
    keyboard_hider = telebot.types.ReplyKeyboardRemove()
    if message.text == "Выйти":
        set_state(message.chat.id, config.States.S_START.value)
        bot.send_message(message.chat.id, 'Я буду скучать( \nНо ты можешь еще раз: \n1) Залогиниться \n2) Узнать обо мне', reply_markup=keyboard_hider)
    elif message.text.find("тариф") + 1:
        set_state(message.chat.id, config.States.S_TAXES.value)
        markup = generate_markup("taxes.txt")
        bot.send_message(message.chat.id, 'Ты хочешь посмотреть:', reply_markup=markup)
    elif message.text.find("аккаунт") + 1:
        set_state(message.chat.id, config.States.S_ACCINFO.value)
        markup = generate_markup("accinf.txt")
        mes = api.inform_about_sub(get_msisdn(message.chat.id))
        ms = ""
        for key in mes:
            ms += "{} : {}\n".format(key, mes[key])

        bot.send_message(message.chat.id, ms + '\nТы хочешь посмотреть:', reply_markup=markup)
    elif message.text.find("услуг") + 1:
        set_state(message.chat.id, config.States.S_SERVICES.value)
        markup = generate_markup("services.txt")
        bot.send_message(message.chat.id, 'Ты хочешь посмотреть:', reply_markup=markup)
@bot.message_handler(func=lambda message: message.text.find("Вернуться") + 1 != 0)
def ret_to_prof(message):
    set_state(message.chat.id, config.States.S_PROFILE.value)
    markup = generate_markup("Profile.txt")
    bot.send_message(message.chat.id, "Что ты хочешь узнать?", reply_markup=markup)

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == config.States.S_ACCINFO.value)
def acc_info(message):
    if message.text.find("Платежи") + 1:
        markup = generate_markup("payments.txt")
        set_state(message.chat.id, config.States.S_PAYMENTS.value)
        bot.send_message(message.chat.id, "Хочешь узнать информацию про:", reply_markup=markup)

    if message.text.find("Мой") + 1:
        markup = generate_markup("back.txt")
        set_state(message.chat.id, config.States.S_MY_TAX.value)
        req = api.tariff(get_msisdn(message.chat.id), get_token(message.chat.id))
        mes = "Название : {}\nКоличество смс : {}\nЦена пакета смс : {}\nКоличество минут : {}\nЦена пакета минут :{}\nПакет интернета : {}\nЦена пакета интернета : {}\nПодробнее : {}".format(
            req['name'], req['smsPackageSize'], req['smsPrice'], req['callPackageSize'], req['callPrice'], req['internetPackageSize'], req['internetPrice'], req['url']
        )

        bot.send_message(message.chat.id, mes + "\nЕсли хочешь сменить тариф напиши 'сменить тариф на ...'", reply_markup=markup)

    if message.text.find("Мои") + 1:
        markup = generate_markup("back.txt")
        set_state(message.chat.id, config.States.S_MY_SERVICES.value)
        req = api.getServices(get_msisdn(message.chat.id), get_token(message.chat.id))
        print(req)
        mes = "Подключенные услуги\n"
        for serv in req:
            mes += "название : {} описание : {} цена {}\n".format(serv["name"], serv["description"], serv["subscriptionFee"])
        bot.send_message(message.chat.id, mes + "\nЕсли хочешь отключить услугу напиши 'отключить ...", reply_markup=markup)

    if message.text.find("информац") + 1:
        keyboard_hider = telebot.types.ReplyKeyboardRemove()
        set_state(message.chat.id, config.States.S_CHANGEINFO_ENTERNAME.value)
        bot.send_message(message.chat.id, "Введи имя \n(-, если хочешь оставить без изменений):", reply_markup=keyboard_hider)

inf_user = {"firstName":"DIMA", "middleName":"ANYA", "lastName":"FILL", "email":"HENRY", "keyword":"HAHATONTEAM"}

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == config.States.S_CHANGEINFO_ENTERNAME.value)
def change_name(message):
    if not message.text.find('-') + 1:
        inf_user.update(firstName=message.text)
    set_state(message.chat.id, config.States.S_CHANGEINFO_ENTERMIDNAME.value)
    bot.send_message(message.chat.id, "Я запомнил имя "+ inf_user["firstName"] + ". Введи отчество \n(-, если хочешь оставить без изменений):")

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == config.States.S_CHANGEINFO_ENTERMIDNAME.value)
def change_midname(message):
    if not message.text.find('-') + 1:
        inf_user.update(middleName=message.text)
    set_state(message.chat.id, config.States.S_CHANGEINFO_ENTERLASTNAME.value)
    bot.send_message(message.chat.id, "Я запомнил отчество "+ inf_user["middleName"] + ". Введи фамилию \n(-, если хочешь оставить без изменений):")

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == config.States.S_CHANGEINFO_ENTERLASTNAME.value)
def change_lastname(message):
    if not message.text.find('-') + 1:
        inf_user.update(lastName=message.text)
    set_state(message.chat.id, config.States.S_CHANGEINFO_ENTERMAIL.value)
    bot.send_message(message.chat.id, "Я запомнил фамилию "+ inf_user["lastName"] + ". Введи Твой e-mail \n(-, если хочешь оставить без изменений):")

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == config.States.S_CHANGEINFO_ENTERMAIL.value)
def change_mail(message):
    if not message.text.find('-') + 1:
        inf_user.update(email=message.text)
    set_state(message.chat.id, config.States.S_CHANGEINFO_ENTERKEY.value)
    bot.send_message(message.chat.id, "Я запомнил e-mail "+ inf_user["email"] + ". Введи новый пароль \n(пароль менять обязательно):")

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == config.States.S_CHANGEINFO_ENTERKEY.value)
def change_key(message):
    inf_user.update(keyword=message.text)
    set_state(message.chat.id, config.States.S_PROFILE.value)
    markup = generate_markup("Profile.txt")
    bot.send_message(message.chat.id, "Я запомнил пароль "+ inf_user["keyword"] + ". Данные сохранены", reply_markup=markup)
    api.changeAbonentInfo(get_msisdn(message.chat.id), get_token(message.chat.id), inf_user)

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == config.States.S_PAYMENTS.value)
def payments(message):
    if message.text.find("Бала") + 1:
        req = api.balance(get_msisdn(message.chat.id), get_token(message.chat.id))
        markup = generate_markup("Profile.txt")
        set_state(message.chat.id, config.States.S_PROFILE.value)
        bot.send_message(message.chat.id, "Баланс : " + str(req["money"]), reply_markup=markup)
    if message.text.find("Начисления") + 1:
        tod = datetime.datetime.today()
        mpa = tod.replace(month=1, day=1, microsecond=0)
        tod = tod.replace(microsecond=0)
        req = api.getCharges(get_msisdn(message.chat.id), get_token(message.chat.id), from1=mpa.isoformat(sep="T"), to=tod.isoformat(sep="T"))
        mes = ""
        for date in req[-20:]:
            mes += "дата :{} \nколичество : {} \nчего: {} \nцена: {}\n\n".format(date["date"], date["volume"], date["type"], date["fee"])
        markup = generate_markup("Profile.txt")
        set_state(message.chat.id, config.States.S_PROFILE.value)
        bot.send_message(message.chat.id, "Выписка за месяц: \n" + mes, reply_markup=markup)
    if message.text.find("Выписк") + 1:
        tod = datetime.datetime.today()
        mpa = tod.replace(month=1, day=1, microsecond=0)
        tod = tod.replace(microsecond=0)
        req = api.payment(get_msisdn(message.chat.id), get_token(message.chat.id), mpa.isoformat(sep="T"), tod.isoformat(sep="T"))
        markup = generate_markup("Profile.txt")
        mes = ""
        for date in req:
            mes += "дата :{} \nКоличество пополнения: {}\n\n".format(date["date"], date["value"])
        set_state(message.chat.id, config.States.S_PROFILE.value)
        bot.send_message(message.chat.id, "Недавние платежи\n" + mes, reply_markup=markup)

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == config.States.S_TAXES.value)
def taxes(message):
    if message.text.find("Все") + 1:
        markup = generate_markup("back.txt")
        requ = api.getTariffs()
        mesa = ""
        for req in requ:
            mes = "Название : {}\nКоличество смс : {}\nЦена пакета смс : {}\nКоличество минут : {}\nЦена пакета минут :{}\nПакет интернета : {}\nЦена пакета интернета : {}\nПодробнее : {}\n\n".format(req['name'], req['smsPackageSize'], req['smsPrice'], req['callPackageSize'], req['callPrice'],req['internetPackageSize'], req['internetPrice'], req['url'])
            mesa += mes
        bot.send_message(message.chat.id, mesa, reply_markup=markup)

    if message.text.find("Мой") + 1:
        markup = generate_markup("back.txt")
        set_state(message.chat.id, config.States.S_MY_TAX.value)
        req = api.tariff(get_msisdn(message.chat.id), get_token(message.chat.id))
        mes = "Название : {}\nКоличество смс : {}\nЦена пакета смс : {}\nКоличество минут : {}\nЦена пакета минут :{}\nПакет интернета : {}\nЦена пакета интернета : {}\nПодробнее : {}".format(
            req['name'], req['smsPackageSize'], req['smsPrice'], req['callPackageSize'], req['callPrice'], req['internetPackageSize'], req['internetPrice'], req['url']
        )

        bot.send_message(message.chat.id, mes + "\nЕсли хотите сменить тариф напишите 'сменить тариф на ...'", reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)

