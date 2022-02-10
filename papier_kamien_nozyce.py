# Gra w papier, kamień, nożyce między użytkownikiem a komputerem. 
#

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
  
  
print("Do następnego razu! :)")
  
