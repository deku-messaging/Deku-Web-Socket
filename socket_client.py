#!/usr/bin/env python3

import websocket
import _thread
import time
import rel
import json
import logging
import sec_ecdh
import base64

logging.basicConfig(level='INFO')

ec = sec_ecdh.C_ECDH()

sample_session_string = "https://staging.smswithoutborders.com:1234567890987654321"
sample_token_string = "1234567890987654321"

session_id = "12345"

def on_message(ws, message):
    # print(message)
    message = json.loads(message)

    if 'session_id' in message:
        session_id = message['session_id']
        logging.info("+ new session id began: %s", session_id)

    if 'from_session_id' in message:
        logging.info("+ new client message: %s", message)

    """
    if 'session_id' in message:
        message['url'] = "https://staging.smswithoutborders.com"
        logging.info("+ session init: %s", message)
    """

    """
    elif 'new_session' in message and 'data' in message:
        logging.info("+ peer msg: %s", message)

    else:
        logging.info("+ message: %s", message)
    """


def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

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
