from BitVector import BitVector
from copy import deepcopy

class RC4():

    def __init__(self, key_string):
        if len(key_string) != 16:
            raise ValueError("Please enter a 16 character key string")

        self.key_string = key_string
        self.initS()
        self.make_key()
        self.initT()
        self.performKSA()


    def make_key(self):
        #Grab the key and split it into bytes (int form)
        self.key_string = BitVector(textstring=self.key_string)
        byte = 8
        self.K = []
        for i in range(0,128,byte):
            self.K.append(self.key_string[i:i+8].intValue())

    def initS(self):
        #initialize S to a list from 0 to 255
        self.S = []
        for i in range(256):
            self.S.append(i)

    def initT(self):
        #initialize T according to specs in Lecture 9
        self.T = []
        keylen = len(self.K)

        for i in range(256):
            self.T.append(self.K[i % keylen])

    def performKSA(self):
        #performs the key scheduling algorithm
        j = 0
        for i in range(256):
            j = (j + self.S[i] + self.T[i]) % 256
            self.swap(self.S[i],self.S[j])

    def swap(self, i, j):
        #swap values of S
        temp = i
        i = j
        j = temp

    def encrypt(self, stream_data):
        encrypted_text = ''
        #Need a copy of S b/c things get swapped and need original S for decrypt
        copyS = deepcopy(self.S)

        i = 0
        j = 0

        #psuedo random number generator from Lecture 9

        for byte in stream_data:
            i = (i+1) % 256
            j = (j+copyS[i]) % 256
            self.swap(copyS[i], copyS[j])
            k =  (copyS[i] + copyS[j]) % 256
            encrypted_text += chr(copyS[k] ^ ord(byte))

        return encrypted_text

    def decrypt(self, encrypted_data):
        #performs the encryption on the encrypted data to decrypt
        return(self.encrypt(encrypted_data))

    def openImage(self, image_file):
        with open(image_file, 'r') as f:
            data = f.readlines()

        header = data[0:2]
        print(header)

        return data, header
    


if __name__ == "__main__":
    test = RC4("LucasElmerGoedde")
    data = "Secret message"
    encrypted = test.encrypt(data)
    print("Encrypted: ", encrypted)
    decrypted = test.decrypt(encrypted)
    print("Decrypted: ", decrypted)