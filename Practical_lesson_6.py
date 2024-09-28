import random, string


def task_1() -> None:
    print("Task 1")
    arr = [random.choice(string.ascii_letters + string.digits) for i in range(10)]
    print(f"Исходный массив: {arr}")
    unique_arr = list(set(arr))
    result = []
    for value in unique_arr:
        if arr.count(value) > 1:
            result.append(value)
    print(f"Повторяющиеся элементы: {result if result else 'Отсутствуют'}")


def filter_by_task_2(num: int) -> bool:
    if num % 2 != 0:
        return True
    return False


def task_2() -> None:
    print("Task 2")
    arr = [random.randint(10, 20) for i in range(10)]
    print(f"Исходный массив: {arr}")
    result = list(set(filter(filter_by_task_2, arr)))
    result.sort(reverse=True)
    print(f"Массив из нечетных чисел: {result if result else 'Отсутствует'}")


def main():
    print("Variant 15")
    task_1()
    task_2()


if __name__ == '__main__':
    main()
