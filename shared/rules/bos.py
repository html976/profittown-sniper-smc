import pandas as pd

def detect_bos(df: pd.DataFrame, lookback: int = 1):
    """
    Detects a Break of Structure (BOS) by checking if the latest close
    has surpassed the highest high or lowest low of the lookback period.

    Args:
        df: A pandas DataFrame with 'high', 'low', and 'close' columns.
        lookback: The number of recent candles to consider for the swing points.

    Returns:
        A tuple containing the direction ('bullish', 'bearish', or None) and
        the price level that was broken.
    """
    if len(df) < lookback:
        return None, None

    # Define the lookback period, excluding the most recent candle
    lookback_period = df.iloc[-lookback-1:-1]

    # Find the highest high and lowest low in the lookback period
    swing_high = lookback_period['high'].max()
    swing_low = lookback_period['low'].min()

    last_close = df.iloc[-1]['close']

    # Check for a bullish or bearish break
    if last_close > swing_high:
        print("\n💹 Break of Structure Detected.")
        return 'bullish', swing_high
    elif last_close < swing_low:
        print("\n💹 Break of Structure Detected.")
        return 'bearish', swing_low

    return None, None
