import asyncio

class Work:
    def __init__(self):
        self.is_started = False
        self._task = None

    async def Start(self, message, text):
        if not self.is_started:
            self.is_started = True
            self._task = asyncio.ensure_future(self._Working(message, text))

    async def Stop(self):
        if self.is_started:
            self.is_started = False
            self._task.cancel()

    async def _Working(self, message, text):
        while True:
            await message.reply_text("Выйти из подземелья", quote=False)
            await message.reply_text("Реанимировать жабу", quote=False)
            await message.reply_text(text, quote=False)
            await asyncio.sleep(7210)  # 7200

            await message.reply_text("Завершить работу", quote=False)
            await asyncio.sleep(21610)  # 21600

class Eat:
    def __init__(self):
        self.is_started = False
        self._task = None

    async def Start(self, message, text):
        if not self.is_started:
            self.is_started = True
            self._task = asyncio.ensure_future(self._Eating(message, text))
        else:
            await message.reply_text("Жаба уже кушает!", quote=True)


    async def Stop(self):
        if self.is_started:
            self.is_started = False
            self._task.cancel()

    async def _Eating(self, message, text):
        while True:
            await message.reply_text(text, quote=False)
            if text.lower() == "откормить жабу":
                await asyncio.sleep(14410) #14400
            elif text.lower() == "покормить жабу":
                await asyncio.sleep(43210) #43200


class Kits:
    def __init__(self):
        self.is_started = False
        self._task = None

    async def Start(self, app, message):
        if not self.is_started:
            self.is_started = True
            self._task = asyncio.ensure_future(self._SendingKits(app, message))
        else:
            await message.reply_text("Жаба уже отправляет аптечки!", quote=True)

    async def Stop(self):
        if self.is_started:
            self.is_started = False
            self._task.cancel()

    async def _SendingKits(self, app, message):
        while True:
            await message.reply_text("Отправить аптечки 10", quote=True)
            await asyncio.sleep(86410)  # 86400
