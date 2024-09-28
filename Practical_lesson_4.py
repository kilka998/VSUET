

def fibonacci_sum(N: int, K: int) -> int:
    if N <= 0 or K <= 0:
        return 0

    a, b = 0, 1
    sum_fib = 0

    for i in range(1, N + K):
        if i >= K:
            sum_fib += a
        a, b = b, a + b

    return sum_fib


def main():
    print('Variant 10')
    N, K = map(int, input('Введите числа N, K через пробел: ').split())
    print(f"Сумма {N} чисел ряда Фибоначчи, начиная с {K}-го элемента: {fibonacci_sum(N=N, K=K)}")


if __name__ == '__main__':
    main()
