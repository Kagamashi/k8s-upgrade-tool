# Baza przechowywująca login i hasło do różnych witryn internetowych. Hasła są zaszyfrowane aby zabezpieczyć je przed niepowołanym dostępem.
# TO TYLKO PROJEKT DO NAUKI, RADZĘ TEGO NIE UŻYWAĆ DO PRZECHOWYWANIA SWOICH PRAWDZIWYCH HASEŁ

master_pwd = input("What is the master password? ")

def add(): #definicje funkcji
  pass

def view():
  pass

while True:
action = input("Would you add new password or view the existing ones (add/view)? If you want to quit press Q.").lower()
if action == "q":
  break

elif action =="add":
  add()

elif action =="view":
  view()
  
else: 
  "Wrong action."
  continue

