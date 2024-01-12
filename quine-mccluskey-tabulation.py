'''
CMSC 130 Laboratory Machine Problem 1
Tabulation Method / Quine McCluskey program
Authors: Antonino, Erica Mae & Trani, Giancarlo Gabriel

This program is designed to generate simplified boolean functions using the tabulation / Quine-McCluskey method.

To implement the method, This Python asks for the desired minterms,
desired number of variables,and desired letter variables from the user.

The program outputs the step-by-step tabulation including the prime implicants table,
and most importantly, the simplified boolean expression.
'''
import itertools # imported to access the groupby() method

'''
Description: Function that checks two minterms for a single-bit difference
Arguments:
x, y                2 minterms from 2 different groups (consecutive) to be compared                   
Return:
bool                True if the 2 minterms differ by 1 bit only, False otherwise
i_mismatch          index where the 2 minterms differ
'''
def compareMinterms(x,y): 
    z = 0
    for i in range(len(x)):
        if x[i] != y[i]:
            i_mismatch = i
            # z is incremented whenever the 2 minterms differ by 1 bit
            z += 1
            if z > 1:
                # if two minterms differ by more than 1 bit, then they shouldn't be paired, thus, returning false
                return (False, None)
    return (True, i_mismatch)


'''
Description: Function that flattens a dictionary/list (remove dimensions)
Arguments:
x                  dictionary/list
Return:
flattened          list that contains all of the binary equivalent of minterms            
'''
def flatten(x): 
    flattened = []
    if type(x) is dict:
        for i in x:
            flattened.extend(x[i])  # add to end of flattened list
    else:
        for i in x:
            for j in i:
                if j not in flattened:
                    flattened.append(j)
    return flattened


'''
Description: Function that determines what are the paired/grouped minterms
Arguments:
x                   grouped binary equivalent of minterms, prime implicants, and essential prime implicants            
Return:
dec                 list containing the decimal form of the minterms
'''
def findMinterms(x): 
    # Counts the number of '-' in binary
    dash = x.count('-')
    if dash == 0:
        # int(x,2) converts x of base 2 to integer/number
        return [str(int(x,2))]
    # Counts the number of '-' in binary
    # pow(2,dash) is code equivalent for 2 to the power of dash (number of '-' in binary). This will determine how many minterms are in the pair/group
    y = [bin(i)[2:].zfill(dash) for i in range(pow(2,dash))] # zfill is used to add zeroes
    dec = []
    for i in range(pow(2,dash)):
        dec1 = x[:]
        idx = -1
        for j in y[0]:
            # idx is the index of “-” in the binary representation.
            if idx != -1:
                idx += dec1[idx+1:].find('-') + 1
            else:
                idx = dec1[idx+1:].find('-')
            dec1 = dec1[:idx]+ j + dec1[idx+1:]
        dec.append(str(int(dec1, 2)))
        y.pop(0)
    return dec


'''
Description: Function that removes don't cares from a list 
Arguments: 
l                   paired minterms
dcs                 list of don't cares
Return:
result              list of minterms without don't cares
'''
def remove_dc(l, dcs):
    result = []
    for i in l:
        if int(i) not in dcs:
            result.append(i)
    return result


'''
Description: Function that finds essential prime implicants in the prime implicants table
Arguments: 
x                   dictionary that contains the prime implicants (both minterm and its respective binary)
Return:
result              list that contains the essential prime implicants
'''
def findEPIs(x): 
    result = []
    for i in x:
        if len(x[i]) == 1:
            if x[i][0] not in result:
                result.append(x[i][0])
            else:
                None
    return result


'''
Description: Removes minterms in prime implicants table/chart which are already covered from essential prime implicants
Arguments: 
pi_mb               dictionary that contains the prime implicants (both minterm and its respective binary)
terms               list that contains essential prime implicants
'''
def removeMinterms(pi_mb, terms): 
    for i in terms:
        for j in findMinterms(i):
            try:
                del pi_mb[j]        # removing of minterms
            except KeyError:        # if key is not found, nothing happens (minterm is not deleted)
                pass                


'''
Description: Function that converts binary representation of essential prime implicants to variables entered by the user
Arguments:
x                   list that contains the prime implicants/essential prime implicants
var                 list of variables (based on the user input)
Return:
varlist            list that contains the variable form of a minterm 
'''
def convertToVar(x, var): 
    varlist = []
    for i in range(len(x)):
        if x[i] == '0':
            for j in var[i]:
                varlist.append(j + "'")    # add prime notation if 0
        elif x[i] == '1':
            for j in var[i]:
                varlist.append(j)          
    return varlist


