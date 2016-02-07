from BitVector import *
import numpy as np

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
    bv = BitVector(filename="key.txt")
    bitvec = bv.read_bits_from_file(128)

    if len(bitvec) != 128:
        raise ValueError("Please give an encryption key that has 16 characters")

    temp = create_sarray()

    for i in range(4):
        for j in range(4):
            byte = bitvec[32*i+8*j:32*i+8*(j+1)]
            temp[j][i] = byte

    key_array = []
    for i in range(4):
        key_array.append(temp[0][i]+temp[1][i]+temp[2][i]+temp[3][i])
        print(key_array[i].get_bitvector_in_ascii())


    return key_array

def aes_encrypt(input_file, encrypted_file):
    subtable, invsubtable = genTables()
    bv = BitVector(filename=input_file)
    key = get_encryption_key()

    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file(128)

        if len(bitvec) != 128:
            pad = 128 - len(bitvec)
            bitvec.pad_from_left(pad)

        sarray = create_sarray()

        for i in range(4):
            for j in range(4):
                byte = bitvec[32*i+8*j:32*i+8*(j+1)]
                sarray[j][i] = sub_bytes(byte, subtable)

        sarray = shift_rows(sarray)

        for i in range(4):
            for j in range(4):
                sarray[j][i] = BitVector(intVal=sarray[j][i])

        sarray = mix_columns(sarray)
        break


def sub_bytes(byte, subtable):

    row = byte.permute([0,1,2,3]).int_val()
    col = byte.permute([4,5,6,7]).int_val()
    #print(row,col)

    #print(subtable[row*16+col])
    return subtable[row*16+col]

def shift_rows(sarray):
    for i in range(4):
        sarray[i] = list(np.roll(sarray[i], -i))

    return sarray

def mix_columns(sarray):
    two = BitVector(intVal=2, size=8)
    three = BitVector(intVal=3, size=8)

    r_array = create_sarray()

    for i in range(4):
        for j in range(4):
            if i == 0:
                part1 = sarray[0][j].gf_multiply_modular(two, AES_modulus, 8)
                part2 = sarray[1][j].gf_multiply_modular(three, AES_modulus, 8)
                r_array[i][j] = part1 ^ part2 ^ sarray[2][j] ^ sarray[3][j]
            elif i == 1:
                part1 = sarray[1][j].gf_multiply_modular(two, AES_modulus, 8)
                part2 = sarray[2][j].gf_multiply_modular(three, AES_modulus, 8)
                r_array[i][j] = part1 ^ part2 ^ sarray[0][j] ^ sarray[3][j]
            elif i == 2:
                part1 = sarray[2][j].gf_multiply_modular(two, AES_modulus, 8)
                part2 = sarray[3][j].gf_multiply_modular(three, AES_modulus, 8)
                r_array[i][j] = part1 ^ part2 ^ sarray[0][j] ^ sarray[1][j]
            elif i == 3:
                part1 = sarray[3][j].gf_multiply_modular(two, AES_modulus, 8)
                part2 = sarray[0][j].gf_multiply_modular(three, AES_modulus, 8)
                r_array[i][j] = part1 ^ part2 ^ sarray[1][j] ^ sarray[2][j]

    return r_array


def create_sarray():
    sarray = [[0 for x in range(4)] for x in range(4)]

    return sarray



if __name__ == "__main__":
    aes_encrypt("plaintext.txt", "encrypted.txt")


