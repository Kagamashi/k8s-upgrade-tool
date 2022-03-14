#Fibonacci - metoda iteracyjna
# 0, 1, 1, 2, 3, 5, 8 ... seria liczb w której każda kolejna liczba jest sumą dwóch poprzednich.

from re import I


first, second = 0,1

n = int(input("Proszę podać ile liczb w ciągu chcesz wyświetlić: "))

def fibonacci(num):
    if num == 0:
        return 0
    elif num == 1:
        return 1
    else:
        return fibonacci(num-1)+fibonacci(num-2)

print("Ciąg Fibonacciego: ")
for i in range(0, n):
    print(fibonacci(i))
