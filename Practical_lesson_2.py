import math


def main():
    x = 2.444
    y = 0.869 * math.pow(10, -2)
    z = -0.13 * math.pow(10, 3)
    print(
         round((math.pow(x, y + 1) + math.exp(y - 1)) * (1 + abs(y - x)) / (1 + x * abs(y - math.tan(z))) + math.pow(abs(y - x), 2) / 2 - math.pow(abs(y - x), 3) / 3, 6)
    )


if __name__ == '__main__':
    main()
