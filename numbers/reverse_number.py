# Program odwracający liczbę

n = int(input("Proszę podać liczbę do odwrócenia: "))
print("Twoja liczba przed odwróceniem: %d" %n) #%d placeholder for number; %s placeholder for string

reverse = 0

while n!=0: #jeśli liczba nie jest zerowa
    reverse = reverse*10 + n%10 #
    n = (n//10) #// dzieli i zaokrągla w dół; / zwykłe dzielenie

print("Po odwróceniu Twoja liczba wynosi: %d" %reverse)


# Przykład działania:
"""
Podajemy n = 324
reverse = reverse * 10 + 324%10 (to będzie 4) = reverse * 10 + 4 czyli otrzymuje reverse = 4
n = (324//10) czyli otrzymujemy 32

reverse = 4 * 10 + 32%10 (to będzie 2) = 40 + 2 czyli otrzymujemy reverse = 42
n = (32//10) czyli otrzymujemy 3 

reverse = 42 * 10 + 3%10 (to będzie ) = 420 + 3 czyli otrzymujemy reverse = 423

Po odwróceniu 423
"""
