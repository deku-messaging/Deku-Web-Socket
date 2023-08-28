#!/usr/bin/env python3

import asyncio
import websockets
import logging
import ssl

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

                        if 'for_session_id' in message and 'public_key' in message:
                            ecdh = sec_ecdh.C_ECDH()

                            ecdh.generate_secret(message['public_key'])
                            d_websockets[session_id].set_ecdh(ecdh)

                            try:
                                data = {"public_key":ecdh.get_public_key().decode(), 
                                        "session_id":session_id}
                                await websocket.send(json.dumps(data))
                            except Exception as error:
                                logging.exception(error)
                        elif 'for_session_id' in message and 'data' in message:
                            if message['for_session_id'] in d_websockets:
                                data = {
                                        "from_session_id":session_id,
                                        "data":message['data']
                                        }
                                ws =  d_websockets[message['for_session_id']].get_socket()
                                await ws.send(json.dumps(data))
                            else:
                                logging.error("- unknown for session required!")



            except Exception as error:
                logging.exception(error)
            finally:
                if session_id in d_websockets:
                    del d_websockets[session_id]

            # await websocket.send(json.dumps(data))

import custom_configs
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile=custom_configs.config['ssl_crt'], 
        keyfile=custom_configs.config['ssl_key'])
ssl_context.load_verify_locations(custom_configs.config['ssl_cabundle'])

asyncio.get_event_loop().run_until_complete(websockets.serve(
    ws_handler = soc_con, 
    host = "0.0.0.0", 
    port = 16000, 
    ssl=ssl_context))
asyncio.get_event_loop().run_forever()
