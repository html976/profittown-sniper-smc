import asyncio
import websockets
import json

import logging


class BaseWebsocketClient:
    """Handles the low-level WebSocket connection and message loop"""

    def __init__(self, uri):
        self._uri = uri
        self._connection = None
        self._handler_dispatcher = None

    async def connect(self):
        """Establishes the Websocket connection"""
        try:
            self._connection = await websockets.connect(self._uri)
            print("Websocket connection established.")
            # Start the listener loop as a concurrent task
            asyncio.create_task(self._listen())
        except (websockets.exceptions.ConnectionClosedError, OSError) as e:
            print(f"Connection failed: {e}. Retrying...")
            await asyncio.sleep(5)
            await self.connect()

    def set_handler_dispatcher(self, dispatcher):
        """Sets the dispathcer function that will process messaages."""
        self._handler_dispatcher = dispatcher

    async def _listen(self):
        """Listens for incomming messages and passes them to the dispatcher"""
        while True:
            try:
                message = await self._connection.recv()
                if self._handler_dispatcher:
                    data = json.loads(message)
                    # Let the dispatcher handle the data
                    await self._handler_dispatcher(data)
            except websockets.exceptions.ConnectionClosedError:
                print("Connection lostt. Reconnecting...")
                await self.connect()
                break  # Exit this loop, a new one start on reconnect

    async def send(self, message: dict):
        """Sends a JSON message to the server"""
        if self._connection:
            await self._connection.send(json.dumps(message))

    async def close(self):
        """Closes the Websocket connection"""
        if self._connection:
            await self._connection.close()
            print("Websoocket connection closed")
