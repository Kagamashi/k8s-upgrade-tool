# Wyniki rzutów kostką przyjmujące wartość od 1 do 6. Zakładając sekwnecję typu "56611166626634416" napisać funkcję,
# która określi ile razy wystąpiły po sobie dwie 6 (tylko dwie - nie TRZY czy więcej)

def question_1(myseq):
    N = len(myseq) #obliczenie długości sekwencji
    if N <= 1:
        return(0) #jeśli sekwnecja jest równa lub mniejsza od 1 zwracamy 0, bo wtedy nie może być dwóch 6

    if N==2 and myseq=='66': #jeśli długość wynosi 2 i sekwencja to 66 od razu zwracamy wartość TRUE
        return(1)

    count_6s = 0

    #przyjmując ciąg długości 9 sprawdzamy d w zakresie od 0 do 6
    for d in range(len(myseq)-2):
        if d>0 and myseq[d:d+2]=='66' and myseq[d+2]!='6' and myseq[d-1]!='6': #
            count_6s+=1
   
    # sprawdzenie dwóch ostatnich elementów
    if myseq[-2:]=='66' and myseq[-3:-2]!='6': #jeśli dwa ostatnie elementy to 6, a trzeci element od końca jest różny od 6
        count_6s+=1
    
    # sprawdzenie dwóch pierwszych elementów sekwencji, jeśli jest dłuższa niż 2 
    if len(myseq)>2 and myseq[0:2]=='66' and myseq[2]!='6': #jeśli dwa pierwsze elementy to 6, a trzeci element jest inny od 6 
        count_6s+=1
    
    return(count_6s) #zwracamy liczbę sekwencji gdzie były więcej niż dwie 6 

################################
# Question 2
#Znaleźć długość najdłuższej sekwencji w której nie występuje liczba 6.

def question_2(myseq):
    
    # if all the elements are equal to 6 then return 0
    if all(x=='6' for x in list(myseq)):
        return(0)
    # if all the elements are not equal to 6 then return the length of the sequence
    if all(x!='6' for x in list(myseq)):
        return(len(myseq))
    
    # The successive rolls end when the 6 occurs and that is why we store these positions
    end_of = []
    for i, d in enumerate(list(myseq)):
        if d=='6':
            end_of.append(i)
    
    # add the position of the last elemnt in case is not 6
    if myseq[-1]!=6:
        end_of.append(len(myseq))
    # then we get the first differences and finally the max
    lenlist = [end_of[i+1]-end_of[i]-1 for i in range(len(end_of)-1)]
    
    # add the first difference of the first element
    lenlist.append(end_of[0])
    
    return(max(lenlist))

################################
# Lucky roll - sekwencja 5 i 6.

def question_3(myseq):
    # if all the elements are less than 5 then return 0
    if all(int(x)<5 for x in list(myseq)):
        return(0)
    # if all the elements are greater than 4 then return the length of the sequence
    if all(int(x)>4 for x in list(myseq)):
        return(len(myseq))
    
    # The successive rolls end when a roll is less than 5
    end_of = []
    for i, d in enumerate(list(myseq)):
        if int(d)<5:
            end_of.append(i)
        
    # add the position of the last elemnt in case is not 5 or 6
    if int(myseq[-1])>4:
        end_of.append(len(myseq))
        
    # get the length of each sequence
    lenlist = [end_of[i+1]-end_of[i]-1 for i in range(len(end_of)-1)]
    
    
    # add the first difference of the first element
    lenlist.append(end_of[0])
    
    # ignore the 0 lengths
    lenlist = [el for el in lenlist if el!=0]
    
    
    # get the most frequenct length and in case of draw return the longest using the sort
    output = max(sorted(lenlist, reverse=True), key=lenlist.count)
    return(output)


################################

eg1 = "616161666" #len = 9
eg2 = "456116513656124566"
eg3 = "56611166626634416"

print("Example 1")

# *1* Przykładowa sekwencja
print(question_1(eg1))
print(question_2(eg1))
print(question_3(eg1))
print("\nExample 2")

# *2* Przykładowa sekwencja
print(question_1(eg2))
print(question_2(eg2))
print(question_3(eg2))
print("\nExample 3")

# *3* Przykładowa sekwencja
print(question_1(eg3))
print(question_2(eg3))
print(question_3(eg3))
