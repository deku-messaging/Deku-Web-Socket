#!/usr/bin/env python3
import websocket
import _thread
import time
import rel
import json
import logging
import ecdh
import base64
import logging
logging.basicConfig(level='INFO')


"""
1. requires connection url to start connection - gotten from qr code
2. connects to server and gets a session_id, also informs server which
session it is communicating with for_session_id
3. encryption happens between session_id and server
4. once encryption is setup, browser client is informed it can now communicate with session_id
5. information is sent to the browser client decrypted - using session_id
6. information is received from the browser in an encrypted way
"""

for_session_id = "12345"

ec = C_ECDH()

def on_message(ws, message):
    message = json.loads(message)
    """
    """
    if 'public_key' in message:
        ec.generate_secret(message['public_key'])

    if 'session_id' in message:
        session_id = message['session_id']

    logging.info(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    """
    """
    public_key = ec.get_public_key().decode()
    data = {
            "for_session_id":for_session_id,
            "public_key":public_key
            }
    ws.send(json.dumps(data))

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://staging.smswithoutborders.com:16000",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
