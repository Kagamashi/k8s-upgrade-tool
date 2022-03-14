#Program wyświetlający ciąg Fibonacciego do wartości nterms

nterms = int(input("Ile wyrazów ciągu chcesz wyświetlić? "))

n1, n2 = 0, 1 #dwie pierwsze wartości ciągu
count = 0

if nterms <= 0: #sprawdzenie czy liczba wyrazów jest poprawna
   print("Proszę, podaj dodatnią liczbę całkowitą.")

elif nterms == 1: #jeśli wyraz ma być tylko 1 po prostu wyświetlamy 0
   print("Ciąg Fibonacciego do",nterms,":")
   print(n1)

else: #tworzenie ciągu Fibonacciego
   print("Fibonacci sequence:")
   while count < nterms:
       print(n1)
       nth = n1 + n2
   
       n1 = n2  #zaktualizowanie wartości
       n2 = nth
       count += 1
