# from stegano import lsb
# # from stegano.lsbset import generators

# def hideMessage(imageFilePath, message):
#     hidedImage = lsb.hide(imageFilePath, message)
#     return hidedImage

# def getMessage(imageFilePath):
#     clearedMessage = lsb.reveal(imageFilePath)
#     return clearedMessage

import LsbSteg

def hideMessage(filePath, message):
    print("path: "+filePath)
    LsbSteg.encodeLSB(message, filePath, filePath)
    return True

def extractMessage(filePath):
    message = LsbSteg.decodeLSB(filePath)
    return message