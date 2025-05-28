import asyncio

from classes import TelegramClass

from dotenv import load_dotenv

load_dotenv()


async def main():
    tele = TelegramClass(1962516090)
    await tele.config()

    await tele.fetch_history()
    await tele.listen_channel()


if __name__ == '__main__':
    asyncio.run(main())
