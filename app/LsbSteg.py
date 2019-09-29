from PIL import Image
from os.path import splitext

bitsPerChar = 8
bitsPerPixel = 3
maxBitStuffing = 2
fextension = ".png"

def canEncode(message, image):
       width, height = image.size
       imageCapacity = width * height * bitsPerPixel
       messageCapacity = (len(message) * bitsPerChar) - (bitsPerChar + maxBitStuffing)
       return imageCapacity >= messageCapacity

def createBinaryTriplePairs(message):
       binaries = list("".join([bin(ord(i))[2:].rjust(bitsPerChar,'0') for i in message]) + "".join(['0'] * bitsPerChar))
       binaries = binaries + ['0'] * (len(binaries) % bitsPerPixel)
       binaries = [binaries[i*bitsPerPixel:i*bitsPerPixel+bitsPerPixel] for i in range(0,int(len(binaries) / bitsPerPixel))]
       return binaries

def embedBitsToPixels(binaryTriplePairs, pixels):
       
       binaryPixels = [list(bin(p)[2:].rjust(bitsPerChar,'0') for p in pixel) for pixel in pixels]
      
       for i in range(len(binaryTriplePairs)):
              for j in range(len(binaryTriplePairs[i])):
                     # print(binaryPixels[i][j], binaryTriplePairs[i][j])
                     binaryPixels[i][j] = list(binaryPixels[i][j])
                     binaryPixels[i][j][-1] = binaryTriplePairs[i][j]
                     binaryPixels[i][j] = "".join(binaryPixels[i][j])

       newPixels = [tuple(int(p,2) for p in pixel) for pixel in binaryPixels]
       return newPixels

def encodeLSB(message, imageFilename, newImageFilename):
       filename, extension = splitext(imageFilename)
       # print(filename, extension)              

       img = Image.open(imageFilename)
       
       if (extension==".jpeg") | (extension==".jpg"):
              img.save(filename+fextension)
              img = Image.open(filename+fextension)
       
       size = img.size

       if not canEncode(message, img):
              print("cant encode")
              return None

       binaryTriplePairs = createBinaryTriplePairs(message)

       pixels = list(img.getdata())
       # print("pixels", pixels)
       newPixels = embedBitsToPixels(binaryTriplePairs, pixels)

       newImg = Image.new("RGB", size)
       newImg.putdata(newPixels) 

    #    finalFilename = ".".join([newImageFilename,extension])
    #    finalFilename = ".".join([newImageFilename])
       # print(newImageFilename)

       newImg.save(filename+"_enc_"+fextension)
       newImg.save(newImageFilename)

       return newImg

def getLSBsFromPixels(binaryPixels):
       totalZeros = 0
       binList = []
       for binaryPixel in binaryPixels:
              for p in binaryPixel:
                     if p[-1] == '0':
                            totalZeros = totalZeros + 1
                     else:
                            totalZeros = 0
                     binList.append(p[-1])
                     if totalZeros == bitsPerChar:
                            # print("totalZeros", totalZeros)
                            return  binList

def decodeLSB(imageFilename):
       filename, extension = splitext(imageFilename)
       # print(filename, extension)              

       img = Image.open(imageFilename)
       
       if (extension==".jpeg") | (extension==".jpg"):
              # print("do")
              img.save(filename+fextension)
              img = Image.open(filename+"_"+fextension)
       
       pixels = list(img.getdata())

       # print( [list(bin(p) for p in pixel) for pixel in pixels] )
       
       binaryPixels = [list(bin(p)[2:].rjust(bitsPerChar,'0') for p in pixel) for pixel in pixels]
       
       binList = getLSBsFromPixels(binaryPixels)
       # print("binList", binList)
       test = list(int("".join(binList[i:i+bitsPerChar]),2) for i in range(0,len(binList)-bitsPerChar,bitsPerChar))
      
       message = "".join([chr(int("".join(binList[i:i+bitsPerChar]),2)) for i in range(0,len(binList)-bitsPerChar,bitsPerChar)])
       return message