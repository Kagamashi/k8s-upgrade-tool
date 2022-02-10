#

import random

user_win = 0 
computer_underscore = 0

while True:
  user_input = print("Wybierz Papier/Kamień/Nożyce albo wciśnij K żeby zakończyć grę: ").lower()
  if user_input == "k":
    break
    
  if user_input is not in ["papier", "kamień", "nożyce"]:
    continue
  
  
  
