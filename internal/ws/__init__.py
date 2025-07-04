# from .base_client import BaseWebsocketClient
# from . import handlers

# class TradingWebsocketClient(BaseWebsocketClient):
#     """
#     Application-specific client that maps message topics to handlers.
#     """
#     def __init__(self, uri):
#         super().__init__(uri)
#         # The 'dispatcher' maps topics to the functions that handle them
#         self._handlers = {
#             'price_tick': handlers.handle_price_tick,
#             'trade_update': handlers.handle_trade_update,
#             'error': handlers.handle_error
#         }
#         # Set the dispatcher for the base client to use
#         self.set_handler_dispatcher(self._dispatch_message)

#     async def _dispatch_message(self, data: dict):
#         """Finds the correct handler based on the message topic."""
#         topic = data.get('topic')
#         handler = self._handlers.get(topic)
        
#         if handler:
#             await handler(data)
#         else:
#             print(f"Warning: No handler found for topic '{topic}'")
    
#     async def subscribe_to_prices(self, symbol: str):
#         """Sends a subscription message for a specific symbol."""
#         subscription_message = {
#             "action": "subscribe",
#             "topic": "price_tick",
#             "symbol": symbol
#         }
#         await self.send(subscription_message)
#         print(f"Sent subscription request for {symbol}.")