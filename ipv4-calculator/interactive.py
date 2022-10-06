from classes import Result
from calculator_lib import cidr_calculator, is_valid_ipv4, is_valid_cidr


def main():
    # Obter o IP que o usuário digitou e verificar se é um IP válido.
    valid_input = False
    while not valid_input:
        ip = input("Enter the ip address (e.g. 144.255.10.2): \n")
        if ip and is_valid_ipv4(ip):
            valid_input = True
        else:
            print("Invalid ip address. Try an address like 123.321.123.321")

    # Caso seja um IP válido, obter o CIDR que o usuário digitou.
    valid_input = False
    cidr = None
    while not valid_input:
        cidr = input("Enter the CIDR (e.g. 24): \n")
        if cidr and is_valid_cidr(cidr):
            valid_input = True
            cidr = int(cidr)
        else:
            print("Invalid CIDR. Try a number between 0 and 32")

    # Calcular o resultado e imprimir o resultado.
    result: Result = cidr_calculator(ip, cidr)
    print(result)


if __name__ == "__main__":
    main()
