#!/usr/bin/env python3

import websocket
import _thread
import time
import rel
import json
import logging
import ecdh
import base64

logging.basicConfig(level='INFO')

ec = ecdh.C_ECDH()

sample_session_string = "https://staging.smswithoutborders.com:1234567890987654321"
sample_token_string = "1234567890987654321"

def phone_client_sample(ws, message):
    """
    """
    if not 'public_key' in message or not 'session_id' in message:
        ec.generate_secret(message['public_key'])

        with open("sample.json", "r") as f:
            sample_data = json.load(f)

        sample_data = ec.encrypt(json.dumps(sample_data))
        sample_data = base64.b64encode(sample_data).decode()

        data = {"public_key":ec.get_public_key().decode('utf-8'),
                "data":sample_data}

        logging.info("%s", data)

        ws.send(json.dumps(data))


def on_message(ws, message):
    # print(message)
    message = json.loads(message)

    if 'session_id' in message:
        """
        """
        message['url'] = "https://staging.smswithoutborders.com"
        logging.info("+ session init: %s", message)

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

    """
    data = {"session_id":base64.b64encode(sample_session_string.encode()).decode(),
            "session_token":base64.b64encode(sample_token_string.encode()).decode()}
    logging.info(data)

    ws.send(json.dumps(data))
    """


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
