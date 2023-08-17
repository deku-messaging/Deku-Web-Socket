#!/usr/bin/env python3

import asyncio
import websockets
import logging

import json
import sec_ecdh
import base64

import uuid

logging.basicConfig(level='DEBUG')

def generate_random_uuid():
    return uuid.uuid4()


with open("sample.json", "r") as f:
    data = json.load(f)

d_websockets = {}

class c_socket:
    def __init__(self, session_id, websocket):
        self.session_id = session_id
        self.websocket = websocket

    def set_ecdh(self, ecdh):
        self.ecdh = ecdh

    def get_socket(self):
        return self.websocket

async def soc_con(websocket, path):
    logging.debug("+ New client connection")

    try:
        session_id = str(generate_random_uuid())

        # browser client should attach url to this 
        data = {"session_id":session_id}

        d_websockets[session_id] = c_socket(session_id, websocket)
        logging.info("+ sending: %s", data)

        await websocket.send(json.dumps(data))

    except Exception as error:
        logging.exception(error)

    else:
            try:
                while True:
                        message = await websocket.recv()
                        message = json.loads(message)

                        logging.info("+ received: %s", message)

                        if 'session_id' in message and 'for_session_id' in message and 'public_key' in message:
                            ecdh = sec_ecdh.C_ECDH()

                            ecdh.generate_secret(message['public_key'])
                            d_websockets[message['for_session_id']].set_ecdh(ecdh)

                            try:
                                data = {"public_key":ecdh.get_public_key().decode(), 
                                        "for_session_id":message['for_session_id']}
                                # await d_websockets[message['']].get_socket().send(json.dumps(data))
                                await websocket.send(json.dumps(data))
                            except Exception as error:
                                logging.exception(error)

                        if 'session_id' in message and 'for_session_id' in message and 'data' in message:
                            try:
                                data = base64.b64decode(message['data'].encode())
                                data = d_websockets[message['for_session_id']].get_ecdh().decrypt(message['data'])
                                data = {"from_session_id":message['session_id'], "data":data}

                                await d_websockets[message['for_session_id']].get_socket().send(json.dumps(data))
                            except Exception as error:
                                logging.exception(error)

                        if 'session_id' in message and 'to_session_id' in message and 'data' in message:
                            """
                            """
                            await d_websockets[message['to_session_id']].get_socket().send(message['data'])

            except Exception as error:
                logging.exception(error)
            finally:
                if session_id in d_websockets:
                    del d_websockets[session_id]

            # await websocket.send(json.dumps(data))

asyncio.get_event_loop().run_until_complete(websockets.serve(soc_con, "0.0.0.0", 16000))
asyncio.get_event_loop().run_forever()
