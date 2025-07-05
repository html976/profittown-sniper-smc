async def handle_price_tick(data: dict):
    """PRocesses incoming price tick data."""
    symbol = data.get("symbol")
    price = data.get("price")
    print(f"📈Price Update: {symbol} is at {price}.")
    pass


async def handle_error(data: dict):
    """Handles error messages from the server."""
    pass    