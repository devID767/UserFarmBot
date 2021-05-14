import random

from pyrogram import Client, filters

from time import sleep

import Sending

app = Client("farm_account_1")

Works = {}
Eats = {}
SendKits = {}

def IsSelf(message):
    if message.from_user.is_self:
        return True
    RepliedUser = app.get_messages(message.chat.id, reply_to_message_ids=message.message_id).from_user
    if RepliedUser.is_self:
        return True
    else:
        return False

def IsAll(message, command):
    sleep(random.randrange(1, 20, 1)/10)
    text = "None"
    if not IsSelf(message):
        text = message.text.split(command, maxsplit=1)[1]

    if text == "all":
        return True
    else:
        return False

@app.on_message(filters.text & filters.command("status", prefixes="."))
def Status(client, message):
    if IsAll(message, ".status ") or IsSelf(message):
        message.delete()
        try:
            IsWorking = Works.get(message.chat.id).IsWorking
        except:
            IsWorking = False

        try:
            IsEating = Eats.get(message.chat.id).IsEating
        except:
            IsEating = False

        try:
            IsSendingKits = SendKits.get(message.chat.id).IsSendingKits
        except:
            IsSendingKits = False

        message.reply_text(f"IsEating = {IsEating}\n"
                           f"IsWorking = {IsWorking}\n"
                           f"IsSendingKits = {IsSendingKits}")


@app.on_message(filters.command("send", prefixes="."))
def SendKitsCommand(client, message):
    if IsSelf(message):
        command = message.text.split(".send ", maxsplit=1)[1]

        global SendKits

        try:
            sendkits = SendKits[message.chat.id]
        except:
            sendkits = Sending.Kits()
            SendKits[message.chat.id] = sendkits

        if command == "start":
            sendkits.SendingKits(app, message)
        elif command == "stop":
            sendkits.IsSendingKits = False
            sendkits.sendKitsSleep.set()
            SendKits.pop(message.chat.id)
            message.reply_text("Send stopped")
        else:
            message.reply_text("Unknown command")

@app.on_message(filters.command("eat", prefixes="."))
def EatCommand(client, message):
    if IsSelf(message):
        command = message.text.split(".eat ", maxsplit=1)[1]
        message.delete()

        global Eats

        try:
            eat = Eats[message.chat.id]
        except:
            eat = Sending.Eat()
            Eats[message.chat.id] = eat

        if command.lower() == "покормить жабу" or command.lower() == "откормить жабу":
            eat.Eating(message, command)
        elif command == "stop":
            eat.IsEating = False
            eat.eatSleep.set()
            Eats.pop(message.chat.id)
            message.reply_text("Eat stopped")
        else:
            message.reply_text("Unknown command")

@app.on_message(filters.command("work", prefixes="."))
def WorkCommand(client, message):
    if IsSelf(message):
        command = message.text.split(".work ", maxsplit=1)[1]

        global Works

        try:
            work = Works[message.chat.id]
        except:
            work = Sending.Work()
            Works[message.chat.id] = work

        if command.lower() == "поход в столовую" or command.lower() == "работа крупье" or command.lower() == "работа грабитель":
            work.Working(message, command)
        elif command == "stop":
            work.IsWorking = False
            work.workSleep.set()
            Works.pop(message.chat.id)
            message.reply_text("Work stopped")
        elif command == "finish":
            message.reply_text("Завершить работу")
        else:
            message.reply_text("Unknown command")

@app.on_message(filters.text & filters.command("take", prefixes="."))
def TakeFrog(client, message):
    if IsSelf(message):
        message.delete()
        message.reply_text("Взять жабу", quote=False)

@app.on_message(filters.text & filters.command("class", prefixes="."))
def TakeClass(client, message):
    if IsSelf(message):
        message.delete()
        message.reply_text("Выбрать класс Авантюрист", quote=False)

@app.on_message(filters.text & filters.command("inventory", prefixes="."))
def Inventory(client, message):
    if IsAll(message, ".inventory ") or IsSelf(message):
        message.delete()
        message.reply_text("Мой инвентарь", quote=False)

@app.on_message(filters.text & filters.command("balance", prefixes="."))
def Balance(client, message):
    if IsAll(message, ".balance ") or IsSelf(message):
        message.delete()
        message.reply_text("Мой баланс", quote=False)

@app.on_message(filters.text & filters.command("myfrog", prefixes="."))
def Frog(client, message):
    if IsAll(message, ".myfrog ") or IsSelf(message):
        message.delete()
        message.reply_text("Моя жаба", quote=False)

@app.on_message(filters.text & filters.command("froginfo", prefixes="."))
def Info(client, message):
    if IsAll(message, ".froginfo ") or IsSelf(message):
        message.delete()
        message.reply_text("Жаба инфо", quote=False)

@app.on_message(filters.text & filters.command("sendmoney", prefixes="."))
def SendMoney(client, message):
    if IsSelf(message):
        count = int(message.text.split(".sendmoney ", maxsplit=1)[1])
        app.send_message(message.chat.id, f"Отправить букашки {count}", reply_to_message_id=message.message_id)

@app.on_message(filters.text & filters.command("name", prefixes="."))
def Name(client, message):
    if IsSelf(message):
        name = message.text.split(".name ", maxsplit=1)[1]
        message.reply_text(f"Дать жабе имя {name}", quote=False)


@app.on_message(filters.text & filters.command("help", prefixes="."))
def Help(client, message):
    if IsSelf(message):
        message.delete()
        message.reply_text(f".status [all/(repeat)]\n"
                           f".send [start/stop]\n"
                           f".eat [name of work/stop]\n"
                           f".work [name of work/stop]\n"
                           f".take (to take frog)\n"
                           f".class (to take the class)\n"
                           f".inventory [all/(repeat)]\n"
                           f".balance [all/(repeat)]\n"
                           f".myfrog [all/(repeat)]\n"
                           f".froginfo all/(repeat)]\n"
                           f".sendmoney [Number]\n"
                           f".name (set name)")

app.run()