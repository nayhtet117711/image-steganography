from flask import Flask, render_template, request, send_from_directory, escape
from werkzeug import secure_filename
import os

from RSA import encrypt, decrypt
from RSAKeyGenerator import generate
from LSBHiding import hideMessage, extractMessage

app = Flask(__name__)

def forms():
   if request.method == 'GET':
      return render_template('forms.html')
   else :
      text = request.form['text']
      image = request.files['imagee']
      fileName = secure_filename(image.filename)
      os.makedirs(os.path.join(app.root_path, 'uploaded'), exist_ok=True)
      image.save(os.path.join(app.root_path, 'uploaded', fileName))
      
      encryptedText = encrypt(text)
      print("encText: "+encryptedText)

      decryptedText = decrypt(encryptedText)

      print("decText: "+decryptedText)

      return render_template(
        'formResult.html', 
        fileUrl='/download/'+fileName, 
        fileName=fileName,
        encryptedText=encryptedText, decryptedText=decryptedText)#, messageFromImage=messageFromImage)
      
def download_file(fileName):
   uploaedFolder = os.path.join(app.root_path, 'uploaded')
   return send_from_directory(directory=uploaedFolder, filename=fileName, as_attachment=True)
