from hw05 import *

rc4Cipher = RC4("Thisisakeystring")
orignalImage = rc4Cipher.openImage("winterTown.ppm")
encryptedImage = rc4Cipher.encrypt(orignalImage)
decryptedImage = rc4Cipher.decrypt(encryptedImage)
if orignalImage == decryptedImage:
    print('RC4  is awesome')
else:
    print("Hmm, something seems fishy!")