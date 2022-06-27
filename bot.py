import telebot
import datetime
import json
import os

TOKEN = os.environ['TOKEN']

def getdata():
    fjson = open('botdata.json')
    botdata = json.load(fjson)
    return botdata

def getbot():
    return telebot.TeleBot(TOKEN)

def Send(text):
    for i in getdata()['access']:
        getbot().send_message(i, f"{text}")

def start():
    bot = getbot()
#    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
#    bot.send_message(539836106, f"Bot started {now}")

    @bot.message_handler(commands=['test'])
    def test(message):
        bot.reply_to(message, message.text.split(' ')[1])

    @bot.message_handler(commands=['start', 'help'])
    def start(message):
        botdata = getdata()
        if message.from_user.id in botdata['access']:
            bot.reply_to(message, "У вас есть доступ к уведомлениям")
        else:
            bot.reply_to(message, f"У вас нет доступа к уведомлениям. \n/getaccess - чтобы запросить доступ")

    @bot.message_handler(commands=['getaccess'])
    def getaccess(message):
        botdata = getdata()
        if message.from_user.id in botdata['access']:
            bot.reply_to(message, "У вас уже есть доступ к уведомлениям")
        else:
            bot.reply_to(message, "Вы отправили запрос на получение доступа...")
            bot.send_message(539836106, f"{message.from_user.username}\nзапросил доступ к боту\n/access give {message.from_user.id} - чтобы выдать доступ")

    @bot.message_handler(commands=['access'])
    def access(message):
        botdata = getdata()
        arg = message.text.split(' ')
        if message.from_user.id in botdata['admins']:
            if 1 < len(arg):
                if arg[1] == "give":
                    if 2 < len(arg):
                        if int(arg[2]) in botdata['access']:
                            bot.reply_to(message, f"ID: {arg[2]} уже имеет доступ")
                            return
                        botdata['access'].append(int(arg[2]))
                        with open('botdata.json', 'w') as outfile:
                            json.dump(botdata, outfile)
                        bot.reply_to(message, f"Выдан доступ для ID: {arg[2]}")
                        bot.send_message(int(arg[2]), f"Доступ получен")
                    else:
                        bot.reply_to(message, f"Не указан ID")
                if arg[1] == "remove":
                    if 2 < len(arg):
                        botdata['access'].remove(int(arg[2]))
                        with open('botdata.json', 'w') as outfile:
                            json.dump(botdata, outfile)
                        bot.reply_to(message, f"ID: {arg[2]} удалён из доступа")
                        bot.send_message(int(arg[2]), f"Вас удалили из доступа")
                    else:
                        bot.reply_to(message, f"Не указан ID")
                if arg[1] == "list":
                    bot.reply_to(message, f"Список ID в доступе:\n{botdata['access']}")
            else:
                bot.reply_to(message, f"/access give|remove|list")

    bot.infinity_polling()
