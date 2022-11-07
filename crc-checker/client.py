from crc_calculator import CRC32
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


def main():
    client = Client('localhost', 5000)
    data = input("Enter data: ")
    crc = CRC32(data)
    client.send(crc.encode())
    print("Sent: {}".format(crc.encode()))
    print("Received: {}".format(client.recv()))
    client.close()

if __name__ == '__main__':
    main()


