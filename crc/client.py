import crc
import server
import client
import socket


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((self.host, self.port))

    def send(self, data):
        self.sock.send(data)

    def recv(self):
        return self.sock.recv(1024)

    def close(self):
        self.sock.close()

    def __del__(self):
        self.close()


# Path: crc/server.py


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

    def recv(self):
        return self.sock.recv(1024)

    def send(self, data):
        self.sock.send(data)

    def close(self):
        self.sock.close()

    def __del__(self):
        self.close()


def data_to_32bits_blocks(data):
    blocks = []
    for i in range(0, len(data), 4):
        blocks.append(data[i:i+4])
    return blocks


def crc16(data):
    crc = 0xFFFF
    for block in data_to_32bits_blocks(data):
        crc ^= int.from_bytes(block, 'little')
        for i in range(16):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc.to_bytes(2, 'little')


def main():
    server = server.Server('127.0.0.1', 5000)
    client = client.Client('127.0.0.1', 5000)

    data = b'Hello World'
    crc = crc.crc16(data)

    client.send(data)
    client.send(crc)

    data = server.recv()
    crc = server.recv()
