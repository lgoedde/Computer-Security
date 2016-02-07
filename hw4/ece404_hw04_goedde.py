from BitVector import *

AES_modulus = BitVector(bitstring='100011011')

def genTables():
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    subBytesTable = []           # for encryption
    invSubBytesTable = []        # for decryption
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For byte scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For byte scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))

    return subBytesTable, invSubBytesTable

def get_encryption_key():
    with open("key.txt", 'r')as f:
        key = f.readline()

    if len(key) != 16:
        raise ValueError("Please give an encryption key that has 16 characters")

    return key

def aes_encrypt(input_file, encrypted_file):
    subtable, invsubtable = genTables()


    

