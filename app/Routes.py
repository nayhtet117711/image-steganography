from flask import Flask, render_template, request, send_from_directory, escape
from werkzeug import secure_filename
import os

from RSA import encrypt, decrypt
from RSAKeyGenerator import generate
from LSBHiding import hideMessage, extractMessage

app = Flask(__name__)

def encryptText():
   if request.method == 'GET':
      return render_template('senderView.html')
   else :
      text = request.form['text']
      publicKey = request.form['publicKey']

      print("secretText: "+text)
      print("publicKey: "+ publicKey)
      
      if(len(str(text))>100):
         return render_template(
            'senderView.html', 
            text=text,
            publicKey=publicKey,
            errorText="Secret text is too long.")

      encryptedText = encrypt(text, publicKey)
      print("encryptedText: "+encryptedText)

      return render_template(
        'senderView.html', 
        text=text,
        publicKey=publicKey,
        encryptedText=encryptedText)

def decryptText():
   if request.method == 'GET':
      return render_template('receiverView.html')
   else :
      text = request.form['text']
      privateKey = request.form['privateKey']

      print("encryptedText: "+ text)
      print("privateKey: "+privateKey)
      
      decryptedText = decrypt(text, privateKey)
      print("decryptedText: "+decryptedText)

      return render_template(
        'receiverView.html', 
        text=text,
        privateKey=privateKey,
        decryptedText=decryptedText)
      
def download_file(fileName):
   uploaedFolder = os.path.join(app.root_path, 'uploaded')
   return send_from_directory(directory=uploaedFolder, filename=fileName, as_attachment=True)

def generateKey ():
   if request.method == 'GET':
      return render_template('keyGenerate.html')
   else :
      pubKey,priKey = generate()
      return render_template('keyGenerate.html', privateKey=priKey, publicKey=pubKey)