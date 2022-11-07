import socket
from crc_calculator import CRC32

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

    def recv(self):
        return self.sock.recvfrom(1024)

    def send(self, data, addr):
        self.sock.sendto(data, addr)

    def close(self):
        self.sock.close()

    def __del__(self):
        self.close()

def main():
    server = Server('localhost', 5000)
    try:
      while True:
          data, addr = server.recv()
          print("Received: {}".format(data))
          crc = CRC32(binary=data)
          is_valid = crc.validate()
          server.send(str(is_valid).encode(), addr)
          print("Sent: {}".format(is_valid))    
    except KeyboardInterrupt:
      server.close()
      exit(0)

if __name__ == '__main__':
    main()
    