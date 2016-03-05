#! /usr/bin/env python3.4

import argparse
from BitVector import BitVector
from hashlib import sha512

def init_message():
    message = args.input_file.readlines()

    #initial message
    init_bv = BitVector(textstring=message[0])

    #get its length to append later
    mess_len = init_bv.length()

    #add a one in case of empty messages
    plus1 = init_bv + BitVector(bitstring='1')

    #This length is for finding how many zeros to add
    plus1_len = plus1.length()

    #Number of zeros to pad exluding the 128 bit length appended to end
    num_zeros = (896 - plus1_len) % 1024

    #add everything together
    final_bv = plus1 + BitVector(bitlist=[0]*num_zeros) + BitVector(intVal=mess_len, size=128)

    return final_bv

def init_vector():
    h_stuff = ['6a09e667f3bcc908', 'bb67ae8584caa73b', '3c6ef372fe94f82b', 'a54ff53a5f1d36f1', '510e527fade682d1',
               '9b05688c2b3e6c1f', '1f83d9abfb41bd6b', '5be0cd19137e2179']

    return [BitVector(hexstring=h) for h in h_stuff]

def getKeys():
     keys = ['428a2f98d728ae22', '7137449123ef65cd', 'b5c0fbcfec4d3b2f', 'e9b5dba58189dbbc',
            '3956c25bf348b538', '59f111f1b605d019', '923f82a4af194f9b', 'ab1c5ed5da6d8118',
            'd807aa98a3030242', '12835b0145706fbe', '243185be4ee4b28c', '550c7dc3d5ffb4e2',
            '72be5d74f27b896f', '80deb1fe3b1696b1', '9bdc06a725c71235', 'c19bf174cf692694',
            'e49b69c19ef14ad2', 'efbe4786384f25e3', '0fc19dc68b8cd5b5', '240ca1cc77ac9c65',
            '2de92c6f592b0275', '4a7484aa6ea6e483', '5cb0a9dcbd41fbd4', '76f988da831153b5',
            '983e5152ee66dfab', 'a831c66d2db43210', 'b00327c898fb213f', 'bf597fc7beef0ee4',
            'c6e00bf33da88fc2', 'd5a79147930aa725', '06ca6351e003826f', '142929670a0e6e70',
            '27b70a8546d22ffc', '2e1b21385c26c926', '4d2c6dfc5ac42aed', '53380d139d95b3df',
            '650a73548baf63de', '766a0abb3c77b2a8', '81c2c92e47edaee6', '92722c851482353b',
            'a2bfe8a14cf10364', 'a81a664bbc423001', 'c24b8b70d0f89791', 'c76c51a30654be30',
            'd192e819d6ef5218', 'd69906245565a910', 'f40e35855771202a', '106aa07032bbd1b8',
            '19a4c116b8d2d0c8', '1e376c085141ab53', '2748774cdf8eeb99', '34b0bcb5e19b48a8',
            '391c0cb3c5c95a63', '4ed8aa4ae3418acb', '5b9cca4f7763e373', '682e6ff3d6b2b8a3',
            '748f82ee5defb2fc', '78a5636f43172f60', '84c87814a1f0ab72', '8cc702081a6439ec',
            '90befffa23631e28', 'a4506cebde82bde9', 'bef9a3f7b2c67915', 'c67178f2e372532b',
            'ca273eceea26619c', 'd186b8c721c0c207', 'eada7dd6cde0eb1e', 'f57d4f7fee6ed178',
            '06f067aa72176fba', '0a637dc5a2c898a6', '113f9804bef90dae', '1b710b35131c471b',
            '28db77f523047d84', '32caab7b40c72493', '3c9ebe0a15c9bebc', '431d67c49c100d4c',
            '4cc5d4becb3e42b6', '597f299cfc657e2a', '5fcb6fab3ad6faec', '6c44198c4a475817']

     return [BitVector(hexstring=x) for x in keys]

#the structure of this function follows closely with Prof. Avi's SHA-1 code
def hash_processing(message):
    words = [None] * 80
    k = getKeys()
    h_tot = init_vector()

    for n in range(0,message.length(),1024):
        block = message[n:n+1024]
        #first 16 words are the message block
        words[0:16] = [message[i:i+64] for i in range(0,1024,64)]
        for i in range(16,80):
            #word scheduling equation from the notes
            int_part = (int(words[i-16]) + int(sigma0(words[i-15])) + int(words[i-7]) + int(sigma1(words[i-2]))) % (2**64)
            words[i] = BitVector(intVal=int_part,size=64)

            a,b,c,d,e,f,g,h = h_tot

        for i in range(80):
            temp_a = a.deep_copy()
            temp_e = e.deep_copy()

            #functions for T1 and T2
            Ch = (e & f) ^ (~e & g)
            Maj = (a & b) ^ (a & c) ^ (b & c)
            sigmaA = (temp_a>>28) ^ (temp_a>>34) ^ (temp_a>>39)
            sigmaE = (temp_e>>14) ^ (temp_e>>18) ^ (temp_e>>41)

            #T1 and T2 needed for e and a
            T1_int = (int(h) + int(Ch) + int(sigmaE) + int(words[i]) + int(k[i])) % (2**64)
            T2_int = (int(sigmaA) + int(Maj)) % (2**64)

            #round processing
            h = g
            g = f
            f = e
            e_int = (int(d) + T1_int) % (2**64)
            e = BitVector(intVal=e_int,size=64)
            d = c
            c = b
            b = a
            a_int = (T1_int + T2_int) % (2**64)
            a = BitVector(intVal=a_int,size=64)

            letters = [a,b,c,d,e,f,g,h]

        #make the initial values for the next round, the calculated values from this round
        for i in range(8):
            temp = (int(h_tot[i]) + int(letters[i])) % (2**64)
            h_tot[i] = BitVector(intVal=temp,size=64)


    final_hash = BitVector(size=0)
    for item in h_tot:
        final_hash+=item

    return final_hash

#Sigma functions from the notes
def sigma0(num):
    temp = num.deep_copy()

    return (temp>>1) ^ (temp>>8) ^ (temp.shift_right(7))

def sigma1(num):
    temp = num.deep_copy()

    return (temp>>19) ^ (temp>>61) ^ (temp.shift_right(6))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python implementation of SHA-512 hashing")
    parser.add_argument('input_file', type=argparse.FileType('r'))
    args = parser.parse_args()

    bv = init_message()
    final = hash_processing(bv)

    with open("output.txt", 'w') as f:
        f.write(final.get_bitvector_in_hex())





