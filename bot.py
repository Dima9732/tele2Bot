import config
import telebot
import requests
import json

bot = telebot.TeleBot(config.token)

class Client():
    msisdn = None
    Token = None

client = Client()
host = "http://tele2-hackday-2017.herokuapp.com/api/"
@bot.message_handler(commands=["start"]) #реагирование на начало
def start(message):
    bot.send_message(message.chat.id, "Введите телефон в формате: /tel 7903......")

@bot.message_handler(commands=["tel"])
def tel(message):
    if len(message.text[5:]) == 11 and message.text[5:].isdigit():
        client.msisdn = message.text[5:]
        bot.send_message(message.chat.id, "А теперь парольное слово /pas .......")
    else:
        bot.send_message(message.chat.id, "Неправильный номер((")

@bot.message_handler(commands=["pas"])
def pas(message):
    headers = {'accept': 'application/json', 'X-API-Token':message.text[5:]}
    r = requests.get(host + "subscribers/" + client.msisdn + "/balance", headers=headers)
    inf = json.loads(r.text)
    if r.status_code == 200:
        client.Token = message.text[5:]
        mes = "Вы успешно авторизировались!) \nВаш баланс: {} \nВаши остатки по пакетам: \n\tсмс: {} \n\tинтернет: {} \n\tминуты: {}\n".format(inf["data"]["money"],
                                                                                                                                         inf["data"]["sms"],
                                                                                                                                         inf["data"]["internet"],
                                                                                                                                         inf["data"]["call"])
        bot.send_message(message.chat.id, mes)
    else:
        bot.send_message(message.chat.id, "Неправильный пароль(( " + message.text[5:])

if __name__ == '__main__':
    bot.polling(none_stop=True)