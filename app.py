from flask import Flask, jsonify, render_template, request, make_response
# import jwt
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'

api_url_prefix = "api"

# changes here
@app.route(f"/")
def home():
    return render_template("home.html")

@app.route(f"/{api_url_prefix}/login")
def login():
    return render_template("login.html")

@app.route(f"/{api_url_prefix}/register")
def register():
    return render_template("register.html")

@app.route(f"/{api_url_prefix}/chat")
def chat():
    return render_template("chat.html")
# changes end




if __name__ == '__main__':
    app.run(debug=True)