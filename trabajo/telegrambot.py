from telebot import asyncio_filters
from telebot import types

from telebot.async_telebot import AsyncTeleBot

# list of storages, you can use any storage
from telebot.asyncio_storage import StateMemoryStorage

# new feature for states.
from telebot.asyncio_handler_backends import State, StatesGroup
import asyncio

# default state storage is statememorystorage
bot = AsyncTeleBot('6428167880:AAF6nnf_Dl-A_yz8-q-gbwDoOkv1LOaZcuI', state_storage=StateMemoryStorage())


# Just create different statesgroup
class MyStates(StatesGroup):
    email = State()  # statesgroup should contain states
    codigo =State()
    sensor1= State()
    sensor2= State()
    sensor3= State()
    sensor4= State()


@bot.message_handler(commands=['start'])
async def start_ex(message):

    await bot.set_state(message.from_user.id, MyStates.email, message.chat.id)
    await bot.send_message(message.chat.id, 'Hola, escribe tu correo :')



@bot.message_handler(state="*", commands='cancel')
async def any_state(message):

    await bot.send_message(message.chat.id, "Your state was cancelled.")
    await bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=MyStates.email)
async def send_email(message):

    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    await bot.send_message(message.chat.id,
                           "Ingresa el codigo enviado a este correo:\n<b>{email}</b>".format(
                               email=message.text), parse_mode="html")
    await bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=MyStates.codigo)
async def check_code(message):
    markup = types.ReplyKeyboardMarkup()
    itembtnd = types.KeyboardButton('Funciona')
    itembtne = types.KeyboardButton('No Funciona')
    markup.row(itembtnd, itembtne)
    await  bot.send_message(message.chat.id, "Correcto,revise el sensor de la puerta del piloto:", reply_markup=markup)
    await bot.delete_state(message.from_user.id, message.chat.id)



bot.add_custom_filter(asyncio_filters.StateFilter(bot))



asyncio.run(bot.polling())