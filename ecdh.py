#!/usr/bin/env python3

from ecdsa import ECDH, NIST256p
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class C_ECDH:
    def __init__(self):
        """
        """
        self.ecdh = ECDH(curve=NIST256p)
        self.ecdh.generate_private_key()

    def get_public_key(self):
        """
        """
        return self.ecdh.get_public_key().to_pem()


    def generate_secret(self, peer_public_key):
        """
        """

        """
        with open("remote_public_key.pem") as e:
            remote_public_key = e.read()
        """

        self.ecdh.load_received_public_key_pem(peer_public_key)
        self.b_secrets = self.ecdh.generate_sharedsecret_bytes()


    def encrypt(self, data) -> bytes:
        vector = get_random_bytes(AES.block_size)

        cipher = AES.new(self.b_secrets, AES.MODE_CBC, vector)

        return vector + cipher.encrypt(pad(data.encode(),  AES.block_size))


    def decrypt(self, data: bytes) -> bytes:
        iv = data[:16]
        data = data[16:]

        decryption_cipher = AES.new(self.b_secrets, AES.MODE_CBC, iv)

        return unpad(decryption_cipher.decrypt(data), AES.block_size)


if __name__ == "__main__":
    client1 = C_ECDH()
    client2 = C_ECDH()

    client1_public_key = client1.get_public_key()

    client2_secrets = client2.generate_secret(client1_public_key)
    client1_secrets = client1.generate_secret(client2.get_public_key())

    text = "hello world"

    e_text_client1 = client1.encrypt(text)
    e_text_client2 = client2.encrypt(text)

    assert(client1.decrypt(e_text_client1) == client2.decrypt(e_text_client2))
