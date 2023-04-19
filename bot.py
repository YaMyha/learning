import telebot
import config

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands = ['start'])
def welcome(message):
    sti = open('C:/Users/Professional/Desktop/Python/KeenUpClose.webp','rb')
    bot.send_sticker(message.chat.id, sti)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Пицца")
    item2 = types.KeyboardButton("Газировка")
    
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Садимся на корабль типа \"БеконФасоль\", {0.first_name}!\nЯ - <b>Билли Блэйз</b>".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)
    
@bot.message_handler(content_types = ['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'Пицца':
             bot.send_message(message.chat.id, 'Поехали!')
        elif message.text == 'Газировка':
             bot.send_message(message.chat.id, 'Надо подзаправиться...')
        else:
            bot.send_message(message.chat.id, 'Не понимаю...бип-бип')
    
bot.polling(none_stop = True) 