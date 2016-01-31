#!/usr/bin/env/python

def field_or_ring():
    num = int(input("Enter a number, n, to determine if Zn is a field or ring: "))

    for i in range(1,num):
        test = gcd(num, i)

        if test != 1:
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