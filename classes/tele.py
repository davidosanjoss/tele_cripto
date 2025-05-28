import os

from telethon import TelegramClient, events


class TelegramClass:
    def __init__(self, channel_id):
        self.client = None
        self.channel = None
        self.channel_id = channel_id

    async def config(self):
        self.client = TelegramClient(
            "session_name",
            int(os.environ['TELE_API_ID']),
            os.environ['TELE_API_HASH'])
        await self.client.start()
        await self.__set_channel()

    async def __verify_has_client(self):
        if self.client is None:
            raise Exception('Client is not set, please use .config()')

    async def __set_channel(self):
        dialogs = await self.client.get_dialogs()

        return next(
            (d.entity for d in dialogs if d.entity.id == self.channel_id),
            None
        )

    async def get_all_chats(self):
        await self.__verify_has_client()

        dialogs = await self.client.get_dialogs()
        for dlg in dialogs:
            name = dlg.name
            username = dlg.entity.username  # None se não houver @username
            chat_id = dlg.entity.id
            print(f"{name:30}  → @{username if username else '-'}  (ID={chat_id})")

    async def fetch_history(self, limit=10):
        await self.__verify_has_client()

        async for msg in self.client.iter_messages(self.channel, limit=limit):
            print(f"{msg.id} • {msg.date:%Y-%m-%d %H:%M} • {msg.sender_id}: {msg.text}")

    async def listen_channel(self):
        await self.__verify_has_client()

        @self.client.on(events.NewMessage(chats=self.channel))
        async def handler(event):
            print(f"[NOVO] {event.id} • {event.date:%H:%M} • {event.sender_id}: {event.text}")

        print("🔔 Aguardando novas mensagens em VIP SIGNALS…")
        await self.client.run_until_disconnected()
