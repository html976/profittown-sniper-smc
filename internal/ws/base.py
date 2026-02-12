import os
import asyncio
import json
from asyncio import Task
import websockets

class BaseWebsocketClient:
    _listener_task: Task | None = None

    def __init__(self):
        self._uri = None
        self._connection = None
        self._handler_dispatcher = None

    async def connect(self):
        """Establishes the Websocket connection"""
        try:
            app_id = os.getenv('APP_ID', '1089')
            token = os.getenv('DERIV_TOKEN')
            self._uri = f"wss://ws.derivws.com/websockets/v3?app_id={app_id}"
            
            print(f"🔗 Attempting connection to: {self._uri}")
            self._connection = await websockets.connect(self._uri)
            print("✅ Websocket connection established with broker.")
            
            # Start listener BEFORE authorizing so we can hear the response
            self._listener_task = asyncio.create_task(self._listen())

            # Now authorize using the SEND method defined below
            if token:
                await self.send({"authorize": token})
                print("🔑 Authorization request sent.")

        except Exception as e:
            print(f"❌ Connection failed: {e}. Retrying in 5s...")
            await asyncio.sleep(5)
            await self.connect()

    async def send(self, message: dict):
        """THIS IS THE MISSING METHOD - DO NOT REMOVE"""
        if self._connection:
            await self._connection.send(json.dumps(message))

    async def _listen(self):
        """Listens for incoming messages"""
        while True:
            try:
                message = await self._connection.recv()
                if self._handler_dispatcher:
                    data = json.loads(message)
                    await self._handler_dispatcher(data)
            except Exception:
                break

    async def close(self):
        if self._listener_task:
            self._listener_task.cancel()
        if self._connection:
            await self._connection.close()
