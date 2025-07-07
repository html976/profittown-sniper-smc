async def handle_tick_history(data: dict):
    """
    Processes incoming price candle data.
    """
    request_id = data["req_id"]
    candles = data["candles"][0]
    pip_size = data["pip_size"]

async def handle_error(data: dict):
    """Handles error messages from the server."""
    pass
