from flask import Flask, render_template, request, send_from_directory, escape
from werkzeug import secure_filename
import os
import random
from PIL import Image

from RSA import encrypt, decrypt
from RSAKeyGenerator import generate
from LSBHiding import hideMessage, extractMessage

app = Flask(__name__)

def encryptText():
   if request.method == 'GET':
      return render_template('senderView.html')
   else :
      # publicKey = request.form['publicKey']
      imgInput = request.files['imgInput']
      secTextFile = request.files['secTextFile']
      pubKeyFile = request.files['pubKeyFile']

      imgFileName = secure_filename(imgInput.filename)
      imgInput.save(os.path.join(app.root_path, 'temp', imgFileName))

      secFileName = secure_filename(secTextFile.filename)
      secTextFile.save(os.path.join(app.root_path, 'temp', secFileName))

      pubKeyName = secure_filename(pubKeyFile.filename)
      pubKeyFile.save(os.path.join(app.root_path, 'temp', pubKeyName))

      text = list(open(os.path.join(app.root_path, 'temp', secFileName)))[0]
      publicKey = list(open(os.path.join(app.root_path, 'temp', pubKeyName)))[0]

      img = Image.open(os.path.join(app.root_path, 'temp', imgFileName))
      imgWidth, imgHeight = img.size
      if(imgWidth>800 | imgHeight>800) :
         return render_template(
            'senderView.html', 
            text=text,
            publicKey=publicKey,
            errorText="Image pixel size more than 800x800.")

      if(len(str(text))>100):
         return render_template(
            'senderView.html', 
            text=text,
            publicKey=publicKey,
            errorText="Secret text is too long.")

      encryptedText = encrypt(text, publicKey)
      
      encryptedStageFile = open(os.path.join(app.root_path, 'temp', "encryptedStageFile.txt"), "w+")
      encryptedStageFile.write(encryptedText)   

      hideMessage(os.path.join(app.root_path, 'temp', imgFileName), encryptedText)

      return render_template(
        'senderView.html', 
        text=text,
        publicKey=publicKey,
        imgOutput = "/download/"+imgFileName,
        encryptedText="/download/encryptedStageFile.txt",

      )

def decryptText():
   if request.method == 'GET':
      return render_template('receiverView.html')
   else :
      imgInput = request.files['imgInput']
      privKeyFile = request.files['privKeyFile']

      imgFileName = secure_filename(imgInput.filename)
      imgInput.save(os.path.join(app.root_path, 'temp', imgFileName))

      privKeyFileName = secure_filename(privKeyFile.filename)
      privKeyFile.save(os.path.join(app.root_path, 'temp', privKeyFileName))

      privateKey = list(open(os.path.join(app.root_path, 'temp', privKeyFileName)))[0]
  
      encryptedText = extractMessage(os.path.join(app.root_path, 'temp', imgFileName))
      # print(encryptedText1)
      encryptedStageFile = open(os.path.join(app.root_path, 'temp', "encryptedStageFile.txt"), "w+")
      encryptedStageFile.write(encryptedText)   
          
      decryptedText = decrypt(encryptedText, privateKey)

      decryptedStageFile = open(os.path.join(app.root_path, 'temp', "decryptedStageFile.txt"), "w+")
      decryptedStageFile.write(decryptedText)   

      return render_template(
        'receiverView.html', 
        text=encryptedText,
        privateKey=privateKey,
        decryptedText=decryptedText,
        encryptedStageFile='/download/encryptedStageFile.txt',
        decryptedStageFile='/download/decryptedStageFile.txt')
      
def download_file(fileName):
   uploaedFolder = os.path.join(app.root_path, 'temp')
   return send_from_directory(directory=uploaedFolder, filename=fileName, as_attachment=True)

def generateKey ():
   if request.method == 'GET':
      return render_template('keyGenerate.html')
   else :
      pubKey,priKey = generate()
      pubKeyFile = open(os.path.join(app.root_path, 'temp', "pubKeyGen.txt"), "w+")
      privKeyFile = open(os.path.join(app.root_path, 'temp', "privKeyGen.txt"), "w+")
      pubKeyFile.write(pubKey)   
      privKeyFile.write(priKey)

      return render_template('keyGenerate.html', privateKey='/download/privKeyGen.txt', publicKey='/download/pubKeyGen.txt')