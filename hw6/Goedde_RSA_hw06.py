#! /usr/bin/env python3.4

from BitVector import BitVector
import argparse
from PrimeGenerator import PrimeGenerator

def getInput(blocksize):
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

    if blocksize == 16:
        bv_data = []
        for item in padded:
            item = BitVector(textstring=item)
            item.pad_from_left(128)
            bv_data.append(item)

    if blocksize == 64:
        bv_data = []
        for item in padded:
            item = BitVector(hexstring=item)
            item.pad_from_left(128)
            bv_data.append(item)

    return bv_data

def keyGen():
    #e is given by the homework exercise
    e = 65537

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

def findD(p,q):
    e = 65537
    totient = (p-1) * (q-1)

    bv_tot = BitVector(intVal=totient)
    bv_e = BitVector(intVal=e)

    d = bv_e.multiplicative_inverse(bv_tot)
    d = d.int_val()

    return d

def encrypt(p,q,data):
    e = 65537
    n = p * q

    e_data = []
    for item in data:
        item = item.int_val()
        e_data.append(pow(item,e,n))

    #make each int a bitvector and then get the hex value
    e_data = [BitVector(intVal=x,size=256).get_bitvector_in_hex() for x in e_data]

    #Join them all into one string
    e_data = "".join(e_data)

    args.output_file.write(e_data)

def decrypt(p,q,data):
    d = findD(p,q)



#Chinese remainder theorem from pg. 35, Lecture 12
def CRT(data, p, q, d):
    n = p * q

    vp = pow(data, d, p)
    vq = pow(data, d, p)

    #Finish this up
    
#gcd python function taken from Prof. Kak's lecture on Finite Fields(Lecture 5, pg. 20)
def gcd(a,b):
    while b:
        a,b = b, a%b
    return a


if __name__ == "__main__":

    #argparse is soooo much better for getting command line arguments
    parser = argparse.ArgumentParser(description="Python implementation of the RSA encryption/decryption algorithm")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encrypt', action='store_true', default=False, help='Flag to tell the program to run encryption')
    group.add_argument('-d', '--decrypt', action='store_true', default=False, help="Flag to tell the program to run decryption")
    parser.add_argument('input_file', type=argparse.FileType('r'))
    parser.add_argument('output_file', type=argparse.FileType('w'))
    args = parser.parse_args()

    p,q = keyGen()
    if args.encrypt:
        bv_data = getInput(16)
        encrypt(p,q, bv_data)

    if args.decrypt:
        bv_2 = getInput(64)
        decrypt(p,q, bv_2)

