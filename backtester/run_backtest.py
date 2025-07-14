# backtester/run_backtest.py

import pandas as pd
from backtester.market import MarketSimulator
from backtester.data_handler import load_data

# Import your existing SMC rule functions
from shared.rules.bos import detect_bos
from shared.rules.smc_conditions import (
    find_order_block,
    check_liquidity_sweep,
    check_fibonacci_zone,
    check_clean_structure,
    check_impulse_from_ob
)
# Import your risk manager if you have one
# from shared.utils.risk_manager import calculate_lot_size

def run_backtest():
    """Main function to run the backtesting process."""
    # --- 1. Initialization ---
    market = MarketSimulator(initial_balance=1000.0)
    # Make sure you have a CSV with historical data
    df = load_data('path/to/your/historical_data.csv')
    lookback = 50 # Number of candles to establish initial structure

    # --- 2. Main Backtesting Loop ---
    print("\n--- Starting Backtest Loop ---")
    for i in range(lookback, len(df)):
        # Create a view of the history available at this point in time
        current_df = df.iloc[0:i]
        current_candle = df.iloc[i]

        # Update market with the latest candle to check for SL/TP hits
        market.tick(current_candle)

        # --- 3. Apply Strategy Logic ---
        bos_direction, bos_level = detect_bos(current_df, lookback=20)

        if bos_direction:
            ob = find_order_block(current_df, bos_direction)
            if ob:
                # Run confluence checks
                checks = [
                    check_liquidity_sweep(current_df, ob, bos_direction),
                    check_fibonacci_zone(current_df, ob, bos_direction),
                    check_clean_structure(current_df, ob),
                    check_impulse_from_ob(current_df, ob, bos_level, bos_direction)
                ]
                score = sum(checks)

                # --- 4. Simulate Execution ---
                if score >= 3: # Your acceptance threshold
                    print(f"\nTrade Signal Found at index {i}!")
                    # Define entry, SL, and TP
                    entry_price = ob['high'] if bos_direction == 'bullish' else ob['low']
                    sl_price = ob['low'] if bos_direction == 'bullish' else ob['high']
                    # Simplified TP calculation (e.g., 3R)
                    tp_price = entry_price + (abs(entry_price - sl_price) * 3) if bos_direction == 'bullish' else entry_price - (abs(entry_price - sl_price) * 3)

                    # Simplified lot size for simulation
                    lot_size = 0.1

                    if bos_direction == 'bullish':
                        market.buy(entry_price, sl_price, tp_price, lot_size)
                    elif bos_direction == 'bearish':
                        market.sell(entry_price, sl_price, tp_price, lot_size)

    # --- 5. Post-Loop Analysis ---
    print("\n--- Backtest Finished ---")
    print(f"Final Balance: ${market.balance:.2f}")
    total_trades = len(market.trade_history)
    wins = len([t for t in market.trade_history if t['status'] == 'TP'])
    losses = len([t for t in market.trade_history if t['status'] == 'SL'])
    win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0

    print(f"Total Trades: {total_trades}")
    print(f"Win Rate: {win_rate:.2f}%")

if __name__ == '__main__':
    run_backtest()
