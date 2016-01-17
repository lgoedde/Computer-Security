#! /bin/env/python3.4
from math import *
import string

def cipher():
    with open('input.txt', 'r') as f:
        data = f.readline()
    data = list(data)

    with open('key.txt', 'r') as f:
        key = f.readline()
    key = list(key)

    fir = floor(len(data)/len(key))
    last = (len(data)%len(key))
    key *= fir
    key += key[0:last]

    chars = list(string.ascii_uppercase)
    chars += string.ascii_lowercase

    key_ind = []
    text_ind = []
    for letter in key:
        key_ind.append(chars.index(letter))

    for text in data:
        text_ind.append(chars.index(text))

    final = [chars[sum(x)%len(chars)] for x in zip(key_ind, text_ind)]
    output = "".join(final)

    with open("output.txt", 'w') as f:
        f.write(output)

if __name__ == "__main__":
    cipher()