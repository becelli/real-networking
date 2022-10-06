import socket, sys, time, struct
import concurrent.futures as futures

MAX_TIME_IN_SEC = 30

# Dicionário de protocolos. Será utilizada para
# identificar o protocolo a partir do número de porta.
PROTOCOL_MAP = {
    6: "TCP",
    17: "UDP",
    20: "FTP",
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTP",
    587: "SMTP",
    993: "IMAP",
    995: "POP3",
}


# Classe auxiliar para controlar o número de ocorrências
# de um protocolo em um determinado intervalo de tempo.
class Counter:
    def __init__(self, time_start):
        # Ao "iniciar" o contador, o tempo de início é definido
        # como o tempo atual.
        self.time_start = time_start
        # O dicionário de ocorrências é inicializado com zeros.
        self.occurrence = {}
        for i in range(MAX_TIME_IN_SEC):
            self.occurrence[i] = 0

    def inc(self):
        # Incrementa o número de ocorrências do protocolo.
        # O número de ocorrências é definido pelo número de segundos
        # desde o início do intervalo.
        time_now = time.time()
        # Coerção para inteiro pois alguns SOs podem retornar frações de segundos.
        time_diff = int(time_now - self.time_start)
        if time_diff < MAX_TIME_IN_SEC:
            self.occurrence[time_diff] += 1


def sniff(IPPROTO_USED, time_start) -> dict:
    # Dicionário que armazenará os protocolos e seus respectivos
    # números de ocorrências.
    protocols = {
        "FTP": Counter(time_start),
        "SSH": Counter(time_start),
        "TELNET": Counter(time_start),
        "SMTP": Counter(time_start),
        "DNS": Counter(time_start),
        "HTTP": Counter(time_start),
        "POP3": Counter(time_start),
        "IMAP": Counter(time_start),
    }

    try:  # Tentar criar um socket.
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, IPPROTO_USED)
        """
        socket.AF_INET indica que o socket será de IPv4.
        socket.SOCK_RAW indica que o socket estará escutando os pacotes
        de rede, antes de serem processados pelo kernel. (por isso, RAW)
        socket.IPPROTO_TCP indica que o socket irá tratar somente
        pacotes TCP.
        """
    except:
        sys.exit()  # Se não conseguir, sai do programa.

    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    # IP_HDRINCL indica que o socket irá tratar os pacotes de rede
    # como se eles estivessem contidos no cabeçalho IP.
    s.bind(("", 0))
    # Binda o socket a uma porta aleatória.

    # Enquanto o tempo de captura for menor que o
    # tempo máximo, o socket irá receber pacotes de rede.
    while (time.time() - time_start) < MAX_TIME_IN_SEC:
        packet, _ = s.recvfrom(65565)  # Recebe o pacote de rede.
        ip_header = packet[0:20]  # Pega o cabeçalho IP (20 bytes).
        iph = struct.unpack("!BBHHHBBH4s4s", ip_header)
        """
        Desempacota o cabeçalho binário do protocolo IP. Irá dividir o
        cabeçalho IP em uma tupla (que logo será extraída), consoante a
        quantidade de bytes de cada campo. Tem-se que:
        ! indica que os bytes serão interpretados como big-endian. (padrão de rede)
        B: 1 byte, H: 2 bytes e 4s: 4 bytes
        """
        version_ihl = iph[0]  # Byte que indica a versão e o tamanho do cabeçalho.
        version = version_ihl >> 4  # Versão do protocolo IP.
        iph_length = (version_ihl & 0xF) * 4  # Tamanho do cabeçalho IP.
        ttl = iph[5]  # Tempo de vida do pacote.
        protocol = iph[6]  # Protocolo de transporte (TCP, UDP, ICMP, etc.)
        s_addr = socket.inet_ntoa(iph[8])  # Endereço de origem.
        d_addr = socket.inet_ntoa(iph[9])  # Endereço de destino.

        if protocol == 6:  # Protocolo TCP.
            t = struct.unpack("!HHLLBBHHH", packet[iph_length : iph_length + 20])
            # Desempacota o cabeçalho TCP. Segue a mesma lógica do cabeçalho IP.
            # B: 1 byte, H: 2 bytes e, neste caso, L: 4 bytes
            source_port = t[0]  # Porta de origem.
            dest_port = t[1]  # Porta de destino.
            sequence = t[2]  # Número de sequência do pacote.
            ack = t[3]  # Número de sequência do ACK.
            doff_reserved = t[4]  # Deslocamento e espaço reservado
            tcph_length = doff_reserved >> 4  # Tamanho do cabeçalho TCP.

            # Verifica se o protocolo é um dos desejados e incrementa seu número.
            if source_port in PROTOCOL_MAP:  # Caso do protocolo na porta de origem.
                protocols[PROTOCOL_MAP[source_port]].inc()
                print(f"Protocol {PROTOCOL_MAP[source_port]} from {s_addr} to {d_addr}")

            if dest_port in PROTOCOL_MAP:  # Caso do protocolo na porta de destino.
                protocols[PROTOCOL_MAP[dest_port]].inc()
                print(f"Protocol {PROTOCOL_MAP[dest_port]} from {s_addr} to {d_addr}")

        elif protocol == 17:  # Protocolo UDP
            u = struct.unpack("!HHHH", packet[iph_length : iph_length + 8])
            # Desempacota o cabeçalho UDP. Segue a mesma lógica do cabeçalho IP.
            # Neste caso, é um cabeçalho mais simples, de apenas 8 bytes.
            source_port = u[0]  # Porta de origem.
            dest_port = u[1]  # Porta de destino.
            length = u[2]  # Tamanho do pacote.
            checksum = u[3]  # Checksum.

            # Verifica se o protocolo é um dos desejados e incrementa seu número.
            if source_port in PROTOCOL_MAP:  # Caso do protocolo na porta de origem.
                protocols[PROTOCOL_MAP[source_port]].inc()
                print(f"Protocol {PROTOCOL_MAP[source_port]} from {s_addr} to {d_addr}")

            if dest_port in PROTOCOL_MAP:  # Caso do protocolo na porta de destino.
                protocols[PROTOCOL_MAP[dest_port]].inc()
                print(f"Protocol {PROTOCOL_MAP[dest_port]} from {s_addr} to {d_addr}")

    return protocols


