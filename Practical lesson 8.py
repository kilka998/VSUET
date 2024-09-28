import random
from typing import List


def generate_random_matrix(M: int, N: int, lower_bound: int = 0, upper_bound: int = 10) -> List[list]:
    return [[random.randint(lower_bound, upper_bound) for _ in range(N)] for _ in range(M)]


def output_matrix(matrix: List[list], name: str = "Изначальная") -> None:
    print(f"\n{name} матрица: ")
    for row in matrix:
        print(row)


def task_1() -> None:
    print("Task 1")
    M, N, c, d = map(
        int, input(
        "Введите количество строк (M), количество столбцов (N), число для проверки (c) и множитель (d) через пробел: "
        ).split()
    )
    matrix = generate_random_matrix(M=M, N=N, )
    output_matrix(matrix=matrix)
    rows_with_c = []
    for i in range(M):
        if c in matrix[i]:
            rows_with_c.append(i)
            matrix[i] = [x * d for x in matrix[i]]
    output_matrix(matrix=matrix, name="Задача 1. Результатирующая")
    print("Строки, содержащие хотя бы один элемент равный c:", rows_with_c)


def is_all_odd(row: list) -> bool:
    return all(x % 2 != 0 for x in row)


def task_2() -> None:
    print("Task 2")
    M, N = map(
        int, input("Введите количество строк (M), количество столбцов (N) через пробел: ").split()
    )
    matrix = generate_random_matrix(M=M, N=N)
    output_matrix(matrix=matrix)
    max_sum = None
    max_row_index = None
    for i in range(M):
        if is_all_odd(matrix[i]):
            row_sum = sum(abs(x) for x in matrix[i])
            if max_sum is None or row_sum > max_sum:
                max_sum = row_sum
                max_row_index = i
    if max_row_index is not None:
        print(
            f"\nСтрока с максимальной суммой модулей элементов (среди строк с только нечетными элементами): индекс {max_row_index}, сумма {max_sum}")
        print("Строка:", matrix[max_row_index])
    else:
        print("\nНет строк, содержащих только нечетные элементы.")


def main():
    print("Variant 15")
    task_1()
    task_2()


if __name__ == '__main__':
    main()