'''
Description: Function that implements the Petrick's method for further simplification where 2 minterms are multiplied
Arguments:
x, y                 prime implicants in variables form               
Return:
result               list that contains products from essential prime implicants that are multiplied to one another
'''
def multiply_minterms(x,y):
    result = []
    for i in x:
        if i + "'" in y or (len(i) == 2 and i[0] in y):
            return []
        else:
            result.append(i)
    for i in y:
        if i not in result:
            result.append(i)
    return result


'''
Description: Function that implements the Petrick's method for further simplification where 2 expressions are multiplied
Arguments:
x, y                 prime implicants in variables form 
Return:
result               Returns a list that contains the collection of products from essential prime implicants that are multiplied to one another
'''
def multiply(x,y):
    result = []
    for i in x:
        for j in y:
            temp = multiply_minterms(i,j)
            if len(temp) != 0:
                result.append(temp) 
            else:
                None
    return result


'''
Description: Function that implements the Petrick's method for further simplification where 2 minterms are multiplied
Arguments:
x, y                 prime implicants in decimal form 
Return:
results              Returns a list that contains the collection of products from essential prime implicants that are multiplied to one another
'''
def multiplication(x, y):
    result = []
    if len(x) == 0 and len(y) == 0: # both lists empty
        return result
    elif len(x) == 0: # x is empty
        return y
    elif len(y) == 0: # y is empty
        return x

    else:   # both lists are not empty
        for i in x:
            for j in y:
                if i == j:  # if the two minterms are the same
                    result.append(i)
                else:
                    result.append(list(set(i+j)))

        result.sort()  # sort list
        results = list(result for result, _ in itertools.groupby(result))   # remove redundant lists
        return results  # retun list of results


'''
Description: Function for printing of the table that contains minterms and their binary equivalent 
Arguments:
minterms             list that contains both minterms and don't cares
mint                 dictionary that contains the binary equivalent of minterms
size                 number of variables
var                  list that contains the variables to be used
'''
def binconvert(minterms, mint, size, var):
    print("\033[0;32;40m") # Prints Bright Green colored text

    # Converts minterms to binary
    for minterm in minterms:
        try:
            # bin(minterm) is used to convert number to binary
            # bin(minterm)[2:].zfill(size) is used to set the number of bits
            mint[minterm].append(bin(minterm)[2:].zfill(size))
        except KeyError:
            mint[minterm] = [bin(minterm)[2:].zfill(size)]
        
    # Printing of the table that contains the minterms and their binary equivalent
    print("\n\n\n\n   Minterms\t  Binary representation\n%s"%('=' * 42))

    # Prints variables
    print('\t\t\t'+''.join(''.join(i) for i in var))
    print("%s"%('-' * 42))

    # Minterms and their binary representation are printed
    for i in sorted(mint.keys()):
        for j in mint[i]:
            print("    %-20d%s"%(int(j,2), j)) # to display minterm, convert to decimal
        print('-' * 42)
        

'''
Description: Function for printing of the table for the grouped minterms based on the number of 1s in their binary representation 
Arguments:
minterms             list that contains both minterms and don't cares
groups               dictionary that contains the grouped binary equivalent of minterms
size                 number of variables
var                  list that contains the variables to be used
'''
def groupBin(minterms, groups, size, var):
    # Grouping of minterms
    for minterm in minterms:
        try:
            # bin(minterm) is used to convert number to binary
            # bin(minterm)[2:].zfill(size) is used to set the number of bits
            groups[bin(minterm).count('1')].append(bin(minterm)[2:].zfill(size))
        except KeyError:
            groups[bin(minterm).count('1')] = [bin(minterm)[2:].zfill(size)]

    # Printing grouped minterms
    # Prints the table that contains the grouped minterms and their binary equivalent
    print("\n\n\n\n   Minterms\t  Binary representation\n%s"%('=' * 42))

    # Prints variables
    print('\t\t\t'+''.join(''.join(i) for i in var))
    print("%s"%('-' * 42))

    # Minterms and their binary representation are printed
    for i in sorted(groups.keys()):
        for j in groups[i]:
            print("    %-20d%s"%(int(j,2), j))   # to display minterm, convert to decimal
        print('-' * 42)


