import pandas as pd

import pandas as pd
import numpy as np


import pandas as pd
import plotly.graph_objects as go


def visualize_bos(df: pd.DataFrame, direction: str, level: float, lookback: int):
    """
    Creates an interactive candlestick chart using Plotly and visualizes the BOS.

    Args:
        df: The pandas DataFrame with OHLC data and a DatetimeIndex.
        direction: 'bullish' or 'bearish'.
        level: The price level of the broken structure.
        lookback: The lookback period used for BOS detection.
    """
    if not direction or not level:
        print("No Break of Structure to visualize.")
        # Even with no BOS, we can still show a basic chart
        fig = go.Figure(data=[go.Candlestick(
            x=df.index, open=df['open'], high=df['high'], low=df['low'], close=df['close'])])
        fig.update_layout(title_text='Candlestick Chart',
                          template='plotly_dark')
        fig.show()
        return

    # Create the main candlestick figure
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df['open'],
                                         high=df['high'],
                                         low=df['low'],
                                         close=df['close'],
                                         name='Candles')])

    # Add a horizontal line for the broken structure level
    fig.add_shape(type='line',
                  x0=df.index[0], y0=level,
                  x1=df.index[-1], y1=level,
                  line=dict(color='Gray', dash='dash'),
                  name='BOS Level')

    # Add a marker for the breakout candle
    breakout_candle_index = df.index[-1]

    if direction == 'bullish':
        marker_price = df.loc[breakout_candle_index, 'low'] * 0.99
        marker_symbol = 'triangle-up'
        marker_color = 'limegreen'
    else:  # bearish
        marker_price = df.loc[breakout_candle_index, 'high'] * 1.01
        marker_symbol = 'triangle-down'
        marker_color = 'red'

    fig.add_trace(go.Scatter(x=[breakout_candle_index],
                             y=[marker_price],
                             mode='markers',
                             marker=dict(symbol=marker_symbol,
                                         color=marker_color, size=12),
                             name='BOS Event'))

    # Update layout for a clean look
    fig.update_layout(
        title=f'BOS Detected: {direction.capitalize()}',
        template='plotly_dark',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,  # Hide the range slider
        showlegend=False
    )

    fig.show()


def detect_bos(df: pd.DataFrame, lookback: int = 20):
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


def check_clean_structure(df: pd.DataFrame, ob: dict):
    """
    Checks for a Fair Value Gap / Imbalance after the OB, indicating a clean structure.

    Returns:
        True or False.
    """
    ob_index = df.index.get_loc(ob['index'])
    if ob_index < 2:
        return False

    candle_before_ob = df.iloc[ob_index - 1]
    candle_after_ob = df.iloc[ob_index + 1]

    # Bullish Imbalance: The low of the candle after the impulse is higher
    # than the high of the candle before the OB.
    bullish_fvg = candle_after_ob['low'] > candle_before_ob['high']

    # Bearish Imbalance: The high of the candle after the impulse is lower
    # than the low of the candle before the OB.
    bearish_fvg = candle_after_ob['high'] < candle_before_ob['low']

    return bullish_fvg or bearish_fvg
