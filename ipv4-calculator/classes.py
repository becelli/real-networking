# fmt: off
from dataclasses import dataclass


# Classe para aramzenar os resultados (Struct)
@dataclass
class Result:
    ip: str
    mask: str
    network: str
    broadcast: str
    first_host: str
    last_host: str
    total_hosts: int

    def __str__(self):
        return f"IP: {self.ip}\nMask: {self.mask}\nNetwork: {self.network}\nBroadcast: {self.broadcast}\nFirst Host: {self.first_host}\nLast Host: {self.last_host}\nTotal Hosts: {self.total_hosts}\n"


@dataclass
class TestCidrCalculator:
    name: str
    ipv4: str
    cidr: int
    expected: Result

    def assert_results(self, result: Result):
        # "Asserta" que os resultados são iguais. Se não forem,
        # imprime o resultado esperado e o resultado obtido.
        for attr in [ "ip", "mask", "network", "broadcast", "first_host", "last_host", "total_hosts"]:
            try:
                assert getattr(result, attr) == getattr(self.expected, attr)
            except AssertionError as e:
                err = f"{attr} mismatch: {getattr(result, attr)} (result) != {getattr(self.expected, attr)} (expected)\n\n"
                raise AssertionError(err) from e

    def __str__(self):
        return f"{self.name}: {self.ipv4}/{self.cidr}"
