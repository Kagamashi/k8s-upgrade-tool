# Armstrong number - it is a number which is equal to the sum of cube of its digits
# Example: 153 -> 1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153 

i = 0 
result = 0

n = int(input("Proszę podaj liczbę do sprawdzenia: "))

number1 = n
temp = n

while n!=0
  n = (n/10)
  i=i+1;

while number1!=0:
  n=number1%10
  result=result+pow(n,i)
  number1=number1//10
  
if temp==result:
  print("Number is an Armstrong!")
else: 
  print("Number is NOT an Armstrong.")