def plot_to_file(protocols, type):  # Função que plota os gráficos.
    import matplotlib.pyplot as plt

    # Configurações do gráfico.
    plt.style.use("ggplot")
    plt.figure(figsize=(15, 5), dpi=300)
    plt.title(f"Protocols over time in {type}/IP")
    plt.xlabel("Time in seconds")
    plt.ylabel("Occurrence")
    plt.xticks(range(MAX_TIME_IN_SEC))

    # Para cada procolo/ocorrência, plota uma linha.
    for protocol, occurences in protocols.items():
        sec, occ = zip(*occurences.occurrence.items())
        plt.plot(sec, occ, label=protocol)
        plt.scatter(sec, occ)

    # Salva-se o gráfico em um arquivo.
    plt.legend()
    plt.savefig(f"graph-{type}.png")


if __name__ == "__main__":
    ip_protocols = [socket.IPPROTO_TCP, socket.IPPROTO_UDP]  # Protocolos de IP.
    time_start = time.time()  # Inicia o tempo de captura.
    # Executa o sniffer para cada protocolo de IP, em paralelo.
    with futures.ThreadPoolExecutor(max_workers=len(ip_protocols)) as executor:
        future_protocols = {
            executor.submit(sniff, ip_protocol, time_start): ip_protocol
            for ip_protocol in ip_protocols
        }  # Soicita a execução para cada protocolo.

        # Assim que completado, extrai os resultados.
        for future in futures.as_completed(future_protocols):
            # Obtém o protocolo.
            ip_protocol = PROTOCOL_MAP[future_protocols[future]]
            # Obtém o resultado.
            protocols = future.result()
            # Plota o gráfico.
            plot_to_file(protocols, ip_protocol)
