import asyncio
import json

from internal.ws.client import WebsocketClient


# --- How to Use It ---
async def main():
    # Replace with your app_id
    app_id = 83085
    uri = f"wss://ws.derivws.com/websockets/v3?app_id={app_id}"
    # uri = f"wss://demo.piesocket.com/v3/channel_123?api_key=VCXCEuvhGcBDP7XhiJJUDvR1e1D3eiVjgZ9VRiaV&notify_self"

    client = WebsocketClient(uri)
    await client.connect()

    try:
        # --- Request 1: Ping ---
        # print("\nSending Ping request...")
        # ping_response = await client.send_request({"ping": 1})
        # print("--- Ping Response ---")
        # print(json.dumps(ping_response, indent=2))

        # --- Request 2: Get Active Symbols ---
        print("\nSending Step 100 tick history request...")
        symbols_response = await client.send_request(
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

        print("--- Step 100 Response ---")
        print(symbols_response)
        # print(f"Found {len(symbols_response.get('active_symbols', []))} symbols.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
