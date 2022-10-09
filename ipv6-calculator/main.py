import re
import numpy as np


def fill_ipv6(ip):
    # Preenche o endereço IPv6 com zeros, retornando uma string com 8 grupos de 4 dígitos, separados por dois pontos.

    groups = ip.split(':')
    groups_count = len(groups)
    number_of_zeros = 8 - groups_count

    # Se o endereço IPv6 não tiver 8 grupos, cria-os preenchendo com zeros.
    for _ in range(number_of_zeros):
        groups.insert(groups.index(''), '0000')

    # Se os zeros a esquerda foram abrevidados, preenche-os com zeros.
    for i, group in enumerate(groups):
        if len(group) < 4:
            groups[i] = group.zfill(4)

    return ':'.join(groups)


def is_valid_ipv6_address(address) -> bool:
    # Verifica se o endereço IPv6 é válido.

    # Verifica se há ambiguidade na abreviação de zeros.
    splitted = address.split('::')
    if len(splitted) > 2:
        return False

    # Preenche o endereço IPv6 com zeros, retornando uma string com 8 grupos de 4 dígitos, separados por dois pontos.
    filled = fill_ipv6(address)
    # Depois do fill, o regex fica muito mais simples heheheh.
    result = re.match(r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$', filled)
    return result is not None  # Retorna True ou False.


def ipv6_to_bytes(address) -> bytes:
    # Converte o endereço IPv6 para bytes.
    filled = fill_ipv6(address)
    groups = filled.split(':')
    return b''.join([int(group, 16).to_bytes(2, 'big') for group in groups])


def bytes_to_ipv6(address) -> str:
    # Converte os bytes para endereço IPv6.
    groups = [address[i:i + 2] for i in range(0, len(address), 2)]
    return ':'.join([group.hex() for group in groups])


def bytes_to_int(address) -> int:
    # Converte os bytes para int.
    return int.from_bytes(address, 'big')


def int_to_bytes(address) -> bytes:
    # Converte o int para bytes.
    return address.to_bytes(16, 'big')


def divide(address, cidr, subnets, is_rightmost):
    # Obter a quantidade de bits necessários para representar o número de sub-redes.
    bits = int(np.ceil(np.log2(subnets)))
    # Transformar o endereço IPv6 em um inteiro para facilitar as operações.
    ip_as_bytes = ipv6_to_bytes(address)
    ip_as_int = bytes_to_int(ip_as_bytes)

    # Quantidade de bits que serão divididos.
    diff = 128 - cidr

    addresses = []
    for i in range(subnets):
        # contador em binário.
        counter = format(i, f'0{bits}b')
        # Para o left-most, inverte o contador.
        counter = counter if is_rightmost else counter[::-1]
        # Cria a máscara.
        mask = int(counter + '0' * diff, 2)
        # Aplica a máscara (OR bit a bit).
        or_result = ip_as_int | mask
        # Converte o resultado para bytes.
        as_bytes = int_to_bytes(or_result)
        # Converte os bytes para endereço IPv6 + CIDR.
        ip = bytes_to_ipv6(as_bytes)
        addr = f'{ip}/{cidr}'
        addresses.append(addr)

    return addresses


def network_division(address, subnet_cidr, subnets) -> list:
    # Divide a rede em sub-redes, utilizando o método rightmost e leftmost.
    right_most = divide(address, subnet_cidr, subnets, is_rightmost=True)
    left_most = divide(address, subnet_cidr, subnets, is_rightmost=False)
    return right_most, left_most


def main():
    #  get address and CIDR
    while True:
        address, cidr = input(
            'Insira um endereço IPv6 com um CIDR. Ex: 2001:db1::/32.\n>>> ').strip().split('/')
        if is_valid_ipv6_address(address):
            break
    cidr = int(cidr)

    # get number of subnets.
    while True:
        subnets = int(input('Digite o número de sub-redes: '))
        bits = int(np.ceil(np.log2(subnets)))
        cidr_subnets = cidr + bits
        if cidr_subnets > 128:
            print('O número de sub-redes é muito grande.')
        else:
            break

    right, left = network_division(address, cidr_subnets, subnets)

    print(f"Criando {subnets} sub-redes a partir de {address}/{cidr}...")
    print(f"Sub-redes à direita (rightmost)")
    for i, subnet in enumerate(right):
        print(f"Sub-rede {i + 1}: {subnet}")
    print(f"Sub-redes à esquerda (leftmost)")
    for i, subnet in enumerate(left):
        print(f"Sub-rede {i + 1}: {subnet}")


if __name__ == '__main__':
    main()
