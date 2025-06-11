import os
from pprint import pprint

import ccxt.async_support as ccxt


class ByBit:
    def __init__(self, value_per_order=100.00, test=False):
        self.value_per_order = value_per_order
        # noinspection PyTypeChecker
        self.exchange = ccxt.bybit(
            {
                "apiKey": os.getenv("BYBIT_API_KEY"),
                "secret": os.getenv("BYBIT_API_SECRET"),
                "enableRateLimit": True,
            }
        )
        self.exchange.enable_demo_trading(test)

    async def fetch_ticker(self, symbol):
        return await self.exchange.fetch_ticker(symbol)

    async def create_future_order(self, signal, *args, **kwargs):
        symbol = f"{signal.symbol.upper()}:USDT"
        entry_price = signal.entry
        amount = self.value_per_order / entry_price
        tp_price = float(signal.targets[0])
        diff = abs(tp_price - entry_price)
        sl_price = entry_price + diff

        if signal.side.lower() == "buy":
            sl_price = entry_price - diff

        params = {
            "takeProfit": tp_price,
            "stopLoss": sl_price,
        }

        pprint(signal)

        await self.exchange.set_leverage(signal.leverage, symbol)

        order = await self.exchange.create_order(
            symbol=f"{symbol}",
            type="limit",
            side=signal.side.lower(),
            amount=amount,
            price=entry_price,
            params=params,
        )
        return order

    async def close(self):
        await self.exchange.close()
