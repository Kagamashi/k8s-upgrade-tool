#Program sprawdzający czy dany string jest palindromem

#my_str = 'aIbohPhoBiA'
my_str = input("Podaj słowo do sprawdzenia: ")

my_str = my_str.casefold() #nie zwraca uwagi na wielkość znaków

#rev_str = reversed(my_str) #odwraca string
rev_str=my_str[::-1]

if list(my_str) == list(rev_str):
    print("To JEST palindrom!")
else:
    print("To NIE JEST palindrom.")
