from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

def get_client():
    client = Client(
        os.getenv("API_KEY"),
        os.getenv("API_SECRET"),
        testnet=True
    )

    client.futures_change_leverage(symbol="BTCUSDT", leverage=10)
    return client

