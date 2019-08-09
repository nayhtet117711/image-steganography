# from __future__ import print_function

#encryption method
def encrypt(plainText):
    keys = []                                       #list to store text from key_generator.txt
    with open("keys/key_generator.txt", 'r') as file:
        for line in file:
            for a in line.split():                  #split text by space
                keys.append(a)                      #add text to keys list
    n = int(keys[2])                                #declare n
    e = int(keys[4])                                #declare e
    
    # plainText = "Hello world 123"
    encText = ""
    for char in plainText:
        encText = encText + str(encryption(ord(char),e,n)) + "\n"
    encText = encText + str(n) + "\n" + str(keys[4])
    return encText
    
#encyrption funciton. m^e % n
def encryption(m,e,n):
    x = pow(m,e,n)
    return x

## DESCypt
def decrypt(encText):
    keys = []  # list to store text from key_generator.txt
    with open("keys/key_generator.txt", 'r') as file:
        for line in file:
            for a in line.split():  # split text by space
                #print(a)
                keys.append(a)  # add text to keys list
    keysLength = len(keys)
    d = keys[10]

    nums = []
    for line in encText.splitlines():
        # print(line)
        nums.append(int(line))            

    l = len(nums)
    n = nums[l-2]
    e = nums[l-1]

    i = 0
    decText = ""
    while i < l -2:
        x = decryption(nums[i], int(d), int(n))
        y = chr(x)
        decText = decText+y
        #print(chr(x).encode('utf-8'), file=decrypted_Mess)
        i+=1
    return decText

def decryption(c,d,n):
    x = pow(c,d,n)
    return x