#GRA W QUIZ - po odpowiedzi na wszystkie pytania pokazuje ile % odpowiedzi było poprawnych

print("Witaj w quizie o Telekomunikacji!")

playing = input("Czy masz ochotę zagrać? ")
score = 0

if playing.lower() != "tak":
  quit()
else:
  print("Super! Zagrajmy :)")

answer = input("Co oznacza skrót FDD?")
if answer.lower() == "frequency division duplex":
  print("Prawidłowa odpowiedź!")
  score += 1
else: 
  print("Źle :(")

answer = input("Co oznacza skrót MIMO?")
if answer.lower() == "multiple input multiple output":
  print("Prawidłowa odpowiedź!")
  score += 1
else:
  print("Źle :(")
  
answer = input("Co oznacza skrót TDMA?")
if answer.lower() == "time division multiple access":
  print("Prawidłowa odpowiedź!")
  score += 1
else: 
  print("Źle :(")

answer = input("Co oznacza skrót BTS?")
if answer.lower() == "base transceiver station":
  print("Prawidłowa odpowiedź!")
  score += 1
else:
  print("Źle :(")
  
print("Odpowiedziałeś/aś poprawnie na " + str(score) + " pytań")
print("Zdobyłeś/aś " + str((score / 5) * 100) + "%.")

