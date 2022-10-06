from classes import Result


def is_valid_ipv4(ip: str) -> bool:
    """Checar se o ip é válido"""
    if ip is None:
        return False
    try:
        ip = ip.split(".")
        if len(ip) != 4:  # Checar se tem 4 octetos
            return False
        for i in ip:
            if int(i) < 0 or int(i) > 255:  # Checar se os octetos são válidos
                return False
        return True
    except ValueError:  # Se alguma coisa errada acontecer, retornar False
        return False


def is_valid_cidr(cidr: str) -> bool:
    """Checar se o cidr é válido"""
    try:
        value = int(cidr)
        if value is None or value < 0 or value > 32:
            return False
        return True
    except ValueError:
        return False


def bin2ip(bin_ip: str) -> str:
    """Converte um endereço binário para um endereço ip"""
    if bin_ip is None:
        return None
    return ".".join([str(int(bin_ip[i : i + 8], 2)) for i in range(0, 32, 8)])


def ip2bin(ip: str) -> str:
    """Converte um endereço ip para um endereço binário"""
    if ip is None:
        return None
    return "".join(map(lambda x: bin(int(x))[2:].zfill(8), ip.split(".")))


def cidr2bin_mask(cidr: int) -> str:
    """Converte uma notação CIDR para uma máscara binária"""
    if cidr is None or cidr < 0 or cidr > 32:
        return None
    mask = "".join(["1"] * cidr + ["0"] * (32 - cidr))
    return mask


def inv_bin(bin_ip: str) -> str:
    """Inverte a máscara binária, mapeando 0 para 1 e 1 para 0"""
    return "".join(map(lambda x: "1" if x == "0" else "0", bin_ip))


def get_network_binaddr(ip_bin, mask_bin):
    """Calcula o endereço de rede"""
    if not (ip_bin and mask_bin):
        return None
    return "".join(map(lambda x, y: str(int(x) & int(y)), ip_bin, mask_bin))


def get_broadcast_binaddr(ip_bin, mask_bin):
    """Calcula o endereço de broadcast"""
    if not (ip_bin and mask_bin):
        return None
    cast = "".join(map(lambda x, y: str(int(x) | int(y)), ip_bin, inv_bin(mask_bin)))

    # Obter o endereço de rede para checar se o endereço de broadcast é igual ao endereço de rede
    net = get_network_binaddr(ip_bin, mask_bin)
    if net == cast:  # Se são iguais, não há broadcast.
        return None
    return cast


def get_first_host_binaddr(network_bin, broadcast_bin):
    """Calcula o endereço binário do primeiro host"""
    # Se não há endereço de rede ou de broadcast, não há primeiro host
    if not (network_bin and broadcast_bin):
        return None
    # Se o endereço de rede é igual ao de broadcast ou é 255.255.255.255, não há primeiro host
    if network_bin == "1" * 32 or network_bin == broadcast_bin:
        return None

    first_bin = None
    network_bin = network_bin[:]  # Cópia para não alterar o endereço de rede.

    """
    i. Para cada bit, da direita para a esquerda, se o bit é 1,
    substitua por 0.
    ii. Se o bit for 0, substitua por 1 e saia do loop. 

    A primeira operação é desnecessária neste caso, mas caso aceite-se máscaras fora do padrão CIDR,
    por exemplo, uma máscara ímpar (255.255.255.1), o endereço de rede comecará em .1, e o primeiro host
    será o endereço de rede + 1, isto é, .2.

    """
    for i, bit in enumerate(network_bin[::-1]):
        if bit == "0":
            first_bin = network_bin[: 32 - i - 1] + "1" + network_bin[32 - i :]
            break
        else:
            network_bin = network_bin[: 32 - i - 1] + "0" + network_bin[32 - i :]

    # Verificar se o primeiro host é igual ao endereço de broadcast
    # Apenas ocorre se há menos que 2 endereços, sem desconsiderar os endereços de rede e broadcast.
    if (
        first_bin == "255.255.255.255"
        or first_bin == broadcast_bin
        or network_bin == broadcast_bin
    ):  # Verificações em que não há primeiro host ou anularia o endereço de broadcast
        return None

    return first_bin if first_bin != network_bin else None


def get_last_host_binaddr(broadcast_bin, network_bin):
    """Calcula o endereço binário do último host"""
    # Se não há endereço de rede ou de broadcast, não há último host
    if not (broadcast_bin and network_bin):
        return None
    # Se o endereço de broadcast é igual ao de rede, não há último host
    if broadcast_bin == "0" * 32 or broadcast_bin == network_bin:
        return None

    last_bin = None
    broadcast_bin = broadcast_bin[:]  # Cópia para não alterar o endereço de broadcast.
    """
    i. Para cada bit, da direita para a esquerda, se o bit é 0,
    substitua por 1.
    ii. Se o bit for 1, substitua por 0 e saia do loop.

    Realiza a mesma lógica do primeiro host, porém, diminuindo o endereço de broadcast.
    """
    for i, bit in enumerate(broadcast_bin[::-1]):
        if bit == "1":
            last_bin = broadcast_bin[: 32 - i - 1] + "0" + broadcast_bin[32 - i :]
            break
        else:
            broadcast_bin = broadcast_bin[: 32 - i - 1] + "1" + broadcast_bin[32 - i :]

    # Verificações em que não há último host ou anularia o endereço de rede.
    if last_bin == "0.0.0.0" or network_bin == broadcast_bin or last_bin == network_bin:
        return None

    return last_bin


def get_host_count(first_host_bin, last_host_bin):
    """Calcula o número de host e converte para inteiro"""
    if not (first_host_bin and last_host_bin):
        return 0

    # Zip para fazer o cálculo de bit a bit
    zipped = zip(first_host_bin[::-1], last_host_bin[::-1])
    counter = 0
    for i, (bit1, bit2) in enumerate(zipped):
        if bit1 != bit2:  # Caso o bit seja diferente, o número de host é incrementado
            counter += 2**i
    return int(counter) - 1  # Subtrai 1 para não contar o endereço de rede


def cidr_calculator(ipv4: str, cidr: int) -> Result:
    """Função geral que agrega todas as funções anteriores,
    calcula os endereços de rede, broadcast, primeiro e
    último host e retorna um objeto Result"""
    if not is_valid_ipv4(ipv4) or not is_valid_cidr(cidr):
        return None

    ip_bin = ip2bin(ipv4)
    mask_bin = cidr2bin_mask(cidr)
    network_bin = get_network_binaddr(ip_bin, mask_bin)
    broadcast_bin = get_broadcast_binaddr(ip_bin, mask_bin)
    first_host_bin = get_first_host_binaddr(network_bin, broadcast_bin)
    last_host_bin = get_last_host_binaddr(broadcast_bin, network_bin)
    host_count = get_host_count(first_host_bin, last_host_bin)

    results = [mask_bin, network_bin, broadcast_bin, first_host_bin, last_host_bin]
    # Converte para representação de IP
    mask, network, broadcast, first_host, last_host = map(bin2ip, results)
    return Result(
        ip=ipv4,
        mask=mask,
        network=network,
        broadcast=broadcast,
        first_host=first_host,
        last_host=last_host,
        total_hosts=host_count,
    )
