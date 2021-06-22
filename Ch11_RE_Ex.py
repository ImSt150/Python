import re
hand = open('regex_sum_1234158.txt') #returning a handle sequence of strings(lines)
lst=list()
for line in hand: #line is both an iteration variable and a python's reserved word
    line = line.rstrip()

    if re.search('[0-9]+', line): #matching the lines with 1 or more digits
        y = re.findall('[0-9]+', line) #return a list of line digits
    else :
        continue  # if the line lacks digit, skip back to for
    #print(y)
    for el in y :
        el_int = int(el)  #converting each string element(with numberic characters) of list y into an integer
    #y_int = int(y)
        lst.append(el_int) #appending each integer to our master list of integers
print(lst) #for debugging
numbers_count = len(lst)  #number of integer numbers in the master list.
print(numbers_count)
total = sum(lst)
print(total)
