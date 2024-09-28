

def recurse_task_1(A: int, B: int, arr: list = []) -> list:
    if A < B:
        arr.append(A)
        return recurse_task_1(A + 1, B, arr=arr)
    arr.append(B)
    return arr


def task_1() -> None:
    print("Block A. Task 7")
    A = int(input("Введите число А: "))
    B = int(input("Введите число B: "))
    print(f"Числа от {A} до {B}: {recurse_task_1(A, B)}")


def is_prime_recursive(n: int, divisor: int = 2) -> bool:
    if n <= 2:
        return True if n == 2 else False
    if n % divisor == 0:
        return False
    if divisor * divisor > n:
        return True
    return is_prime_recursive(n, divisor + 1)


def task_2() -> None:
    print("Block B. Task 4")
    n = int(input("Введите натуральное число n > 1: "))
    if is_prime_recursive(n):
        print("YES")
    else:
        print("NO")


def main():
    task_1()
    task_2()


if __name__ == '__main__':
    main()
