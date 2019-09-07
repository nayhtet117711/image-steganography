from flask import Flask, render_template, redirect, request, send_from_directory

import os

from Routes import encryptTextStep1, encryptTextStep2, decryptTextStep1, decryptTextStep2, generateKey

from nocache import nocache



app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
@nocache
def indexPage():
    return render_template('index.html')
    # return redirect("/sender")

app.add_url_rule("/keys", "generate-keys", generateKey, methods=["GET", "POST"])

app.add_url_rule("/sender", "sender", encryptTextStep1, methods=["GET", "POST"])

@app.route("/sender2", methods=["POST"])
def sender2():
    encryptedText = request.form["encryptedText"]
    return render_template('senderViewStep2.html', encryptedText=encryptedText)

app.add_url_rule("/sender2-do", "sender2-do", encryptTextStep2, methods=["POST"])


app.add_url_rule("/receiver", "receiver", decryptTextStep1, methods=["GET", "POST"])

@app.route("/receiver2", methods=["POST"])
def receiver2():
    encryptedText = request.form["encryptedText"]
    return render_template('receiverViewStep2.html', encryptedText=encryptedText)

app.add_url_rule("/receiver2-do", "receiver2-do", decryptTextStep2, methods=["POST"])

@app.route("/downloads/<fileName>")
@nocache
def downloads(fileName):
    uploaedFolder = os.path.join(app.root_path, 'temp')
    return send_from_directory(directory=uploaedFolder, filename=fileName, as_attachment=True,cache_timeout=0)

if __name__ == "__main__":
   app.run(debug=True)