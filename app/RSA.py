
#encryption method
def encrypt(plainText, publicKey):
    keys = publicKey.split()
    n = int(keys[0])                                #declare n
    e = int(keys[1])                                #declare e

    encText = ""
    for char in plainText:
        encText = encText + str(encryption(ord(char),e,n)) + " "
    encText = encText + str(n) + " " + str(keys[1])
    return encText
    
#encyrption funciton. m^e % n
def encryption(m,e,n):
    x = pow(m,e,n)
    return x

## DESCypt
def decrypt(encText, privateKey):
    keys = privateKey.split()  # list to store text from key_generator.txt
    d = keys[1]
    nums = encText.split()        
    l = len(nums)

    n = nums[l-2]
    e = nums[l-1]

    i = 0
    decText = ""
    while i < l -2:
        x = decryption(int(nums[i]), int(d), int(n))
        y = chr(x)
        decText = decText+y
        #print(chr(x).encode('utf-8'), file=decrypted_Mess)
        i+=1
    return decText

def decryption(c,d,n):
    x = pow(c,d,n)
    return x