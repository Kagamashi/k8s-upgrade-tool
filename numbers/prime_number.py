#Program sprawdzający czy dana liczba jest liczbą pierwszą

#num = 29
num = int(input("Podaj liczbę, którą chcesz sprawdzić: "))

#zdefiniowanie zmiennej flag
flag = False

if num > 1:  #wszystkie liczby pierwsze są większe od 1
    for i in range(2, num):  #szukanie dzielników
        if (num%i) == 0:
            flag = True  #jeśli znaleziono dzielnik zmieniamy wartość flagi
            break  #koniec pętli

if flag:
    print(num, "nie jest liczbą pierwszą.")
else:
    print(num, "jest liczbą pierwszą.")
