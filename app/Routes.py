from flask import Flask, render_template, request, send_from_directory, escape
from werkzeug import secure_filename
import os
from os.path import splitext
import random
from PIL import Image

from RSA import encrypt, decrypt
from RSAKeyGenerator import generate
from LSBHiding import hideMessage, extractMessage

app = Flask(__name__)

bitsPerChar = 8
bitsPerPixel = 3
maxBitStuffing = 2
extension = "png"

def estimateImage(message):
      #  width, height = image.size
   
      #  imageCapacity = width * height * bitsPerPixel
       messageCapacity = (len(message) * bitsPerChar) - (bitsPerChar + maxBitStuffing)
      
       imageCapacity = messageCapacity+8
       imagePixel = imageCapacity/bitsPerPixel
    
       return imageCapacity,imagePixel

def encryptTextStep1():
   if request.method == 'GET':
      return render_template('senderView.html')
   else :
      secTextFile = request.files['secTextFile']
      pubKeyFile = request.files['pubKeyFile']
      secText = request.form['secText']
      pubKeyText = request.form['pubKeyText']

      if(len(secText)==0) :   
         secFileName = secure_filename(secTextFile.filename)
         secTextFile.save(os.path.join(app.root_path, 'temp', secFileName))
         secText = ""
         secTextArr = list(open(os.path.join(app.root_path, 'temp', secFileName)))
         for t in secTextArr:
            secText = secText + "\n" + t
      
      if(len(pubKeyText)>0) :
         publicKey = pubKeyText
      else :
         pubKeyName = secure_filename(pubKeyFile.filename)
         pubKeyFile.save(os.path.join(app.root_path, 'temp', pubKeyName))
         publicKey = open(os.path.join(app.root_path, 'temp', pubKeyName)).readlines()[0]

      # if(len(str(text))>100):
      #    return render_template(
      #       'senderView.html', 
      #       text=text,
      #       publicKey=publicKey,
      #       errorText="Secret text is too long.")

      encryptedText = encrypt(str(secText), str(publicKey))
      
      encryptedStageFile = open(os.path.join(app.root_path, 'temp', "encryptedStageFile.txt"), "w+")
      encryptedStageFile.write(encryptedText)   

      imageCapacity, imagePixel = estimateImage(encryptedText)
      imageCapacity = float(imageCapacity)/8000

      # if( imageCapacity > 50) :
      #   return render_template(
      #   'senderView.html', 
      #   errorText = "Message size is greater than 50 KB (size="+str(imageCapacity)+")!")

      return render_template(
         'senderView.html', 
         imageCapacity=imageCapacity,
         imagePixel=imagePixel,
         secText=secText,
         pubKeyText=publicKey,
         encryptedTextFile="/downloads/encryptedStageFile.txt",
         encryptedText = encryptedText
      )

def encryptTextStep2():
   imgInputFile = request.files['imgInputFile']
   encryptedTextFile = request.files['encryptedTextFile']
   encryptedText = request.form['encryptedText']
   stegoKey = request.form['stegoKey']

   if(encryptedText==0) :
      encryptedTextFileName = secure_filename(encryptedTextFile.filename)
      encryptedTextFile.save(os.path.join(app.root_path, 'temp', encryptedTextFileName))
      encryptedText = list(open(os.path.join(app.root_path, 'temp', encryptedTextFileName)))[0]

   imgFileName = secure_filename(imgInputFile.filename)
   filename, extension = splitext(imgFileName)
   imgFileNameO = secure_filename(filename+"o"+extension)
   # print(filename, extension, imgFileNameO, os.path.join(app.root_path)+"/temp/"+imgFileNameO)
   imgInputFile.save(os.path.join(app.root_path, 'temp', imgFileName))
   # imgInputFile.save(os.path.join(app.root_path, 'temp', imgFileNameO))
   img = Image.open(os.path.join(app.root_path, 'temp', imgFileName))
   img.save(os.path.join(app.root_path)+"/temp/"+imgFileNameO)

   osize = img.size
   ofsize = os.path.getsize(os.path.join(app.root_path, 'temp', imgFileName))

   imageCapacity, imagePixel = estimateImage(encryptedText)
   imageCapacity = float(imageCapacity)/8000

   imgWidth, imgHeight = img.size
   if(imagePixel>= imgWidth*imgHeight) :
      return render_template(
         'senderViewStep2.html', 
         encryptedText=encryptedText,
         errorText="Image pixel ("+str(imgWidth)+" x "+ str(imgHeight)+") is not enough the text "+str(imageCapacity) +" KB!")

   hideMessage(os.path.join(app.root_path, 'temp', imgFileName), encryptedText+"_"+stegoKey)

   imgn = Image.open(os.path.join(app.root_path, 'temp', imgFileName))
   nsize = imgn.size
   nfsize = os.path.getsize(os.path.join(app.root_path, 'temp', imgFileName))

   return render_template(
      'senderViewStep2.html', 
      encryptedText=encryptedText,
      imgOutput = "/downloads/"+imgFileName,
      imgInput = "/downloads/"+imgFileNameO,
      osize=osize,
      ofsize=int(ofsize)/1000,
      nsize=nsize,
      nfsize=int(nfsize)/1000
   )

