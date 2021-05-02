from telebot import types

import json
import os
import re
import telebot
import time


bot = telebot.TeleBot(json.loads(open("token.json").read())['token'], parse_mode='Markdown')
comandos = {
    'start': "Saluda al Usuario.",
    'help': 'Emite la lista de comandos.',
    "r <Numero de dados>d<Numero de caras> ": "Tira la cantidad de dados indicada de la cantidad de caras indicada.\nEjemplo:\n/r 3d6",
    "led": "Enciende el led de la pico.",
    "temperatura": "Devuelve ls temperatura leida por la pico."
}

serial_connected = 0
if os.path.exists('COM3') == True:
    import serial
    ser = serial.Serial('COM3', 115200)
    serial_connected = 1
    time.sleep(3)

encendido = False


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup()
    led_but = types.InlineKeyboardButton('/led')
    temp_but = types.InlineKeyboardButton('/temperature')
    markup.row(led_but, temp_but)
    bot.reply_to(message, f"Hola {message.from_user.first_name}", reply_markup=markup)


@bot.message_handler(commands=['led'])
def led_options(message):
    """ Show commands related to the leds
    """
    markup = types.ReplyKeyboardMarkup()
    led_status = types.InlineKeyboardButton('/get-led-status')
    led_on = types.InlineKeyboardButton('/turn-led-on')
    led_off = types.InlineKeyboardButton('/turn-led-off')
    markup.row(led_status)
    markup.row(led_on, led_off)
    bot.reply_to(message, "¿Encender o apagar?", reply_markup=markup)


@bot.message_handler(commands=['turn-led-on'])
def turn_on_led( message):
    """ Send to the pico-agent to turn on the led
    """
    bot.reply_to(message, "Led encendido")


@bot.message_handler(commands=['turn-led-off'])
def turn_on_led( message):
    """ Send to the pico-agent to turn off the led
    """
    bot.reply_to(message, "Led apagado")


@bot.message_handler(commands=['get-led-status'])
def turn_on_led(message):
    """ Request to the pico-agent the status of the led
    """
    bot.reply_to(message, "Led encendido")


@bot.message_handler(commands=['temperature'])
def get_temp(message):
    """ Request to the pico-agent the current temperature
    """
    bot.reply_to(message, "Requesting temperature")


if __name__ == '__main__':
    print("Starting polling")
    bot.polling()