'''
Description: Function for printing of the table for the paired minterms and checking for the unmarked prime implicants 
Arguments:
groups              dictionary that contains the grouped binary equivalent of minterms
pi_b                set that contains the prime implicants (binary only)
var                 list that contains the variables to be used
Return:
pi_b                set that contains the unmarked prime implicants (binary only)
'''
def pairMin(groups, pi_b, var):
    # Process for creating tables, pairing minterms, and finding prime implicants starts
    while True:
        # Copies the groups where minterms are grouped based on the number of 1 in their binary number
        temp = groups.copy()
        l = sorted(list(temp.keys()))
        marked = set()
        groups = {}
        a = 0
        stop = True

        for i in range(len(l)-1):
            for j in temp[l[i]]:        # Current group elements
                for k in temp[l[i+1]]:  # Next group elements
                    result = compareMinterms(j, k) 
                    if result[0]: # If the minterms differ by 1 bit only
                        # Put a '-' in the changing bit and add it to corresponding group
                        try:
                            if j[:result[1]] + '-' + j[result[1]+1:] not in groups[a]:
                                groups[a].append(j[:result[1]] + '-' + j[result[1]+1:])
                            else:
                                None
                        except KeyError:
                            groups[a] = [j[:result[1]] + '-' + j[result[1]+1:]] # If the group doesn't exist, create the group at first and then put a '-' in the changing bit and add it to the newly created group
                        stop = False
                        marked.add(j) 
                        marked.add(k)
            a += 1
        
        # set(flatten(temp)).difference(marked) is used to check which minterms in the temp are not in set 'marked' 
        unmarked = set(flatten(temp)).difference(marked) 

        # pi_b.union(unmarked) is used to add unmarked minterms to the list of prime implicants
        pi_b = pi_b.union(unmarked) 

        print("\033[1;33;40m") # Prints Yellow colored text

        # Printing prime implicants/unmarked minterms of current table
        if len(unmarked) == 0:
            print("Unmarked prime implicant/s:", None)
        else:
            print("Unmarked prime implicant/s:", ', '.join(unmarked))
        
        # If the minterms cannot be combined/paired further (they do not differ by 1 bit only)
        if stop:
            # Print all prime implicants
            if len(pi_b) == 0:
                print("\n\nPrime implicants from all tables: ", None)
            else:
                print("\n\nPrime implicants from all tables: ", ', '.join(pi_b))
            break # break from while statement to start printing the prime implicants table

        # Next groups are printed
        print("\033[0;32;40m") # Prints Bright Green colored text
        print("\n\n\n\n   Minterms\t    Binary representation\n%s"%('=' * 42))

        # Prints variables
        print('\t\t\t   '+''.join(''.join(i) for i in var))
        print("%s"%('-' * 42))

        # Minterms and their binary representation are printed
        for i in sorted(groups.keys()):
            for j in groups[i]:
                print("   %-24s%s"%(','.join(findMinterms(j)), j))
            print('-' * 42)
    return pi_b


'''
Description: Function that generates the prime implicants table 
Arguments:
mt                  list that contains the minterms
dc                  list that contains the don't cares
pi_b                set that contains the prime implicants (binary only)
pi_mb               dictionary that contains the prime implicants (both minterm and its respective binary)
Return:
pi_mb               Returns dictionary that contains the prime implicants (both minterm and its respective binary)
'''
def printPI(mt, pi_b, dc):
    # Printing prime implicant table/chart
    MaxBinaryValueLen = len(str(mt[-1])) # Length of the maximum minterm
    pi_mb = {}

    print("\033[0;32;40m") # Prints Bright Green colored text
    print('\n\n\nPrime Implicants table:\n\n    Minterms                       | %s\n%s'%(' '.join((' ' * (MaxBinaryValueLen-len(str(i)))) + str(i) for i in mt), '=' * (len(mt)*(MaxBinaryValueLen+1) + 38)))
    
    # Prints unpaired and paired prime implicants and what minterms are present in them
    for i in pi_b:
        y = 0
        paired_minterms = findMinterms(i)
        print(" %-34s|"%', '.join(paired_minterms), end = ' ')
        for j in remove_dc(paired_minterms, dc):
            x = mt.index(int(j)) * (MaxBinaryValueLen + 1) # Index/position to be marked 'X' in the prime implicants table
            print(' ' * abs(x-y) + ' ' * (MaxBinaryValueLen-1) + 'X', end = '')
            y = x + MaxBinaryValueLen
            try:
                # Add minterms in prime implicants table/chart
                if i not in pi_mb[j]:
                    pi_mb[j].append(i)
                else:
                    None
            except KeyError:
                pi_mb[j] = [i]
        print('\n' + '-' * (len(mt)*(MaxBinaryValueLen+1) + 38))
    return pi_mb


