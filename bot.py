import config
import telebot

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=["start"]) #реагирование на начало
def start(message):
    bot.send_message(message.chat.id, "Введите телефон в формате: /tel 7903......")

@bot.message_handler(commands=["tel"]) #реагирование на начало
def tel(message):
    msisdn = message.text
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)