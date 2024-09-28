

def filter_by_task_1_1(number: int) -> bool:
    if number > 0 and number < 4:
        return True
    else:
        return False


def task_1_1() -> None:
    print("Task 1.1")
    numbers = [int(input("Введите целое число: ")) for idx in range(3)]
    result = list(filter(filter_by_task_1_1, numbers))
    print(f'Числа, принадлежашие промежутку [1, 3]: {", ".join([str(i) for i in result])}'
          if result else "Нет чисел принадлежащих промежутку [1, 3]")


def task_1_2() -> None:
    print("\nTask 1.2")
    number = int(input("Введите двузначное число: "))
    print("Да" if number % 10 == number // 10 else "Нет")


def task_2() -> None:
    print("\nTask 2 Variant 15")
    a, b = map(int, input("Введите числа a и b через пробел: ").split())
    print(f"Результат: {a + b**2 if a < 2 and b > 3 else  (b**2 + 2 if a > b and a > 3 else b)}")


def task_3() -> None:
    print("\nTask 3 Variant 18")
    number = input("Введите число: ")
    print(f'Число является {"дробным" if float(number) % 1 != 0 else "целым"}')


def main():
    task_1_1()
    task_1_2()
    task_2()
    task_3()


if __name__ == '__main__':
    main()
