from flask import Flask, render_template, request, send_from_directory, escape
from werkzeug import secure_filename
import os

from RSAEncryption import newkeys, encrypt, decrypt, importKey
from LSBHiding import hideMessage, extractMessage

app = Flask(__name__)

def index():
   privateKey, publicKey = newkeys(2048)
   privateKeyFormated = privateKey.exportKey().decode('ascii')
   publicKeyFormated = publicKey.exportKey().decode('ascii')
   return render_template('index.html', privateKey=privateKeyFormated, publicKey=publicKeyFormated)

def get_user_list():
   querys = request.args
   try:
      querys['filter']
   except:
      return "List of all users."
   else:
      return "List of Users filtered  by "+querys['filter']

def get_user_info(username):
   user = { 
      'fullName': 'Nay Htet Zaw', 
      'age': 24, 
      'city': 'Mandalay'
   }
   return render_template('userInfo.html', user=user)

def forms():
   if request.method == 'GET':
      return render_template('forms.html')
   else :
      text = request.form['text']
      image = request.files['imagee']
      fileName = secure_filename(image.filename)
      os.makedirs(os.path.join(app.root_path, 'uploaded'), exist_ok=True)
      image.save(os.path.join(app.root_path, 'uploaded', fileName))
      
      pubKey = open(os.path.join(app.root_path,"keys", "publickey.pem")).read()
      privKey = open(os.path.join(app.root_path,"keys", "private.key")).read()
      
      encryptedText = encrypt(text, importKey(pubKey)).hex()
      print(encryptedText)
      hideMessage(os.path.join(app.root_path, 'uploaded', fileName), encryptedText)
      # hidedImage.save(os.path.join(app.root_path, 'uploaded', fileName))

      messageFromImage = extractMessage(os.path.join(app.root_path, 'uploaded', fileName))

      decryptedText = decrypt(bytes.fromhex(messageFromImage), importKey(privKey))

      print("Message from Image ---->")
      print("->"+decryptedText)

      return render_template(
        'formResult.html', 
        fileUrl='/download/'+fileName, 
        fileName=fileName,
        encryptedText=encryptedText, decryptedText=decryptedText, messageFromImage=messageFromImage)
      
def download_file(fileName):
   uploaedFolder = os.path.join(app.root_path, 'uploaded')
   return send_from_directory(directory=uploaedFolder, filename=fileName, as_attachment=True)
