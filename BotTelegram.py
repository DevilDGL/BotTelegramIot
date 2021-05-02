import json
import numpy as np
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


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f"Hola {message.from_user.first_name}")


@bot.message_handler(commands=['led'])
def send_welcome(message):
    ser.write(bytes("l".encode('ascii')))
    global encendido
    if not(encendido):
        bot.reply_to(message, "Led encendido")
        encendido = True
    else:
        bot.reply_to(message, "Led apagado")
        encendido = False


@bot.message_handler(commands=['temperatura'])
def send_welcome(message):
    ser.write(bytes("t".encode('ascii')))
    time.sleep(1)
    if ser.inWaiting() > 0:
        pico_data = ser.readline()
        pico_data = pico_data.decode("utf-8","ignore")
    bot.reply_to(message, f"la temperatura es de {pico_data[:-2]}")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    txt = ""
    for i, j in zip(comandos.keys(),comandos.values()):
        txt += "- */" + i + "*: " + j + "\n"
    bot.reply_to(message, f"Los comandos disponibles son:\n{txt}")


@bot.message_handler(commands=['r'])
def send_welcome(message):
    a = re.search(r"[0-9]+d[0-9]+",message.text)
    txt = message.text[a.span()[0]:a.span()[1]] if a != None else False
    if not txt:
        bot.reply_to(
            message,
            f"Error en el comando, deberia tener la forma:\n/r <Numero de dados>d<Numero de caras>\nEjemplo:\n/r 3d6" 
        )
        exit()
    n1, n2 = txt.split("d")
    tiradas = sorted(np.random.randint(1, int(n2)+1, size=int(n1)), reverse=True)
    salida = "La tirada ha sido:\n" + str(tiradas)[1:-1] + "\nY su suma es:\n" + str(sum(tiradas))
    bot.reply_to(message, salida)


if __name__ == '__main__':
    print("Starting polling")
    bot.polling()
