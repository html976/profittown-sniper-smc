import asyncio
import json

from internal.ws.client import TradingWebsocketClient
from shared.utils.data_manager import PriceDataManager


async def main():
    # Replace with your app_id
    app_id = 83085
    uri = f"wss://ws.derivws.com/websockets/v3?app_id={app_id}"
    # uri = f"wss://demo.piesocket.com/v3/channel_123?api_key=VCXCEuvhGcBDP7XhiJJUDvR1e1D3eiVjgZ9VRiaV&notify_self"

    price_manager = PriceDataManager()

    client = TradingWebsocketClient(uri, price_manager)

    await client.connect()

    try:
        # --- Request 2: Get Tick History ---
        print("\nSending Step 100 tick history request...")
        historical_candles = await client.tick_history(
            {
                "ticks_history": "stpRNG",
                "adjust_start_time": 1,
                "granularity": 900,
                "count": 100,
                "end": "latest",
                "start": 1,
                "style": "candles",
            }
        )
        # print(historical_candles)

        # Convert dictionary to DataFrame
        price_manager.initialize_history(historical_candles['candles'])
        print(price_manager.get_dataframe())
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
