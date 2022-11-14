
key = "1001"


def xor(a: str, b: str) -> str:
    # Realiza uma operação XOR entre duas strings de bits
    result = []
    for i in range(1, len(b)):
        res = '0' if a[i] == b[i] else '1'
        result.append(res)
    return ''.join(result)


def mod2div(divident: str, divisor: str) -> str:

    # Número de bits a ser aplicado XOR
    pointer = len(divisor)
    # Obtendo os primeiros bits do dividendo
    step = divident[:pointer]
    for i in range(pointer, len(divident)):
        if step[0] == '1':
            # Aplicando XOR e deslocando 1 bit
            step = xor(divisor, step) + divident[i]
        else:   # Se o bit mais significativo for 0
            # Se o bit mais significativo do dividendo (ou a parte
            # usada em cada etapa) for 0, a etapa não pode usar o
            # divisor regular; em vez disso, ele usa o divisor
            # com todos os bits definidos como 0.
            step = xor('0' * pointer, step) + divident[i]

    # Aplicando XOR para o último passo
    if step[0] == '1':
        step = xor(divisor, step)
    else:
        step = xor('0' * pointer, step)

    return step


def string_to_binary(message: str) -> str:
    # Converter mensagem para binário
    binary = ''.join(format(ord(i), '08b') for i in message)
    return binary


def binary_to_string(binary: str) -> str:
    # Converter binário para mensagem
    message = ''.join(chr(int(binary[i:i+8], 2))
                      for i in range(0, len(binary), 8))
    return message
