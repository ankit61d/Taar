from flask import Flask, json, jsonify, render_template, request, make_response
import jwt
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'

api_url_prefix = "api"

@app.route(f"/{api_url_prefix}/login", method='POST')
def api_login():
    print(request.data)
    data = {"token":"<token>", "redirect_url": "/chat"}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json')
    return response


# changes here
@app.route(f"/")
def home():
    return render_template("home.html")

@app.route(f"/login")
def login():
    return render_template("login.html")

@app.route(f"/register")
def register():
    return render_template("register.html")

@app.route(f"/chat")
def chat():
    return render_template("chat.html")
# changes end




if __name__ == '__main__':
    app.run(debug=True)