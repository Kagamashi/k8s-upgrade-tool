# Baza przechowywująca login i hasło do różnych witryn internetowych. Hasła są zaszyfrowane aby zabezpieczyć je przed niepowołanym dostępem.
# TO TYLKO PROJEKT DO NAUKI, RADZĘ TEGO NIE UŻYWAĆ DO PRZECHOWYWANIA SWOICH PRAWDZIWYCH HASEŁ

from cryptography.fernet import Fernet #pip install cryptography -> żeby zainstalować pakiet

master_pwd = input("What is the master password? ")

'''  
def write_key():
  key = Fernet.generate.key()
  with open("key.key", "wb") as key_file:
    key_file.write(key) ''' 
  # ''' ''' wykomentowanie bloku tekstu
  
def load_key():
  file = open("key.key", "rb")
  key = file.read()
  file.close() #trzeba zamknąć plik za każdym razem jak go otwieramy (żeby się uchronić przez zbędnymi problemami)
  return


def add(): 
  name = input('Account Name: ')
  pwd = input('Password: ')
  
  with open('password.txt', 'a') as f: #
    f.write(name + "|" + pwd + "\n")

def view():
  with open('passwords.txt', 'r') as f:
    for line in f.readlines():
      data = line.rstrip() 
      user, passw = data.split("|")
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

