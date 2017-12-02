import config
import telebot

bot = telebot.TeleBot(config.token)

@bot.message_handler(func=lambda message: True, content_types=["text"]) #реагирование на сообщение от юзера 'text'
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)