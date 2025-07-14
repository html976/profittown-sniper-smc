# backtester/market.py

import pandas as pd

class MarketSimulator:
    """
    Simulates a market environment, managing trades, balance, and equity.
    """
    def __init__(self, initial_balance: float = 1000.0):
        self.balance = initial_balance
        self.equity = initial_balance
        self.open_positions = []
        self.trade_history = []ÏÏÏßß

    def _calculate_profit(self, position, close_price: float):
        """Calculates profit or loss in currency."""
        # This is a simplified P/L calculation. A real one would be more
        # complex, involving pip values and lot sizes for the specific instrument.
        price_diff = close_price - position['entry_price']
        if position['type'] == 'sell':
            price_diff = -price_diff

        # Assuming lot size directly correlates to profit factor for simplicity
        profit = price_diff * position['lot_size'] * 100 # Simplified multiplier
        return profit

    def _check_trades(self, current_candle: pd.Series):
        """Checks open positions against the current candle for SL/TP hits."""
        positions_to_close = []
        for position in self.open_positions:
            close_price = None
            result = 'running'

            if position['type'] == 'buy':
                if current_candle['low'] <= position['sl']:
                    close_price, result = position['sl'], 'SL'
                elif current_candle['high'] >= position['tp']:
                    close_price, result = position['tp'], 'TP'

            elif position['type'] == 'sell':
                if current_candle['high'] >= position['sl']:
                    close_price, result = position['sl'], 'SL'
                elif current_candle['low'] <= position['tp']:
                    close_price, result = position['tp'], 'TP'

            if close_price:
                profit = self._calculate_profit(position, close_price)
                self.balance += profit
                position['profit'] = profit
                position['status'] = result
                self.trade_history.append(position)
                positions_to_close.append(position)

        # Remove closed positions from the open list
        self.open_positions = [p for p in self.open_positions if p not in positions_to_close]

    def tick(self, current_candle: pd.Series):
        """Advances the market by one candle."""
        self._check_trades(current_candle)
        # Update equity at every tick
        self.equity = self.balance # In a real system, you'd add unrealized P/L

    def _open_position(self, trade_type: str, entry_price: float, sl: float, tp: float, lot_size: float):
        """Adds a new trade to the list of open positions."""
        position = {
            'type': trade_type,
            'entry_price': entry_price,
            'sl': sl,
            'tp': tp,
            'lot_size': lot_size,
            'status': 'open',
            'profit': 0
        }
        self.open_positions.append(position)
        print(f"  -> Opened {trade_type.upper()} @ {entry_price:.2f} | SL: {sl:.2f}, TP: {tp:.2f}")

    def buy(self, entry_price: float, sl: float, tp: float, lot_size: float):
        self._open_position('buy', entry_price, sl, tp, lot_size)

    def sell(self, entry_price: float, sl: float, tp: float, lot_size: float):
        self._open_position('sell', entry_price, sl, tp, lot_size)