'''
Description: Function for printing and simplification of the final equation 
Arguments:
b_pi                set that contains the unmarked prime implicants (binary only)
minterms            list that contains both minterms and don't cares
pi_mb               dictionary that contains the prime implicants (both minterm and its respective binary)
var                 list that contains the variables to be used
'''
def result(pi_mb, b_pi, minterms, var):
    Prime = findEPIs(pi_mb) 
    print("\033[1;33;40m") # Prints Yellow colored text
    print("\nEssential prime implicants: " + ', '.join(str(i) for i in Prime))
    removeMinterms(pi_mb, Prime) # call this function to remove minterms that are in essential prime implicants

    final = []
    print("\033[1;31;40m") # Prints Bright Red colored text
    if(len(pi_mb) == 0): # Check if no minterms remain after removing unpaired minterms that already have a group/pair
        final = [convertToVar(i, var) for i in Prime] # Final result with only essential prime implicants
        print('Boolean function: F = ' + ' + '.join(''.join(i) for i in final)) # Prints the final equation
    else:
        petrick = [[convertToVar(j, var) for j in pi_mb[i]] for i in pi_mb]   # Utilize Petrick's method for further simplification
        while len(petrick) > 1: # Multiplication continues until the sum-of-products of petrick is obtained
            petrick[1] = multiply(petrick[0], petrick[1])
            petrick.pop(0)
        if len(petrick[0]) == 0: # if the length of the list petrick becomes 0, use another formula
            unmarked = list(b_pi)
            PIs = ptrck(minterms, unmarked, var) # Utilize another Petrick's method for further simplification
            for p in PIs:
                st = ''
                for i in range(len(unmarked)):
                    for j in p:
                        if j == i:
                            ans = convertToVar(unmarked[i], var)
                            answer = ""
                            for ele in ans: # Converts the ans list to a string
                                answer += ele
                            st = st + answer + ' + '
                print ("Boolean function: F = " + st[:(len(st)-3)])
        else:
            final = [min(petrick[0], key = len)] # Term in petrick with the least amount of variables is chosen
            final.extend(convertToVar(i, var) for i in Prime) # Essential prime implicants are now added to final list
            print('Boolean function: F = ' + ' + '.join(''.join(i) for i in final)) # Prints the final equation
    print("\n")
    print("\033[0;37;40m") # Prints Normal colored text


'''
Description: Function that implements the other Petrick's method 
Arguments:
minterms            list that contains both minterms and don't cares
unchecked           list that contains the unmarked/unpaired minterm/s
var                 list that contains the variables to be used
Return:
PIs                 2-D list that contains the minterms that will be used for creating the final equation
'''      
def ptrck(minterms, unmarked, var):
    a = []
    for minterm in minterms:
        a.append(bin(minterm)[2:].zfill(len(var)))

    # Make a list PI_chart containing 0s with a length equal to number of minterms
    PI_chart = [[0 for i in range(len(a))] for i in range(len(unmarked))]

    for i in range(len(a)):
        for j in range (len(unmarked)):
            result = compareMinterms(unmarked[j], a[i]) # Checks two minterms for a single-bit difference
            if result[0]:
               PI_chart[j][i] = 1      # if they differ by 1 bit only, change the element of PI_chart with the given index to 1
    
    final = []
    
    # Petrick's method for simplification
    petrick = petrick_method(PI_chart)

    # find the term in petrick with the least amount of variables or minimum length
    minlen = []
    for p in petrick:
        count = 0
        for i in range(len(unmarked)):
            for j in p:
                if j == i:
                    count = count + dashCount(unmarked[i])
        minlen.append(count)

    for i in range(len(minlen)):
        if minlen[i] == min(minlen):
            final.append(petrick[i])

    PIs = flatten(final)
    # [primes[n:n+len(var)] for n in range(0, len(primes), len(var))] groups elements of the list into another list with a length equal to the number of variables
    PIs = [PIs[n:n+len(var)] for n in range(0, len(PIs), len(var))]

    return PIs

'''
Description: Function that counts the number of dash or literals
Arguments:
s                   list that contains the binary representation (with changed bits) of unmarked minterms
Return:
count               number of dash or literals in the binary representation
'''
def dashCount(x):
    count = 0
    for i in range(len(x)):
        if x[i] != '-':
            count+=1
    return count


