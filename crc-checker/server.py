import socket
from utils import mod2div, key, binary_to_string


class Server:
    def __init__(self: object, host: str, port: int) -> None:
        # Cria um Socket UDP e o associa a um endereço e porta
        self.host: str = host
        self.port: int = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        # Define a chave de verificação
        self.key = key

    def verify(self: object, msg: str) -> bool:
        # Verifica se a mensagem recebida é válida
        key_length: int = len(self.key)
        padding: str = '0' * (key_length - 1)
        data_key: str = msg + padding
        # Calcula o resto da divisão
        remainder: str = mod2div(data_key, self.key)
        # Verifica se o resto é 0
        return remainder == '0' * (key_length - 1)

    def decode(self: object, msg: str) -> str:
        # Decodifica a mensagem recebida
        key_length: int = len(self.key)
        padding: str = '0' * (key_length - 1)
        data_key: str = msg + padding
        # Calcula o resto da divisão
        remainder: str = mod2div(data_key, self.key)
        message_without_padding: str = msg[:-len(remainder)]
        # Converte a mensagem para string
        message = binary_to_string(message_without_padding)
        return message

    def receive(self) -> str:
        # Recebe a mensagem do cliente
        data, _ = self.socket.recvfrom(1024)
        return data.decode()

    def run(self) -> None:
        # Executa o servidor
        try:
            while True:
                # Recebe a mensagem do cliente
                message: str = self.receive()

                # Verifica se a mensagem é válida
                if self.verify(message):
                    print("Mensagem transmitida sem erros")
                else:
                    print("Mensagem transmitida com erros")

                # Decodifica a mensagem
                decoded = self.decode(message)
                print(f"Recebido: {decoded}")

        except KeyboardInterrupt:
            print("Server stopped")
            self.socket.close()


if __name__ == "__main__":
    host = '127.0.0.1'
    port = 5000
    server = Server(host, port)
    server.run()
