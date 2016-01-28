#!/usr/bin/env/python

### hw2_starter.py

import sys
from BitVector import BitVector
import string

################################   Initial setup  ################################

# Expansion permutation (See Section 3.3.1):
expansion_permutation = [31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 
9, 10, 11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19, 
20, 21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0]

# P-Box permutation (the last step of the Feistel function in Figure 4):
p_box_permutation = [15,6,19,20,28,11,27,16,0,14,22,25,4,17,30,9,
1,7,23,13,31,26,2,8,18,12,29,5,21,10,3,24]

# Initial permutation of the key (See Section 3.3.6):
key_permutation_1 = [56,48,40,32,24,16,8,0,57,49,41,33,25,17,9,1,58,
50,42,34,26,18,10,2,59,51,43,35,62,54,46,38,30,22,14,6,61,53,45,37,
29,21,13,5,60,52,44,36,28,20,12,4,27,19,11,3]

# Contraction permutation of the key (See Section 3.3.7):
key_permutation_2 = [13,16,10,23,0,4,2,27,14,5,20,9,22,18,11,3,25,
7,15,6,26,19,12,1,40,51,30,36,46,54,29,39,50,44,32,47,43,48,38,55,
33,52,45,41,49,35,28,31]

# Each integer here is the how much left-circular shift is applied
# to each half of the 56-bit key in each round (See Section 3.3.5):
shifts_key_halvs = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1] 




###################################   S-boxes  ##################################

# Now create your s-boxes as an array of arrays by reading the contents
# of the file s-box-tables.txt:
def create_sboxes():
    arrays = []
    with open('s-box-tables.txt') as f:
        for line in f:
            line = line.split()
            if len(line) == 16:
                line = [int(x) for x in line]
                arrays.append(line)

    s_box = []
    for i in range(0,32, 4):
        s_box.append([arrays[k] for k in range(i, i+4)]) # S_BOX

    return s_box

#######################  Get encryption key from user  ###########################

def get_encryption_key(): # key
    #prompt the user for the key
    with open("key.txt", 'r') as f:
       user_supplied_key = f.readline()

    if len(user_supplied_key) != 8:
        raise ValueError("Please give an encryption key that has exactly 8 characters")

    # next, construct a BitVector from the key
    initial_permutation = key_permutation_1
    user_key_bv = BitVector(textstring=user_supplied_key)
    key_bv = user_key_bv.permute(initial_permutation)        ## permute() is a BitVector function
    return key_bv


################################# Generating round keys  ########################
def extract_round_key(nkey): # round key
    round_key = []
    for i in range(16):
        [left,right] = nkey.divide_into_two()   ## divide_into_two() is a BitVector function
        left << shifts_key_halvs[i]
        right << shifts_key_halvs[i]
        nkey = left + right
        new_key = nkey.permute(key_permutation_2)
        round_key.append(new_key)
    return round_key


########################## encryption and decryption #############################

def des(input_file, encrypt_out, decrypt_out, key):

    bv = BitVector(filename = input_file)

    s_boxes = create_sboxes()
    r_bits = [0,5]
    c_bits = [1,2,3,4]

    #Make a fresh vector that we add onto
    total_data = BitVector(size=0)
    round_key = extract_round_key(key)


    ENOUT = open(encrypt_out, 'w')
    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file(64)   ## assumes that your file has an integral
                                                ## multiple of 8 bytes. If not, you must pad it.
        #print("Len of bitvec: ", len(bitvec))
        test= bitvec.get_bitvector_in_ascii()
        #print(bitvec.get_bitvector_in_ascii())
        if len(bitvec) != 64:
            temp = 64 - len(bitvec)
            bitvec.pad_from_left(temp)


        [LE, RE] = bitvec.divide_into_two()

        for i in range(16):
            ## write code to carry out 16 rounds of processing
            #check if we are encrypting or decrypting

            LE_new = RE
            expanded = RE.permute(expansion_permutation)
            #print("Expanded: ",expanded)
            #print("Round key: ",round_key[i])
            xored = expanded ^ round_key[i]
            #print("Xored: ",xored)

            info = []
            for x in range(0,48,6):
                info.append(xored[x:x+6])

            final = BitVector(size=0)
            for i in range(8):
                row = info[i].permute(r_bits).int_val()
                col = info[i].permute(c_bits).int_val()
                final += BitVector(intVal=s_boxes[i][row][col], size=4)

            final = final.permute(p_box_permutation)
            #print("Final after perm: ",final)
            RE = LE ^ final
            LE = LE_new

        total_data += RE + LE
        #print("Total data: ", len(total_data), total_data)
    data = total_data.get_bitvector_in_ascii()
    ENOUT.write(data)
    ENOUT.close()

#*** Starting the decrypt process *******

    filelen = len(data)
    #print(len(data))
    bytes = []
    bytelen = 8
    lastpos = 0

    #keep reading in the data until we don't have anymore 8bit chunks left
    while((filelen - 8) >= 0):
        #go from beginning until you get to the end of the file
        for x in range(0,filelen,8):
            bytes.append(data[x:x+bytelen]) #move by 8 bits
            lastpos = x + bytelen #keep track of last position in case there aren't an even number of 8 bits
            filelen-= 8

    #just in case there are some bits left over, throw them into bytes too
    if(filelen !=0):
        bytes.append(data[lastpos:])

    DEOUT = open(decrypt_out, 'w')

    tot_data = BitVector(size=0)

    for byte in bytes:
        #print(type(byte))
        bv = BitVector(textstring=byte)
        [LE, RE] = bv.divide_into_two()

        for i in range(16):
            ## write code to carry out 16 rounds of processing
            #check if we are encrypting or decrypting

            LE_new = RE
            expanded = RE.permute(expansion_permutation)
            #print("Expanded: ",expanded)
            #print("Round key: ",round_key[15-i])
            xored = expanded ^ round_key[15-i]
            #print("Xored: ",xored)

            info = []
            #Split up the xored value so it can be put through sbox permutations
            for x in range(0,48,6):
                info.append(xored[x:x+6])

            final = BitVector(size=0)
            for i in range(8):
                row = info[i].permute(r_bits).int_val()
                col = info[i].permute(c_bits).int_val()
                final += BitVector(intVal=s_boxes[i][row][col], size=4)

            final = final.permute(p_box_permutation)
            #print("Final after perm: ",final)
            RE = LE ^ final
            LE = LE_new

        tot_data = tot_data + RE + LE
        #print("Tot_data: ", tot_data.get_bitvector_in_ascii())
    de_data = tot_data.get_bitvector_in_ascii()

    DEOUT.write(de_data)
    DEOUT.close()

#################################### main #######################################

def main():
    ## write code that prompts the user for the key
    ## and then invokes the functionality of your implementation
    new_key = get_encryption_key()
    des("message.txt", "encrypted.txt", "decrypted.txt", new_key)
    #des(False, "encrypted.txt", "decrypted.txt", new_key)

if __name__ == "__main__":    main()

