import asyncio

from trading import TelegramClass, ByBit

from dotenv import load_dotenv

load_dotenv()


async def main():
    print("🤖 Bot iniciado!")

    tele = TelegramClass()
    await tele.start()

    bybit = ByBit(value_per_order=200, test=True)
    await tele.listen_channel(bybit.create_future_order)


if __name__ == "__main__":
    asyncio.run(main())
