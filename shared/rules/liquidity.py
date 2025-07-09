import pandas as pd


def check_liquidity_sweep(df: pd.DataFrame, ob: dict, direction: str):
    """
    Checks if a liquidity sweep occurred just before the OB.

    Returns:
        True or False.
    """
    ob_index = df.index.get_loc(ob['index'])

    # Define a small period before the OB to look for a sweep
    search_df = df.iloc[max(0, ob_index - 10):ob_index]
    if search_df.empty:
        return False

    swing_high = search_df['high'].max()
    swing_low = search_df['low'].min()

    sweep_candle = df.iloc[ob_index - 1]  # The candle just before the OB

    if direction == 'bullish':
        # Check if the candle before OB wicked below a recent low
        return sweep_candle['low'] < swing_low
    elif direction == 'bearish':
        # Check if the candle before OB wicked above a recent high
        return sweep_candle['high'] > swing_high

    return False
