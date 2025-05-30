import os
import pprint
import re

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
            username = dlg.entity.username
            chat_id = dlg.entity.id
            print(f"{name:30}  → @{username if username else '-'}  (ID={chat_id})")

    async def fetch_history(self, limit=10):
        await self.__verify_has_client()

        async for msg in self.client.iter_messages(self.channel, limit=limit):
            print(f"{msg.id} • {msg.date:%Y-%m-%d %H:%M} • {msg.sender_id}: {msg.text}")

    async def listen_channel(self):
        await self.__verify_has_client()

        @self.client.on(events.NewMessage(chats=self.channel))
        # @self.client.on(events.NewMessage)
        async def handler(event):
            message = await self.parse_message(event)
            signal = message["signal"]
            target = message["target"]

            if not signal:
                return

            print(f"🚀 Novo sinal: {signal.get("side").upper()} - {signal.get("symbol")} - Target: {target.get("target_number", 0)}")
            pprint.pp(message)

        print("🔔 Aguardando novas mensagens…")
        await self.client.run_until_disconnected()

    async def parse_message(self, event):
        await self.__verify_has_client()

        msg = event.message

        reply_id = msg.reply_to_msg_id
        if reply_id:
            original = await event.get_reply_message()
            signal_text = original.text if original else ""
        else:
            signal_text = msg.text

        side = None
        if "Long" in signal_text:
            side = "buy"
        elif "Short" in signal_text:
            side = "sell"

        m = re.search(r'Name:\s*([A-Z0-9]+/[A-Z0-9]+)', signal_text)
        symbol = m.group(1) if m else None

        m = re.search(r'Cross\s*\(\s*(\d+)X\s*\)', signal_text.replace('*', ''), flags=re.IGNORECASE)
        leverage = int(m.group(1)) if m else None

        m = re.search(r'Entry price[^\n]*\n\s*([\d\.]+)', signal_text, flags=re.IGNORECASE)
        entry = float(m.group(1)) if m else None

        targets = [float(t) for t in re.findall(r'\d\)\s*([\d\.]+)', signal_text)]

        signal = None
        if side and symbol and entry is not None:
            signal = {
                "side": side,
                "symbol": symbol,
                "leverage": leverage,
                "entry": entry,
                "targets": targets,
            }

        target = None
        if reply_id and signal:
            txt = msg.text
            m1 = re.search(r'Target\s*#\s*(\d+)', txt, flags=re.IGNORECASE)
            m2 = re.search(r'Current profit[:\-\s]*([\d\.]+)%', txt, flags=re.IGNORECASE)
            if m1 and m2:
                target = {
                    "target_number": int(m1.group(1)),
                    "profit": float(m2.group(1))
                }

        return {
            "signal": signal,
            "target": target
        }
