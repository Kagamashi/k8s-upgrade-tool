# Baza przechowywująca login i hasło do różnych witryn internetowych. Hasła są zaszyfrowane aby zabezpieczyć je przed niepowołanym dostępem.
# TO TYLKO PROJEKT DO NAUKI, RADZĘ TEGO NIE UŻYWAĆ DO PRZECHOWYWANIA SWOICH PRAWDZIWYCH HASEŁ

master_pwd = input("What is the master password? ")

def add(): #definicje funkcji
  name = input('Account Name: ')
  pwd = input('Password: ')
  
  with open('password.txt', 'a') as f: #
  #file = open('password.txt.', 'a') -> trzeba manualnie zamknąć plik
  #file.close() 
    f.write(name + "|" + pwd + "\n")
  
  #'a' is a mode ('w' -> nadpisuje plik; 'r' -> tylko odczyt; 'a' -> jeśli plik istnieje możemy coś dodać, jeśli nie istnieje tworzymy go

def view():
  with open('passwords.txt', 'r') as f:
    for line in f.readlines():
      data = line.rstrip() #rstrip pozbywa się dodatkowej linii dodanej przez \n
      user, passw = data.split("|")
#data.split("|") ... "hello|miki|eti" => ["hello", "miki", "eti"]
      print("User:", user, "| Password:", passw)
      
      
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

