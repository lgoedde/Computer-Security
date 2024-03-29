#! /usr/bin/env python3.4

from BitVector import BitVector
import argparse
from PrimeGenerator import PrimeGenerator

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

def findD(e,p,q):
    #this is the algorithm for finding D according to the notes
    totient = (p-1) * (q-1)

    bv_tot = BitVector(intVal=totient)
    bv_e = BitVector(intVal=e)

    d = bv_e.multiplicative_inverse(bv_tot)
    d = d.int_val()

    return d

def encrypt(e,p,q,data):

    n = p * q

    e_data = []
    for item in data:
        item = item.int_val()
        e_data.append(pow(item,e,n))

    #make each int a bitvector and then get the hex value
    e_data = [BitVector(intVal=x,size=256).get_bitvector_in_hex() for x in e_data]

    #Join them all into one string
    e_data = "".join(e_data)

    #write the data to the ouput file
    args.output_file.write(e_data)

def decrypt(e,p,q,data):
    #find D
    d = findD(e,p,q)

    in_hex = ''

    for item in data:
        item = int(item)

        #need to use CRT to find MI
        d_data = BitVector(intVal=CRT(item,p,q,d), size=256)

        #get rid of those pesky 0's we added before
        d_data = d_data[128:]

        #save for writing
        in_hex += d_data.get_bitvector_in_hex()

        d_data = d_data.get_bitvector_in_ascii()
        #write to a file
        args.output_file.write(d_data.strip('\n'))

    args.output_file.write("\n"+in_hex)

    with open("pqd.txt", 'w') as f:
        f.write("P: " + str(p)+'\n')
        f.write("Q: " + str(q)+'\n')
        f.write("D: " + str(d))

#Chinese remainder theorem from pg. 35, Lecture 12
def CRT(data, p, q, d):
    p_bv = BitVector(intVal=p)
    q_bv = BitVector(intVal=q)

    vp = pow(data, d, p)
    vq = pow(data, d, q)

    xp = int(p_bv.multiplicative_inverse(q_bv))
    xp *= p

    xq = int(q_bv.multiplicative_inverse(p_bv))
    xq *= q

    final = (vp * xp + vq * xq) % (p * q)

    return final

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

    if args.encrypt:
        e = 65537
        p,q = keyGen(e)

        #save the primes to a file to use later
        with open("primes.txt", 'w') as f:
            f.write(str(p))
            f.write('\n')
            f.write(str(q))

        bv_data = getInput(16)
        encrypt(e,p,q, bv_data)


    if args.decrypt:
        e = 65537
        #read primes from a file
        with open("primes.txt", 'r') as f:
            data = f.readlines()
            p = int(data[0])
            q = int(data[1])

        bv_2 = getInput(64)
        decrypt(e,p,q,bv_2)


