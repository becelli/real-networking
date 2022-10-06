from classes import Result, TestCidrCalculator
from calculator_lib import cidr_calculator


# Realiza testes para compovação dos cálculos obtidos pelo cidr_calculator
def main():
    tests = [
        TestCidrCalculator(
            "Test 1",
            "192.168.0.100",
            24,
            Result(
                ip="192.168.0.100",
                mask="255.255.255.0",
                network="192.168.0.0",
                broadcast="192.168.0.255",
                first_host="192.168.0.1",
                last_host="192.168.0.254",
                total_hosts=254,
            ),
        ),
        TestCidrCalculator(
            "Test 2",
            "8.8.8.8",
            16,
            Result(
                ip="8.8.8.8",
                mask="255.255.0.0",
                network="8.8.0.0",
                broadcast="8.8.255.255",
                first_host="8.8.0.1",
                last_host="8.8.255.254",
                total_hosts=2 ** (32 - 16) - 2,
            ),
        ),
        TestCidrCalculator(
            "Test 3",
            "200.145.184.166",
            19,
            Result(
                ip="200.145.184.166",
                mask="255.255.224.0",
                network="200.145.160.0",
                broadcast="200.145.191.255",
                first_host="200.145.160.1",
                last_host="200.145.191.254",
                total_hosts=2 ** (32 - 19) - 2,
            ),
        ),
        TestCidrCalculator(
            "Test 4",
            "127.0.0.1",
            31,
            Result(
                ip="127.0.0.1",
                mask="255.255.255.254",
                network="127.0.0.0",
                broadcast="127.0.0.1",
                first_host=None,
                last_host=None,
                total_hosts=0,
            ),
        ),
        TestCidrCalculator(
            "Test 5",
            "0.1.2.3",
            32,
            Result(
                ip="0.1.2.3",
                mask="255.255.255.255",
                network="0.1.2.3",
                broadcast=None,
                first_host=None,
                last_host=None,
                total_hosts=0,
            ),
        ),
        TestCidrCalculator(
            "Test 6",
            "255.255.255.255",
            0,
            Result(
                ip="255.255.255.255",
                mask="0.0.0.0",
                network="0.0.0.0",
                broadcast="255.255.255.255",
                first_host="0.0.0.1",
                last_host="255.255.255.254",
                total_hosts=2 ** (32 - 0) - 2,
            ),
        ),
        TestCidrCalculator(
            "Test 7",
            "255.255.255.255",
            32,
            Result(
                ip="255.255.255.255",
                mask="255.255.255.255",
                network="255.255.255.255",
                broadcast=None,
                first_host=None,
                last_host=None,
                total_hosts=0,
            ),
        ),
        TestCidrCalculator(
            "Test do Daniel",
            "192.168.100.25",
            30,
            Result(
                ip="192.168.100.25",
                mask="255.255.255.252",
                network="192.168.100.24",
                broadcast="192.168.100.27",
                first_host="192.168.100.25",
                last_host="192.168.100.26",
                total_hosts=2,
            ),
        )
    ]

    for test in tests:
        print(test, end="")
        result = cidr_calculator(test.ipv4, test.cidr)
        test.assert_results(result)
        print(" - OK")

    print("All tests passed")


if __name__ == "__main__":
    main()
