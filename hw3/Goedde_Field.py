#!/usr/bin/env/python

def field_or_ring():
    n = int(input("Enter a number, n, to determine if Zn is a field or ring: "))

    #Go through all numbers from 1 to n-1 to find its gcd with n
    for i in range(1,n):
        test = gcd(n, i)
        #if the gcd isn't 1 then we know we have just a ring and not a field
        if test != 1:
            #write to the file
            with open("output.txt", 'w') as f:
                f.write("ring")

            exit()

    with open("output.txt", 'w') as f:
        f.write("field")


#gcd python function taken from Prof. Kak's lecture on Finite Fields(Lecture 5, pg. 20)
def gcd(a,b):
    while b:
        a,b = b, a%b
    return a


if __name__ == "__main__":
    field_or_ring()