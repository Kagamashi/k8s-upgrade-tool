import random

end_range = input("Podaj liczbę: ") #odpowiedź użytkownika jest stringiem

if end_range.isdigit(): #sprawdzenie czy podany string jest liczbą
  end_range = int(end_range) #przekonwertowanie stringa do inta 

    if end_range <= 0:
      print('Następnym razem podaj liczbę większą od zera :)')
      quit() 
else:
  print('Następnym razem podaj prawdziwą liczbę!')
  quit()

#przedział otwarty z prawej strony
#jeśli wstawimy tylko jedną liczbę to wygenerowana zostanie liczba z przedziału od 0 do podanej liczby minus 1
#randint ma przedział zamknięty z prawej strony
random_number = random.randint(end_range)  
print(r)


