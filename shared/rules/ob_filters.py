import pandas as pd


def find_order_block(df: pd.DataFrame, direction: str):
    """
    Finds the last opposing candle before an impulse move.

    Returns:
        A dictionary with OB details (e.g., {'high': 1.1, 'low': 1.0}) or None.
    """
    # We look for the OB in the last `n` candles before the breakout
    search_period = df.iloc[-20:-1]

    if direction == 'bullish':
        # Find the last bearish candle before a strong up-move
        down_candles = search_period[search_period['close']
                                     < search_period['open']]
        if not down_candles.empty:
            last_ob_candle = down_candles.iloc[-1]
            return {'high': last_ob_candle['high'], 'low': last_ob_candle['low'], 'index': last_ob_candle.name}

    elif direction == 'bearish':
        # Find the last bullish candle before a strong down-move
        up_candles = search_period[search_period['close']
                                   > search_period['open']]
        if not up_candles.empty:
            last_ob_candle = up_candles.iloc[-1]
            return {'high': last_ob_candle['high'], 'low': last_ob_candle['low'], 'index': last_ob_candle.name}

    return None


def check_impulse_from_ob(df: pd.DataFrame, ob: dict, bos_level: float, direction: str):
    """
    Checks if the candles following the OB led to the BOS.

    Returns:
        True or False.
    """
    ob_index = df.index.get_loc(ob['index'])
    impulse_candles = df.iloc[ob_index + 1:]

    if direction == 'bullish':
        # Was the BOS level broken by any candle after the OB?
        return impulse_candles['close'].max() > bos_level
    elif direction == 'bearish':
        # Was the BOS level broken by any candle after the OB?
        return impulse_candles['close'].min() < bos_level

    return False
