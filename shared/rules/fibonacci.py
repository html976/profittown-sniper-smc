import pandas as pd


def check_fibonacci_zone(df: pd.DataFrame, ob: dict, direction: str):
    """
    Checks if the Order Block is within the 61.8% - 78.6% Fibonacci zone.

    Returns:
        True or False.
    """
    swing_high = df['high'].max()
    swing_low = df['low'].min()
    price_range = swing_high - swing_low

    if direction == 'bullish':
        fib_618 = swing_high - (price_range * 0.618)
        fib_786 = swing_high - (price_range * 0.786)
        # Check if the OB's high is within the zone
        return fib_786 <= ob['high'] <= fib_618

    elif direction == 'bearish':
        fib_618 = swing_low + (price_range * 0.618)
        fib_786 = swing_low + (price_range * 0.786)
        # Check if the OB's low is within the zone
        return fib_618 <= ob['low'] <= fib_786

    return False
