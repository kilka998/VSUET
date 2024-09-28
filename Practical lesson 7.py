import math


def is_prime(num: int) -> bool:
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


def is_binary_palindrome(num: int) -> bool:
    binary_representation = bin(num)[2:]
    return binary_representation == binary_representation[::-1]


def find_palindromic_primes(n: int) -> list:
    result = []
    for i in range(2, n + 1):
        if is_prime(i) and is_binary_palindrome(i):
            result.append(i)
    return result


def task_1() -> None:
    print("Task 1")
    n = int(input("Введите n: "))
    print(
        f"Простые числа, которые не превышают {n},",
        f"двоичная запись которых является палиндромом: {find_palindromic_primes(n)}"
    )


def distance(point1: tuple, point2: tuple) -> float:
    return math.sqrt(
        (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)


def find_minimum_distance(points: list) -> (float, tuple):
    min_distance = float('inf')
    closest_pair = None
    num_points = len(points)

    for i in range(num_points):
        for j in range(i + 1, num_points):
            dist = distance(points[i], points[j])
            if dist < min_distance:
                min_distance = dist
                closest_pair = (points[i], points[j])

    return min_distance, closest_pair


def task_2() -> None:
    print("Task 2")
    X = tuple(map(float, input("Введите координаты X (через пробел): ").split()))
    Y = tuple(map(float, input("Введите координаты Y (через пробел): ").split()))
    Z = tuple(map(float, input("Введите координаты Z (через пробел): ").split()))
    T = tuple(map(float, input("Введите координаты T (через пробел): ").split()))

    points = [X, Y, Z, T]

    min_dist, closest_points = find_minimum_distance(points)
    print(f"Минимальное расстояние между точками {closest_points[0]} и {closest_points[1]}: {min_dist:.4f}")


def main():
    print("Variant 15")
    task_1()
    task_2()


if __name__ == '__main__':
    main()
