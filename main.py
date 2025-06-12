import asyncio
import os

from trading import TelegramClass, ByBit

from dotenv import load_dotenv

load_dotenv()


async def main():
    print("🤖 Bot iniciado!")

    tele = TelegramClass(channel_id=os.getenv("TELEGRAM_CHANNEL_ID"))
    await tele.start()

    bybit = ByBit(value_per_order=float(os.getenv("VALUE_PER_ORDER")), test=True)
    await tele.listen_channel(bybit.create_future_order)


if __name__ == "__main__":
    asyncio.run(main())
