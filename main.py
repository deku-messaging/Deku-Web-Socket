#!/usr/bin/env python3

import asyncio
import websockets
import logging

import json

logging.basicConfig(level='DEBUG')

with open("sample.json", "r") as f:
    data = json.load(f)

async def hello(websocket, path):
    logging.debug("+ New client connection")
    # await websocket.send("Hello, world!")
    await websocket.send(json.dumps(data))

    while True:
        message = await websocket.recv()
        # await websocket.send(f"You said: {message}")
        await websocket.send(json.dumps(data))

asyncio.get_event_loop().run_until_complete(websockets.serve(hello, "0.0.0.0", 16000))
asyncio.get_event_loop().run_forever()
