#! /usr/bin/env python3.4

from BitVector import BitVector
import argparse
from PrimeGenerator import PrimeGenerator
import numpy as np
import sys

def getInput(blocksize):
    #Made this modifiable so it can open ascii and hex string files
    string = args.input_file.readlines()[0]
    filelen = len(string)
    lastpos = 0
    data = []

    while((filelen - blocksize) >= 0):
        #go from beginning until you get to the end of the file
        for x in range(0,filelen,blocksize):
            data.append(string[x:x+blocksize]) #move by 16 bytes
            lastpos = x + blocksize #keep track of last position in case there aren't an even number of 8 bits
            filelen-= blocksize

    if(filelen  > 0):
        data.append(string[lastpos:])

    #this pads on new line characters
    padded = []
    for item in data:
        if len(item) != blocksize:
            pad = blocksize - len(item)
            item += '\n'*pad
        padded.append(item)

    #if 16 is input it is in ascii
    if blocksize == 16:
        bv_data = []
        for item in padded:
            item = BitVector(textstring=item)
            item.pad_from_left(128)
            bv_data.append(item)

    #The file is in hex, so it needs to be read differently
    if blocksize == 64:
        bv_data = []
        for item in padded:
            item = BitVector(hexstring=item)
            item.pad_from_left(128)
            bv_data.append(item)

    return bv_data

def keyGen(e):

    #Prime number generator taken from code provided by Prof. Avi
    generator = PrimeGenerator( bits = 128, debug = 0 )

    #keep looking for p and q until they meet criteria
    while(True):
        p = generator.findPrime() #make the two prime numbers
        q = generator.findPrime()

        p_test = BitVector(intVal=p, size=128) #need to check bits, so turn into BitVectors
        q_test = BitVector(intVal=q, size=128)

        p_2lmb = p_test[0] and p_test[1] #check the first two bits of each
        q_2lmb = q_test[0] and q_test[1]

        if p_2lmb and q_2lmb:
            if not p == q:
                p_gcd = gcd(p-1,e) #check to make sure p-1 is coprime to e
                q_gcd = gcd(q-1,e) #same for q

                #if they are both co-prime then we win. Yay! Otherwise start over
                if p_gcd == 1 and q_gcd == 1:
                    return p,q


def encrypt(e,p,q,data, file):

    n = p * q

    e_data = []
    for item in data:
        item = item.int_val()
        e_data.append(pow(item,e,n))

    #make each int a bitvector and then get the hex value
    e_data = [BitVector(intVal=x,size=256).get_bitvector_in_hex() for x in e_data]

    with open(file, 'w') as f:
        f.write("".join(e_data))

    #return the data because we encrypt more than once
    return e_data


#Chinese remainder theorem from pg. 35, Lecture 12
def CRT(data1, data2, data3, n1, n2, n3):
    ntot = n1 * n2 * n3

    #setting up values according to CRT lecture notes
    N1 = int(ntot/n1)
    N2 = int(ntot/n2)
    N3 = int(ntot/n3)

    bv_1 = BitVector(intVal=n1)
    bv_2 = BitVector(intVal=n2)
    bv_3 = BitVector(intVal=n3)

    BV_1 = BitVector(intVal=N1)
    BV_2 = BitVector(intVal=N2)
    BV_3 = BitVector(intVal=N3)

    part1 = int(BV_1.multiplicative_inverse(bv_1))
    part2 = int(BV_2.multiplicative_inverse(bv_2))
    part3 = int(BV_3.multiplicative_inverse(bv_3))

    #set up an empty Bitvector to add our cracked data onto
    cracked = BitVector(size=0)
    length = len(data1)

    for i in range(length):
        #turn the hex values into ints
        data1[i] = int(data1[i],16)
        data2[i] = int(data2[i], 16)
        data3[i] = int(data3[i],16)

        temp = (data1[i] * N1 * part1 + data2[i] * N2 * part2 + data3[i] * N3 * part3) % ntot
        #need a more precise root function than python has
        temp = solve_pRoot(3, temp)

        cracked += BitVector(intVal=temp, size=128)

    return cracked


#solve_pRoot function from Prof. Avi's Website
def solve_pRoot(p,y):
    p = int(p)
    y = int(y)
    # Initial guess for xk
    try:
        xk = int(pow(y,1.0/p))
    except:
        # Necessary for larger value of y
        # Approximate y as 2^a * y0
        y0 = y
        a = 0
        while (y0 > sys.float_info.max):
            y0 = y0 >> 1
            a += 1
        # log xk = log2 y / p
        # log xk = (a + log2 y0) / p
        xk = int(pow(2.0, ( a + np.log2(float(y0)) )/ p ))

    # Solve for x using Newton's Method
    err_k = pow(xk,p)-y
    while (abs(err_k) > 1):
        gk = p*pow(xk,p-1)
        err_k = pow(xk,p)-y
        xk = -err_k/gk + xk
    return xk

#gcd python function taken from Prof. Kak's lecture on Finite Fields(Lecture 5, pg. 20)
def gcd(a,b):
    while b:
        a,b = b, a%b
    return a


if __name__ == "__main__":

    #argparse is soooo much better for getting command line arguments
    parser = argparse.ArgumentParser(description="Python implementation to break RSA for small values of e")
    parser.add_argument('input_file', type=argparse.FileType('r'))
    parser.add_argument('output_file', type=argparse.FileType('w'))
    args = parser.parse_args()

    #generate three sets of pub/priv keys
    #low value of e, b/c they are easy to crack
    e = 3

    p1, q1 = keyGen(e)
    n1 = p1 * q1
    p2, q2 = keyGen(e)
    n2 = p2 * q2
    p3, q3 = keyGen(e)
    n3 = p3 * q3
    data = getInput(16)

    e_data1 = encrypt(e,p1,q1,data, "encrypted1.txt")
    e_data2 = encrypt(e,p2,q2,data, "encrypted2.txt")
    e_data3 = encrypt(e,p3,q3,data, "encrypted3.txt")

    test = CRT(e_data1,e_data2,e_data3,n1,n2,n3)

    with open("cracked.txt", 'w') as f:
        f.write(test.get_bitvector_in_ascii())



