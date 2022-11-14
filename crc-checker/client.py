import socket
from utils import mod2div, key, string_to_binary


class Client:
    def __init__(self, host, port):
        # Cria um Socket UDP e o associa a um endereço e porta
        self.host: str = host
        self.port: int = port
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect((self.host, self.port))
        # Define a chave de verificação
        self.key = key

    def encode(self: object, msg: bytes) -> str:
        # Codifica a mensagem
        key_length: int = len(self.key)
        padding: str = '0' * (key_length - 1)
        data_key: str = msg + padding
        # Calcula o resto da divisão
        remainder: str = mod2div(data_key, self.key)
        # Adiciona o resto ao final da mensagem
        message: str = msg + remainder
        return message

    def encode_with_error(self, msg: str) -> str:
        message = self.encode(msg)
        # Invert the first bit
        inverted_bit: str = '0' if message[0] == '1' else '1'
        corrupted_message: str = inverted_bit + message[1:]
        return corrupted_message

    def send(self, message: str) -> None:
        # Envia a mensagem para o servidor
        self.socket.sendall(message.encode())

    def run(self) -> None:
        # Executa o cliente
        try:
            while True:
                # Lê a mensagem do usuário
                message: str = input("Digite a mensagem: ")
                # Codifica a mensagem
                binary_message: str = string_to_binary(message)

                # Pergunta seed usuário se deseja enviar a mensagem com erro
                should_send_error: str = input(
                    "Deseja enviar com erro? (s/n): ")

                # se sim, envia a mensagem com erro
                if should_send_error[0].lower() in ['s', 'sim', 'y', 'yes']:
                    message = self.encode_with_error(binary_message)
                else:  # se não, envia a mensagem sem erro
                    message = self.encode(binary_message)

                # Envia a mensagem para o servidor
                self.send(message)

        except KeyboardInterrupt:
            # Fecha o socket
            print("Client stopped")
            self.socket.close()


if __name__ == "__main__":
    port = 5000
    host = '127.0.0.1'
    client = Client(host, port)
    client.run()
