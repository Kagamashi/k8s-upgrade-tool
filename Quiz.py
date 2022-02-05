print("Witaj w quizie o Telekomunikacji!")

playing = input("Czy masz ochotę zagrać? ")

if playing.lower() != "tak":
  quit()
else:
  print("Super! Zagrajmy :)")

answer = input("Co oznacza skrót FDD?")
if answer.lower() == "frequency division duplex":
  print("Pra.wiłowa odpowiedź!")
else: 
  print("Źle :(")

answer = input("Co oznacza skrót MIMO?")
if answer.lower() == "multiple input multiple output":
  print("Prawidłowa odpowiedź!")
else:
  print("Źle :(")
  
answer = input("Co oznacza skrót TDMA?")
if answer.lower() == "time division multiple access":
  print("Prawidłowa odpowiedź!")
else: 
  print("Źle :(")

answer = input("Co oznacza skrót BTS?")
if answer.lower() == "base transceiver station":
  print("Prawidłowa odpowiedź!")
else:
  print("Źle :(")

count
