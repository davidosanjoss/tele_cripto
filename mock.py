import asyncio
import random

from trading import TelegramClass, ByBit

from dotenv import load_dotenv

load_dotenv()


async def main():
    bybit = ByBit(test=True)

    tele = TelegramClass(channel_id=7844586224, session_name="session_mock")
    await tele.start()

    try:
        while True:
            input("Press enter to send mock message...")

            coins = ["SONIC", "ZETA", "LINK", "MASK", "TON", "TIA"]
            ticker = await bybit.fetch_ticker(f"{random.choice(coins)}/USDT:USDT")
            symbol = ticker.get("symbol", "").split(":", 1)[0]
            cross = random.choice([15, 25, 50])
            entry = float(ticker.get("last", 0.0))
            side_int = int(random.choice([True, False]))
            side = ("🟢 Long", "🔴 Short")[side_int]

            targets = [
                round(entry * (1 + (1, -1)[side_int] * pct / cross), 4)
                for pct in (0.10, 0.20, 0.30, 0.40)
            ]

            message = f"""
                {side}
                Name: {symbol}
                Margin mode: Cross ({cross}X)
                
                ↪️ Entry price(USDT):
                {entry:.10f}
                
                Targets(USDT):
                1) {targets[0]:.10f}
                2) {targets[1]:.10f}
                3) {targets[2]:.10f}
                4) {targets[3]:.10f}
                5) 🔝 unlimited
            """

            await tele.client.send_message("me", message)

    except asyncio.CancelledError:
        await tele.client.close()


asyncio.run(main())
