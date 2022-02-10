# Gra w papier, kamień, nożyce między użytkownikiem a komputerem. 
# Zliczanie punktów po każdej wygranie i wyświetlenie wyniku użytkownika oraz komputera po zakończeniu rozgrywki. 

import random

user_win = 0 
computer_underscore = 0

options = ["papier", "kamień", "nożyce"]

while True:
  user_input = print("Wybierz Papier/Kamień/Nożyce albo wciśnij K żeby zakończyć grę: ").lower()
  if user_input == "k":
    break
    
  if user_input is not in options:
    continue
    
  random_number = random.randint(0, 2)
  # papier: 0, kamień: 1, nożyce: 2
  computer_pick = options[random_number]
  print("Komputer wybrał", computer_pick + ".")
  
  if user_input == "kamień" and computer_pick == "nożyce":
    print("Wygrałeś! :)")
    user_score += 1
    
  elif user_input == "papier" and computer_pick == "kamień":
    print("Wygrałeś! :)")
    user_score += 1
    
  elif user_input == "nożyce" and computer_pick == "papier":
    print("Wygrałeś! :)")
    user_score += 1
  
  else:
    print("Przegrałeś :(")
    computer_score += 1
  
print("Udało Ci się wygrać", user_score, "razy.")
print("Komputer wygrał", computer_score, "razy."
print("Do następnego razu! :)")
  
