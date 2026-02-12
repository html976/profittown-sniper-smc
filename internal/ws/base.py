import os
import asyncio
import json
from asyncio import Task
import websockets

class BaseWebsocketClient:
    """Handles the low-level WebSocket connection and message loop"""
    _listener_task: Task | None = None

    def __init__(self, uri=None):
        # We allow uri to be None now because we will build it in connect()
        self._uri = uri
        self._connection = None
        self._handler_dispatcher = None

    async def connect(self):
        """Establishes the Websocket connection with dynamic App ID"""
        try:
            # 1. Pull the APP_ID from Render's environment variables
            # We use '1089' as a backup if you forgot to set the variable
            app_id = os.getenv('APP_ID', '1089')
            
            # 2. Build the correct Deriv URL structure
            self._uri = f"wss://ws.derivws.com/websockets/v3?app_id={app_id}"
            
            print(f"🔗 Attempting connection to: {self._uri}")
            self._connection = await websockets.connect(self._uri)
            print("✅ Websocket connection established with broker.")
            
            # 3. Authorize immediately after connecting
            token = os.getenv('DERIV_TOKEN')
            if token:
                await self.send({"authorize": token})
                print("🔑 Authorization request sent.")

            self._listener_task = asyncio.create_task(self._listen())
            
        except (websockets.exceptions.ConnectionClosedError, OSError) as e:
            print(f"❌ Connection failed: {e}. Retrying in 5s...")
            await asyncio.sleep(5)
            await self.connect()