'''
Description: Function that implements the Petrick's Method to find all solutions
Arguments:
PI_chart            list that contains the 0s and 1s where 1s represents the index where 2 minterms differ by 1 bit
Return:
final               list that contains another list of the minterms with minimum length after doing the multiplication that will be used for creating the final equation
'''
def petrick_method(PI_chart):
    petrick = []
    for col in range(len(PI_chart[0])):
        p = []
        for row in range(len(PI_chart)):
            if PI_chart[row][col] == 1:
                p.append([row])
        petrick.append(p)

    for l in range(len(petrick)-1):   # Multiplication 
        petrick[l+1] = multiplication(petrick[l],petrick[l+1])

    petrick = sorted(petrick[len(petrick)-1], key=len)
    final = []

    # terms with minimum length are selected
    min = len(petrick[0])
    for i in petrick:
        if len(i) == min:
            final.append(i)
        else:
            break

    return final        # the result of the petrick's method is returned

'''
Description: Main Method
Variables:
mt                  list that contains the minterms
minterms            list that contains both minterms and don't cares
size                number of variables
var                 list that contains the variables to be used
dc                  list that contains the don't cares
mint                dictionary that contains the binary equivalent of minterms
groups              dictionary that contains the grouped binary equivalent of minterms
b_pi                set that contains the unmarked prime implicants (binary only)
pi_b                set that contains the prime implicants (binary only)
pi_mb               dictionary that contains the prime implicants (both minterm and its respective binary)
temp                copy of dictionary groups
marked              set that contains the minterms that were paired/combined
unmarked            set that contains the unmarked/unpaired minterms
MaxBinaryValue      binary representation of the highest minterm entered
MaxBinaryValueLen   length of the binary representation of the highest minterm entered
'''
def main():
    print("\033[1;37;40m") # Prints Normal colored text
    # Asks for user input of their desired minterms
    mt = [int(i) for i in input("\nEnter the minterms separated by spaces (ex. 20 28 52 60): ").strip().split()]

    MaxBinaryValue = bin(max(mt))[2:]
    MaxBinaryValueLen = len(MaxBinaryValue)

    validNumOfVar = False
    # Asks for user input of their desired number of variables
    while validNumOfVar == False:
        print("\nMinimum number of variables required: " + str(MaxBinaryValueLen))
        variable = input ("Enter number of variables: ")
       
        if int(variable) < MaxBinaryValueLen:
            print("\nInvalid! Number of variables cannot be less than the length of the binary representation of the highest minterm.\n")
            validNumOfVar = False
        else:
            validNumOfVar = True

    size = int(variable)

    letters = True
    while letters:
        # Asks for user input of their desired variables
        var = [str(i) for i in input("\nEnter the variables separated by spaces (ex. A B C D E F): ").strip().split()]
        if (len(var) != size):
            # if the number of variables they entered is not equal to the size, prints invalid then repeat
            print("Invalid! Number of letters entered must be equivalent to the number of variables input earlier.")
            letters = True
        else:
            letters = False

    # Get don't cares from the user
    dc = [int(i) for i in input("[OPTIONAL, just press enter if none] Enter don't care terms: ").strip().split()]

    mint = {}
    groups = {}
    pi_b = set()

    # sorts the minterms list in ascending order
    mt.sort()

    # if the user entered don't cares, it is added to the minterms list
    minterms = mt + dc
    
    # the minterms list is sorted again, now with the don't care terms
    minterms.sort()

    # Printing of the first table (Minterms and their binary representation)
    binconvert(minterms, mint, size, var)

    # Printing of the table for the grouped minterms based on the number of 1s of their binary representation 
    groupBin(minterms, groups, size, var)

    # Printing of the table for the paired minterms and checking for the unmarked prime implicants
    b_pi = pairMin(groups, pi_b, var)

    # Generation of prime implicant table/chart
    pi_mb = printPI(mt, b_pi, dc)

    # Printing and simplification of the final equation
    result(pi_mb, b_pi, minterms, var)


'''
Description: Menu
'''

def Menu():
    print("\033[1;31;40m") # Prints Bright Red colored text
    print("Welcome to the Tabulation method / Quine- McCluskey program!\nby Antonino, Erica Mae & Trani, Giancarlo Gabriel")
    while True:
        print("\033[0;31;40m") # Prints Red colored text
        menu_choice = input("\n[1] Start\n[0] Quit\nChoice: ")
        if menu_choice == '1':
                main()
                print("Returning to menu...")
        elif menu_choice == '0':
            print("\033[1;37;40m") # Prints Normal colored text
            print("\nGoodbye! Have a great day.\n")
            break
        else:
            print("\033[1;37;40m") # Prints Normal colored text
            print("\nWrong input.\n")
    return True

Menu()