def decryptTextStep1():
   if request.method == 'GET':
      return render_template('receiverView.html')
   else :
      imgInputFile = request.files['imgInputFile']
      stegoKey =  request.form['stegoKey']

      imgFileName = secure_filename(imgInputFile.filename)
      imgInputFile.save(os.path.join(app.root_path, 'temp', imgFileName))      
  
      encryptedText = extractMessage(os.path.join(app.root_path, 'temp', imgFileName))

      savedTextAndStegoKey = encryptedText.split("_")

      print("savetext", encryptedText)

      if( (len(savedTextAndStegoKey)==2) & (savedTextAndStegoKey[1]!=stegoKey) ):
        return render_template(
        'receiverView.html', 
        errorText = "Stego Key does not match!")

      encryptedStageFile = open(os.path.join(app.root_path, 'temp', "encryptedStageFile.txt"), "w+")
      encryptedStageFile.write(encryptedText)   

      return render_template(
        'receiverView.html', 
        imgOutput = '/downloads/'+imgFileName,
        encryptedStageText = encryptedText,
        encryptedStageFile='/downloads/encryptedStageFile.txt')
      
def decryptTextStep2():
      privKeyFile = request.files['privKeyFile']
      encryptedTextFile = request.files['encryptedTextFile']
      privKeyText = request.form['privKeyText']
      encryptedText = request.form['encryptedText']

      if(len(encryptedText)==0):
         encryptedTextFileName = secure_filename(encryptedTextFile.filename)
         encryptedTextFile.save(os.path.join(app.root_path, 'temp', encryptedTextFileName))
         encryptedText = list(open(os.path.join(app.root_path, 'temp', encryptedTextFileName)))[0]

      if(len(privKeyText)==0):
         privKeyFileName = secure_filename(privKeyFile.filename)
         privKeyFile.save(os.path.join(app.root_path, 'temp', privKeyFileName))
         privKeyText = list(open(os.path.join(app.root_path, 'temp', privKeyFileName)))[0] 

      decryptedText = decrypt(str(encryptedText), str(privKeyText))

      decryptedStageFile = open(os.path.join(app.root_path, 'temp', "decryptedTextFile.txt"), "w+")
      decryptedStageFile.write(decryptedText)   

      return render_template(
        'receiverViewStep2.html', 
        encryptedText=encryptedText,
        privKeyText=privKeyText,
        decryptedText=decryptedText,
        decryptedTextFile='/downloads/decryptedTextFile.txt')

def generateKey ():
   if request.method == 'GET':
      return render_template('keyGenerate.html')
   else :
      pubKey,priKey = generate()

      pubKeyFile = open(os.path.join(app.root_path, 'temp', "pubKeyGen.txt"), "w+")
      privKeyFile = open(os.path.join(app.root_path, 'temp', "privKeyGen.txt"), "w+")
      pubKeyFile.write(pubKey)   
      privKeyFile.write(priKey)

      return render_template(
         'keyGenerate.html', 
         privateKey='/downloads/privKeyGen.txt', 
         privateKeyText=priKey, 
         publicKey='/downloads/pubKeyGen.txt',
         publicKeyText=pubKey)