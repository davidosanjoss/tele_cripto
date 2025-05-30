import os
import ccxt.async_support as ccxt


class BrokerageClass:
    def __init__(self):
        self.exchange = ccxt.bybit({
            "apiKey": os.getenv("BYBIT_API_KEY"),
            "secret": os.getenv("BYBIT_API_SECRET"),
            "enableRateLimit": True,
            "options": {
                "adjustForTimeDifference": True,
            },
        })
        self.exchange.set_sandbox_mode(True)
