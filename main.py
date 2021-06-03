import random

from pyrogram import Client, filters

from time import sleep

import Sending

app = Client("farm_account_1")

Works = {}
Eats = {}
SendKits = {}

Num = 1

async def IsSelf(message):
    if message.from_user.is_self:
        return True
    RepliedUser = await app.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
    if RepliedUser.from_user.is_self:
        return True
    else:
        return False

async def IsAll(message):
    sleep(Num/2)
    text = message.text.split(maxsplit=2)[1]

    if text == "all":
        return True
    else:
        return False

@app.on_message(filters.text & filters.command("number", prefixes="."))
async def SetNum(client, message):
    if await IsSelf(message):
        message.delete()
        global Num
        Num = int(message.text.split(".number ", maxsplit=1)[1])
        await message.reply_text(f"Мое установленое число = {Num}")

#@app.on_message(filters.text & filters.command("status", prefixes="."))
async def Status(client, message):
    try:
        IsWorking = Works.get(message.chat.id).is_started
    except:
        IsWorking = False
    try:
        IsEating = Eats.get(message.chat.id).is_started
    except:
        IsEating = False
    try:
        IsSendingKits = SendKits.get(message.chat.id).is_started
    except:
        IsSendingKits = False
    await message.reply_text(f"IsEating = {IsEating}\n"
                        f"IsWorking = {IsWorking}\n"
                        f"IsSendingKits = {IsSendingKits}\n"
                        f"Num = {Num}")

async def SendKitsCommand(client, message):
    command = message.text.split(".send ", maxsplit=1)[1]
    global SendKits

    try:
        sendkits = SendKits[message.chat.id]
    except:
        sendkits = Sending.Kits()
        SendKits[message.chat.id] = sendkits

    if command == "start":
        await sendkits.Start(app, message)
    elif command == "stop":
        await sendkits.Stop()
        del SendKits[message.chat.id]
        await message.reply_text("Send stopped")
    else:
        await message.reply_text("Unknown command")

async def EatCommand(client, message):
    command = message.text.split(".eat ", maxsplit=1)[1]
    global Eats

    try:
        eat = Eats[message.chat.id]
    except:
        eat = Sending.Eat()
        Eats[message.chat.id] = eat

    if command.lower() == "покормить жабу" or command.lower() == "откормить жабу":
        await eat.Start(message, command)
    elif command == "stop":
        await eat.Stop()
        del Eats[message.chat.id]
        await message.reply_text("Eat stopped")
    else:
        await message.reply_text("Unknown command")

async def WorkCommand(client, message):
    command = message.text.split(".work ", maxsplit=1)[1]
    global Works

    try:
        work = Works[message.chat.id]
    except:
        work = Sending.Work()
        Works[message.chat.id] = work

    if command.lower() == "поход в столовую" or command.lower() == "работа крупье" or command.lower() == "работа грабитель":
        await work.Start(message, command)
    elif command == "stop":
        await work.Stop()
        del Works[message.chat.id]
        await message.reply_text("Work stopped")
    else:
        await message.reply_text("Unknown command")

async def SendPepeatMessage(client, message, count):
    msg = await message.reply_text(message.text.split(maxsplit=1 + count)[1 + count], quote=True)
    if message.text.split(maxsplit=2 + count)[1 + count] == '.work':
        await WorkCommand(client, message)
    elif message.text.split(maxsplit=2 + count)[1 + count] == '.eat':
        await EatCommand(client, message)
    elif message.text.split(maxsplit=2 + count)[1 + count] == '.send':
        await SendKitsCommand(client, message)
    elif message.text.split(maxsplit=2 + count)[1 + count] == '.status':
        await msg.delete()
        await Status(client, message)

@app.on_message(filters.text & filters.command("repeat", prefixes="."))
async def Repeat(client, message):
    count = 0
    if await IsAll(message):
        count +=1
        await SendPepeatMessage(client, message, count)
    elif await IsSelf(message):
        count = 0
        await SendPepeatMessage(client, message, count)

@app.on_message(filters.text & filters.command("help", prefixes="."))
async def Help(client, message):
    if IsSelf(message):
        await message.delete()
        await message.reply_text(f".status [all/(repeat)]\n"
                           f".send [start/stop]\n"
                           f".eat [name of work/stop]\n"
                           f".work [name of work/stop]\n"
                           f".repeat [all message/ message]"
                           f".number [num]")

app.run()