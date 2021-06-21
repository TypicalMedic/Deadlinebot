try:
    import telebot
    from datetime import datetime
    import json
    import database_editing1 as act

except ModuleNotFoundError as e:
    with open("Logs.txt", 'w', encoding='utf-8') as logs:
        errMessage = datetime.now().strftime("%d.%m.%Y %H:%M:%S") + " error: " + str(e)
        logs.write(errMessage)
with open("Logs.txt", 'w', encoding='utf-8') as logs:
        errMessage = datetime.now().strftime("%d.%m.%Y %H:%M:%S") + " error: " + str(e)
        logs.write("TestLog")
bot = telebot.TeleBot('1724637364:AAEPqLLPkSfd788vqvneH_dusnBVL5pd2mM')  # коннектимся к нашему боту
users_triggers = dict()

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


for x in data['Users']:
    users_triggers[x['id']] = {'isAddingDeadline': False,
                               'choosingWhatToDelete': False}


def get_deadline_info(item):
    strr = item["name"]
    strr += "\nОписание: " + item["description"]
    strr += "\nКОГДА ДЕДЛАЙН: " + item["expDate"]
    strr += "\nКогда тебя тормошить: в " + item["alarmTime"]
    return strr


@bot.message_handler(commands=['start', 'help'])  # ответ на определенный тип команд
def send_greeting(message):
    global data
    openJson()
    user_name = str(message.from_user.first_name) + ' ' + str(message.from_user.last_name)
    data = act.add_user(message.from_user.id, user_name, data)
    # reply_to отвечает на полученное сообщение (ну типо ссылается)
    bot.send_message(message.from_user.id, "Чо хочешь сделать?\n\n1./add_deadline - добавь дедлайн"
                                           "\n\n2./finish_deadline - закрыть дедлайн\n\n"
                                           "3./show_deadlines - чекни свои дедлайны\n\n"
                                           "Просто нажми на одну из команд!!")
    saveJson()


@bot.message_handler(commands=['finish_deadline'])
def finish_deadline(message):
    openJson()
    count = 0
    mes_beg = "Какой дедлайн закрыл м?\nПросто введи его имя!\n"
    mes = ""
    for x in data["Deadlines"]:
        if x['userId'] == message.from_user.id:
            count += 1
            mes += "Дедлайн №" + str(count) + ": " + x['name'] + "\n"
    if count == 0:
        bot.send_message(message.from_user.id, "А ДЕДЛАЙНОВ ТО НЕТУ!!")
    else:
        mes_beg += mes
        users_triggers[message.from_user.id]['choosingWhatToDelete'] = True
        bot.send_message(message.from_user.id, mes_beg)


@bot.message_handler(commands=['show_deadlines'])
def display_deadlines(message):
    global data
    openJson()
    count = 0
    mes = ""
    for x in data["Deadlines"]:
        if x['userId'] == message.from_user.id:
            count += 1
            mes += "Дедлайн №" + str(count) + "\n"
            mes += get_deadline_info(x) + "\n\n"
    if count == 0:
        bot.send_message(message.from_user.id, "УРА ДЕДЛАЙНОВ НЕТУ!!")
    else:
        bot.send_message(message.from_user.id, mes)


@bot.message_handler(commands=['add_deadline'])
def send_deadline_request(message):
    openJson()
    bot.send_message(message.from_user.id, "Введи информацию о дедлайне таким образом одним сообщением:"
                                           "\nНазвание дедлайна\nОписание (можно оставить пустым)\n"
                                           "Дата окончания дедлайна (в формате дд.мм.гггг)\n"
                                           "Время в которое тебя тормошить (в формате чч:мм:сс)")
    users_triggers[message.from_user.id]['isAddingDeadline'] = True


@bot.message_handler(content_types=['text'])
def actions(message):
    global data
    openJson()
    if users_triggers[message.from_user.id]['isAddingDeadline']:
        res = str(message.text).split("\n")
        if len(res) == 4:
            is_unique = True
            for x in data['Deadlines']:
                if x['name'] == res[0] and x['userId'] == message.from_user.id:
                    is_unique = False
                    break
            if is_unique:
                name = res[0]
                desc = res[1]
                try:
                    final_date = datetime.strptime(res[2], "%d.%m.%Y")
                    notification_time = datetime.strptime(res[3], "%H:%M:%S")
                    if final_date.date() < datetime.now().date():
                        bot.send_message(message.from_user.id, "А дедлайн то уже прошел! Введи дату не раньше завтра!")
                    else:
                        id = 0
                        if len(data["Deadlines"]) != 0:
                            id = data["Deadlines"][-1]["id"] + 1
                        data = act.add_deadline(id, name, message.from_user.id, desc, res[2], res[3], data)
                        bot.send_message(message.from_user.id, "Все деделайн добавился!")
                except ValueError:
                    bot.send_message(message.from_user.id,
                                     "Ты чета не то ввел!\nРовно 4 строки одним сообщением в правильном формате плз!\n"
                                     "Давай добавляй заново!")
            else:
                bot.send_message(message.from_user.id, "Дедлайн с таким именем уже есть! Давай другое!")
        else:
            bot.send_message(message.from_user.id,
                             "Ты чета не то ввел!\nРовно 4 строки одним сообщением в правильном формате плз!\n"
                             "Давай добавляй заново!")
        users_triggers[message.from_user.id]['isAddingDeadline'] = False
    elif users_triggers[message.from_user.id]['choosingWhatToDelete']:
        mes, data = act.delete_deadline(message.text, data)
        bot.send_message(message.from_user.id, mes)
        users_triggers[message.from_user.id]['choosingWhatToDelete'] = False
    else:
        bot.send_message(message.from_user.id, "Скажи команду!\nЕсли забыл напиши /start или /help !")
    saveJson()


bot.polling(none_stop=True)  # МУЗЫКА ГРОМЧЕ ГЛАЗА ЗАКРЫТЫ ЭТО НОН СТОП
