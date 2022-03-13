# Armstrong number - it is a number which is equal to the sum of cube of its digits
# Example: 153 -> 1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153 

num = int(input("Enter a number: ")) #zapytanie użytkownika o liczbę

sum = 0 #inicjalizacja sumy na 0

temp = num 

while temp > 0: 
  digit = temp % 10 #uzyskujemy ostatnią cyfrę przy użyciu operatora Modulo %;
  sum += digit ** 3 #reszta z dzielenia danej liczby przez 10 jest ostatnią cyfrą tej liczby
  temp //= 10 
  
if num == sum:
  print(num, "is an Armstrong number")
else:
  print(num, "is not an Armstrong number")

''' Wyjaśnienie działania algorytmu:
Podajemy 153 -> Temp = 153 
digit = 153 % 10 (czyli mamy resztę z modulo) = 3
powiększamy sumę o 3 podniesione do potęgi 3 -> czyli sum = 27
Dzielimy 153 na 10 i pomijamy to co jest po przecinku otrzymując 15

Temp = 15
Digit = 15 % 10 czyli 5
Zwiększamy sumę o 5^3 czyli 27 + 125 = 152
Dzielimy 15 na 10 i otrzymujemy 1 

Temp = 1
Digit = 1 % 10 czyli 1
Dodajemy do sumy 1^3 czyli sum = 152 + 1 = 153
''' 
