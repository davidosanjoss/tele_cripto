import asyncio

from classes import TelegramClass

from dotenv import load_dotenv

load_dotenv()


async def main():
    print("🤖 Bot iniciado!")
    tele = TelegramClass(1962516090)
    await tele.config()

    await tele.listen_channel()

    # exchange = ccxt.bybit({
    #     "apiKey": os.getenv("BYBIT_API_KEY", ""),
    #     "secret": os.getenv("BYBIT_API_SECRET", ""),
    #     "enableRateLimit": True,
    #     "options": {
    #         "adjustForTimeDifference": True,
    #     },
    # })
    #
    # exchange.enable_demo_trading(True)
    #
    # await exchange.load_markets()
    #
    # print("adw")
    #
    # try:
    #     pprint(await exchange.fetch_transfers())
    # except Exception as e:
    #     print(e)
    #
    # await exchange.close()


if __name__ == '__main__':
    asyncio.run(main())
