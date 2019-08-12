from flask import Flask, render_template

from Routes import encryptText, decryptText, download_file, generateKey

app = Flask(__name__)

@app.route("/")
def indexPage():
    return render_template('index.html')

app.add_url_rule("/keys", "generate-keys", generateKey, methods=["GET", "POST"])

app.add_url_rule("/sender", "sender", encryptText, methods=["GET", "POST"])

app.add_url_rule("/receiver", "receiver", decryptText, methods=["GET", "POST"])

app.add_url_rule("/download/<fileName>", "form-submits", download_file, methods=["GET"])

if __name__ == "__main__":
   app.run(debug=True)