# -*- coding: utf-8 -*-
#
# This file is part of Zoe Assistant
# Licensed under MIT license - see LICENSE file
#

from telebot import types
from zoe import *

import telebot
import json


@Agent('Tila')
class MailAgent:

    def __init__(self):
        self.bot = telebot.TeleBot(json.loads(open("config.json").read())['token'], parse_mode='Markdown')
        self.bot.polling()

    @Intent("tila.read")
    def send_to_chat(self, intent):
        """ Expected intent
            {
                "intent": "tila.read",
                "chat": "chat id"
                "messsage": "message to send to the telegram chat"
            }
        """
        self.bot.send_message(intent['chat'], intent['message'])

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(self, message):
        markup = types.ReplyKeyboardMarkup()
        led_but = types.InlineKeyboardButton('/led')
        temp_but = types.InlineKeyboardButton('/temperature')
        markup.row(led_but, temp_but)
        self.bot.reply_to(message, f"Hola {message.from_user.first_name}", reply_markup=markup)

    @bot.message_handler(commands=['led'])
    def led_options(self, message):
        """ Show commands related to the leds
        """
        markup = types.ReplyKeyboardMarkup()
        led_status = types.InlineKeyboardButton('/get-led-status')
        led_on = types.InlineKeyboardButton('/turn-on-led')
        led_off = types.InlineKeyboardButton('/turn-off-led')
        markup.row(led_status)
        markup.row(led_on, led_off)
        self.bot.reply_to(message, "¿Encender o apagar?", reply_markup=markup)


    @bot.message_handler(commands=['turn-led-on'])
    def turn_on_led(self, message):
        """ Send to the pico-agent to turn on the led
        """
        self.bot.reply_to(message, "Led encendido")
        self._listener.send(json.dumps(
            {"intent": "pico.led", "led": True, "chat": message.chat.id}
        ))

    @bot.message_handler(commands=['turn-led-off'])
    def turn_on_led(self, message):
        """ Send to the pico-agent to turn off the led
        """
        self.bot.reply_to(message, "Led apagado")
        self._listener.send(json.dumps(
            {"intent": "pico.led", "led": False, "chat": message.chat.id}
        ))

    @bot.message_handler(commands=['led-status'])
    def turn_on_led(self, message):
        """ Request to the pico-agent the status of the led
        """
        self.bot.reply_to(message, "Led encendido")
        self._listener.send(json.dumps(
            {"intent": "pico.led", "led": True, "chat": message.chat.id}
        ))

    @bot.message_handler(commands=['temperature'])
    def get_temp(self, message):
        """ Request to the pico-agent the current temperature
        """
        self.bot.reply_to(message, "Requesting temperature")
        self._listener.send(json.dumps(
            {"intent": "pico.get_temp", "chat": message.chat.id}
        ))
