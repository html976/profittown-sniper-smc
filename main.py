import asyncio
import json

from internal.ws.client import TradingWebsocketClient
from shared.utils.data_manager import PriceDataManager

import pandas as pd

from shared.rules.fibonacci import check_fibonacci_zone
from shared.rules.ob_filters import find_order_block, check_impulse_from_ob
from shared.rules.structure import detect_bos, visualize_bos, check_clean_structure
from shared.rules.liquidity import check_liquidity_sweep


async def main():
    # --- 1. Setup Client and Fetch Data ---
    app_id = 83085  # Replace with your app_id if needed
    uri = f"wss://ws.derivws.com/websockets/v3?app_id={app_id}"
    price_manager = PriceDataManager()
    client = TradingWebsocketClient(uri, price_manager)
    await client.connect()

    try:
        print("Fetching historical candle data...")
        historical_data = await client.tick_history({
            "ticks_history": "stpRNG",
            "adjust_start_time": 1,
            "granularity": 900,  # 15-minute timeframe
            "count": 300,
            "end": "latest",
            "start": 1,
            "style": "candles",
        })

        price_manager.initialize_history(historical_data.get('candles', []))
        df = price_manager.get_dataframe()

        if df.empty:
            print("Could not fetch historical data. Exiting.")
            return

        # --- 2. Check for Break of Structure (Entry Condition) ---
        bos_direction, bos_level = detect_bos(df, lookback=20)
        if not bos_direction:
            print("No Break of Structure found. No trade setup.")
            return

        print(
            f"\n🔥 Condition 1: Break of Structure FOUND! ({bos_direction} @ {bos_level})")

        # --- 3. Find The Order Block ---
        ob = find_order_block(df, bos_direction)
        if not ob:
            print("No valid Order Block found for this BOS. No trade setup.")
            return

        print(
            f"✅ Condition 2: Valid Order Block FOUND at {ob['high']}/{ob['low']}")

        # --- 4. Run All Other Confluence Checks ---
        print("\n--- Scoring Confluence ---")
        confluence_checks = {
            "Liquidity Sweep": check_liquidity_sweep(df, ob, bos_direction),
            "Fibonacci Zone": check_fibonacci_zone(df, ob, bos_direction),
            "Clean Structure (Imbalance)": check_clean_structure(df, ob),
            "Impulse from OB": check_impulse_from_ob(df, ob, bos_level, bos_direction),
        }

        # Calculate the final score
        score = sum(confluence_checks.values())

        for check, result in confluence_checks.items():
            print(
                f"{'✅' if result else '❌'} Condition: {check} -> {'Met' if result else 'Failed'}")

        print(f"\n--- Final Confluence Score: {score}/4 ---")

        # --- 5. Make Trading Decision ---
        # Acceptance threshold (e.g., 3 out of 4 checks must pass)
        if score >= 3:
            print("\n🚀 HIGH-CONFLUENCE SETUP DETECTED! Trade criteria met.")
            # Visualize the successful setup
            visualize_bos_plotly(df, bos_direction, bos_level, 20)
        else:
            print("\n📉 Low-confluence setup. No trade.")

    except Exception as e:
        print(f"An error occurred in main: {e}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())
