import telebot
import database_editing1 as Act
import datetime as timeAmout
from datetime import datetime as time
import json

with open('Database.json', 'r', encoding='utf-8') as openfile:
    # Reading from json file
    json_object = json.load(openfile)
data = dict(json_object)


def saveJson():
    with open('Database.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def openJson():
    global data
    with open('Database.json', 'r', encoding='utf-8') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
    data = dict(json_object)


while True:
    try:
        openJson()
    except:
        print("Обновление БД...")
        continue
    for x in data["Deadlines"]:
        if time.now().strftime("%d.%m.%Y") == x["expDate"] and time.now().strftime("%H:%M:%S") == "12:00:00":
            bot = telebot.TeleBot('1724637364:AAEPqLLPkSfd788vqvneH_dusnBVL5pd2mM')
            mes = bot.send_message(x["userId"], "ВАЖНО!! ТВОЙ ДЕДЛАЙН " + x["name"] + " ЗАКОНЧИТСЯ СЕГОДНЯ!!!")
            assert mes
        elif time.now().strftime("%d.%m.%Y") == x["expDate"] and time.now().strftime("%H:%M:%S") == "23:00:00":
            bot = telebot.TeleBot('1724637364:AAEPqLLPkSfd788vqvneH_dusnBVL5pd2mM')
            mes = bot.send_message(x["userId"], "ТВОЙ ДЕДЛАЙН " + x["name"] + " ЗАКОНЧИЛСЯ СЕГОДНЯ!!!")
            data = Act.delete_exp_deadline(x["name"], data)
            assert mes
        if time.now().strftime("%H:%M:%S") == x["alarmTime"] and\
                time.now().strftime("%d.%m.%Y") == x["lastNotificationDate"]:
            bot = telebot.TeleBot('1724637364:AAEPqLLPkSfd788vqvneH_dusnBVL5pd2mM')
            mes = bot.send_message(x["userId"], "НАПОМИНАЮ!! ТВОЙ ДЕДЛАЙН \"" + x["name"] + "\" ЗАКОНЧИТСЯ " +
                                   x["expDate"] + " И ОН ВСЕ ЕЩЕ НЕ ЗАВЕРШЕН!!")
            x["lastNotificationDate"] = (time.now() + timeAmout.timedelta(days=1)).strftime("%d.%m.%Y")
            saveJson()
            assert mes
