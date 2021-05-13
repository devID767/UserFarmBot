from pyrogram import Client, filters

from time import sleep

app = Client("farm_account_1")

CanWork = False
IsWorking = False

CanSendKits = False
IsSending = False

def IsSelf(message):
    if message.from_user.is_self:
        return True
    ReoliedUser = app.get_messages(message.chat.id, reply_to_message_ids=message.message_id).from_user
    if ReoliedUser.is_self:
        return True
    else:
        return False

def IsAll(message, command):
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
        message.reply_text(f"CanWork = {CanWork}\n"
                           f"CanSendKits = {CanSendKits}\n\n"
                           f"IsWorking = {IsWorking}\n"
                           f"IsSending = {IsSending}")


@app.on_message(filters.command("send", prefixes="."))
def SendKitsCommand(client, message):
    if   IsSelf(message):
        command = message.text.split(".send ", maxsplit=1)[1]
        #message.delete()

        global CanSendKits
        global IsSending

        if command == "start":
            CanSendKits = True
            message.reply_text("Send started")
            SendKits(message)
        elif command == "stop":
            CanSendKits = False
            IsSending = False
            message.reply_text("Send stopped")
        else:
            message.reply_text("Unknown command")

def SendKits(message):
    global IsSending

    #Receiver = app.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
    if not IsSending and CanSendKits:
        IsSending = True
        while IsSending:
            app.send_message(message.chat.id, "Отправить аптечки 10", reply_to_message_id=message.message_id)
            sleep(86410) #86400
        IsSending = False
    else:
        message.reply_text("Is sending")


@app.on_message(filters.command("work", prefixes="."))
def WorkCommand(client, message):
    if IsSelf(message):
        command = message.text.split(".work ", maxsplit=1)[1]
        #message.delete()

        global CanWork
        global IsWorking

        if command.lower() == "поход в столовую" or command.lower() == "работа крупье" or command.lower() == "работа грабитель":
            CanWork = True
            Working(message, command)
            message.reply_text("Work started")
        elif command == "stop":
            CanWork = False
            IsWorking = False
            message.reply_text("Work stopped")
        else:
            message.reply_text("Unknown command")

def Working(message, work):
    global IsWorking

    if not IsWorking:
        IsWorking = True
        while CanWork and IsWorking:
            message.reply_text("Выйти из подземелья", quote=False)
            message.reply_text("Реанимировать жабу", quote=False)
            message.reply_text(work, quote=False)
            sleep(7210)  # 7200
            if not IsWorking:
                break
            message.reply_text("Завершить работу", quote=False)
            sleep(21610)  # 21600
        message.reply_text("Работа завершена", quote=False)
    else:
        message.reply_text("Is Working")

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

@app.on_message(filters.text & filters.command("help", prefixes="."))
def Help(client, message):
    if IsSelf(message):
        message.delete()
        message.reply_text(f".status [all/(repeat)]\n"
                           f".send [start/stop]\n"
                           f".work [name of work/stop]\n"
                           f".take (to take frog)\n"
                           f".class (to take the class)\n"
                           f".inventory [all/(repeat)]\n"
                           f".balance [all/(repeat)]\n"
                           f".myfrog [all/(repeat)]\n"
                           f".froginfo all/(repeat)]\n"
                           f".sendmoney [Number]")

app.run()