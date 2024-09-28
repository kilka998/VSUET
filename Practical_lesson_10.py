from typing import List


def output_matrix(matrix: List[list], name: str = "Изначальная", text: str = "") -> str:
    text += f"\n{name} матрица: "
    for row in matrix:
        text += f'\n{row}'
    return text


def write_to_file(text: str) -> None:
    with open('./YudkinMihail_Um242_vivod.txt', 'w', encoding='utf-8') as file:
        file.write(text)


def task_1() -> str:
    output_text = "Task 1. Variant 15"
    matrix = []
    with open('./YudkinMihail_Um242_vvod.txt', 'r') as file:
        for idx, value in enumerate(file.readlines()):
            if value == 'Task 2\n':
                break
            if idx == 1:
                N, M, c, d = map(int, value.split())
            elif idx > 1:
                matrix.append([int(i) for i in value.split()])
    output_text = output_matrix(matrix=matrix, text=output_text)
    rows_with_c = []
    for i in range(M):
        if c in matrix[i]:
            rows_with_c.append(i)
            matrix[i] = [x * d for x in matrix[i]]
    output_text = output_matrix(matrix=matrix, name="Задача 1. Результатирующая", text=output_text)
    output_text += f"\nСтроки, содержащие хотя бы один элемент равный c: {rows_with_c}"
    return output_text


def is_all_odd(row: list) -> bool:
    return all(x % 2 != 0 for x in row)


def task_2() -> str:
    output_text = "\n\nTask 2. Variant 15"
    matrix = []
    is_start_task = False
    start_idx = 9999999999999
    with open('./YudkinMihail_Um242_vvod.txt', 'r') as file:
        for idx, value in enumerate(file.readlines()):
            if value == 'Task 2\n' and not is_start_task:
                is_start_task = True
                start_idx = idx + 1
                continue
            if idx == start_idx:
                N, M = map(int, value.split())
            elif idx > start_idx:
                matrix.append([int(i) for i in value.split()])
    output_text = output_matrix(matrix=matrix, text=output_text)
    max_sum = None
    max_row_index = None
    for i in range(M):
        if is_all_odd(matrix[i]):
            row_sum = sum(abs(x) for x in matrix[i])
            if max_sum is None or row_sum > max_sum:
                max_sum = row_sum
                max_row_index = i
    if max_row_index is not None:
        output_text += f"\nСтрока с максимальной суммой модулей элементов (среди строк с только нечетными элементами): индекс {max_row_index}, сумма {max_sum}\nСтрока: {matrix[max_row_index]}"
    else:
        output_text += "\nНет строк, содержащих только нечетные элементы."
    return output_text


def main():
    text = task_1()
    text += task_2()
    write_to_file(text=text)


if __name__ == '__main__':
    main()
