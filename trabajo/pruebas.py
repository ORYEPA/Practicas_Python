import telebot
from telebot import types
bot = telebot.TeleBot('6428167880:AAF6nnf_Dl-A_yz8-q-gbwDoOkv1LOaZcuI')
# Using the ReplyKeyboardMarkup class
# It's constructor can take the following optional arguments:
# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup()
    itembtnd = types.KeyboardButton('Funciona')
    itembtne = types.KeyboardButton('No Funciona')
    markup.row(itembtnd, itembtne)
    bot.send_message(message.chat.id, "Correcto,revise el sensor de la puerta del piloto:", reply_markup=markup)




# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
