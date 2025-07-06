import asyncio

from shared.utils.helpers import generate_random_number

from . import handlers
from .base import BaseWebsocketClient


class TradingWebsocketClient(BaseWebsocketClient):
    """
    Application-specific client that maps message topics to handlersS
    """

    _pending_requests = {}

    def __init__(self, uri):
        super().__init__(uri)

        # The 'dispatcher' maps topics to the functions that handle them
        self._handlers = {"price_tick": handlers.handle_price_tick}

        # Set dispatcher for the base client to use
        self.set_handler_dispatcher(self._dispatch_message)

    async def _dispatch_message(self, data: dict):
        """Finds the correct handler based on the message topic."""
        topic = data.get("topic")
        handler = self._handlers.get(topic)

        if handler:
            await handler(data)

        else:
            print(f"Warning: No handler for topic: '{topic}'")

    async def tick_history(self, request_payload: dict):
        """Collect historical candle history"""

        # Create a unique ID  and a future to wait for the results
        request_id = generate_random_number()
        future = asyncio.get_running_loop().create_future()

        # Add the ID to the request and store the future
        request_payload["req_id"] = request_id
        self._pending_requests[request_id] = future

        try:
            # Send the request
            await self.send(request_payload)

            # Wait for the listener to receive the matching response
            response = await asyncio.wait_for(future, timeout=10)
            return response
        finally:
            # Clean up in case of timeout or other errors
            self._pending_requests.pop(request_id, None)
