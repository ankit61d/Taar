from flask import Flask, json, jsonify, render_template, request, make_response
# import jwt
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'f7976f8bb0b1cvcec676dfde280ba245'

api_url_prefix = "api"

# dummy json route

@app.route(f"/{api_url_prefix}/login", methods=['POST'])
def api_login():
    print(request.data)
    data = {"token":"<token>", "redirect_url": "/chat"}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json')
    return response

@app.route(f"/{api_url_prefix}/register", methods=['POST'])
def api_register():
    print(request.data)
    data = {"message": "User registered"}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json')
    return response

@app.route(f"/{api_url_prefix}/friends", methods=['GET'])
def api_friends():
    print(request.data)
    data = {
        "friends":[ {"name": "<name>", "userId": "userId1"},
                    {"name": "<name>", "userId": "userId2"},]
        }
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json')
    return response

# sample routes 
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
# sample routes end




if __name__ == '__main__':
    app.run(debug=True)