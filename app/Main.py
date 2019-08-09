from flask import Flask

from Routes import forms, download_file

app = Flask(__name__)

# app.add_url_rule("/", "index", index, methods=["GET"])

# app.add_url_rule("/users", "user-list", get_user_list, methods=["GET"])

# app.add_url_rule("/users/<username>", "user-info", get_user_info, methods=["GET"])

app.add_url_rule("/forms", "form-submit", forms, methods=["GET", "POST"])

app.add_url_rule("/download/<fileName>", "form-submits", download_file, methods=["GET"])

if __name__ == "__main__":
   app.run(debug=True)