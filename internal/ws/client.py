import asyncio
import websockets
import json
import uuid

import ssl

class WebsocketClient:
    """
    A simple client that allows sending a request and awaiting a specific response.
    """

    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self._pending_requests = {}
        self._listener_task = None

    async def connect(self):
        """Establishes the connection and starts the background listener."""
        if self.websocket:
            return

        print("Connecting to WebSocket...")

        print(self.uri)
        ssl_context = ssl.create_default_context()
        self.websocket = await websockets.connect(self.uri, ssl=ssl_context)
        self._listener_task = asyncio.create_task(self._listen())
        print("✅ Connection established.")

    async def _listen(self):
        """Listens for all messages and routes responses back to waiting requests."""
        try:
            while True:
                message = await self.websocket.recv()
                data = json.loads(message)

                # If the response has a req_id, find the waiting request and give it the data
                req_id = data.get("echo_req", {}).get("req_id")
                if req_id and req_id in self._pending_requests:
                    future = self._pending_requests.pop(req_id)
                    future.set_result(data)
                else:
                    # Optional: Handle messages that weren't requested directly (like price ticks)
                    # print(f"[unhandled] {data}")
                    pass
        except websockets.ConnectionClosed:
            print("[warning] Connection closed.")

    async def send_request(self, request_payload: dict, timeout: int = 10):
        """
        Sends a request, waits for the specific response, and returns it.
        This is the only function you need to call.
        """
        if not self.websocket:
            raise ConnectionError("Not connected to WebSocket.")

        # 1. Create a unique ID and a future to wait for the result
        req_id = 1234
        future = asyncio.get_running_loop().create_future()

        # 2. Add the ID to the request and store the future
        request_payload["req_id"] = req_id
        self._pending_requests[req_id] = future

        try:
            # 3. Send the request
            await self.websocket.send(json.dumps(request_payload))

            # 4. Wait for the listener to receive the matching response
            response = await asyncio.wait_for(future, timeout=timeout)
            return response
        finally:
            # Clean up in case of timeout or other errors
            self._pending_requests.pop(req_id, None)

    async def close(self):
        """Closes the connection."""
        if self._listener_task:
            self._listener_task.cancel()
        if self.websocket:
            await self.websocket.close()
        print("Connection closed.")
