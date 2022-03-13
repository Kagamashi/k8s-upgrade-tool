#Program sprawdzający czy liczba jest liczbą pierwsza

#num = 407
num = int(input("Podaj liczbę którą chcesz sprawdzić: "))

if num > 1:
    for i in range(2,num):
        if (num % i) == 0:
            print(num, "nie jest liczbą pierwszą.")
            print(i,"times",num//i,"is",num)
            break
        else:
            print(num,"jest liczbą pierwszą.")
            break

else: #jeśli liczba jest równa lub mniejsza od 1 
    print(num,"nie jest liczbą pierwszą.")
