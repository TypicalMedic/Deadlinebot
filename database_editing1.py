import json
from datetime import datetime
import datetime as delta


def write_in_file(incoming_data):
    with open('Database.json', 'w', encoding='utf-8') as f:
        json.dump(incoming_data, f, ensure_ascii=False, indent=4)


def delete_deadline(name, data):
    count = 0
    mes = ""
    found = False
    for x in data['Deadlines']:
        if x['name'] == name:
            data['Deadlines'].pop(count)
            found = True
            break
        count += 1
    if found:
        mes = 'Дедлайн завершен!!'
    else:
        mes = "Такого дедлайна нет!!"
    with open('Database.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return mes, data


def delete_exp_deadline(name, data):
    count = 0
    for x in data['Deadlines']:
        if x['name'] == name:
            data['Deadlines'].pop(count)
            break
        count += 1
    with open('Database.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return data


def add_deadline(id, name, userId, description, expDate, alarmTime, data):
    notific = datetime.now().strftime("%d.%m.%Y")
    if datetime.now().time() > datetime.strptime(alarmTime, "%H:%M:%S").time():
        notific = (datetime.now() + delta.timedelta(days=1)).strftime("%d.%m.%Y")
    data['Deadlines'].append(
        {
            "id": id,
            "name": name,
            "userId": userId,
            "description": description,
            "expDate": expDate,
            "alarmTime": alarmTime,
            "lastNotificationDate": notific
        }
    )
    return data


def add_user(id, name, data):
    isok = True
    for x in data["Users"]:
        if x["id"] == id:
            isok = False
    if isok:
        data["Users"].append(
            {
                "id": id,
                "name": name
            }
        )
        with open('Database.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    return data
