from flask import Flask, json, jsonify, render_template, request, make_response
import jwt, time
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'f7976f8bb0b1cvcec676dfde280ba245'
api_url_prefix = "api"
bcrypt = Bcrypt()
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.Integer(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    def __repr__(self) -> str:
        return f"User('{self.id}', '{self.full_name}', '{self.phone_number}', '{self.password}')"


# generate jwt token
def generate_token(user_id):
    try:
        payload = {
            'id': user_id,
            'created_at':time.time(),
            'expiry': time.time() + 989898
        }
        return jwt.encode(payload, app.config.get('SECRET_KEY'), algorithm='HS256')
    except Exception as e:
        return e


@app.route(f"/{api_url_prefix}/login", methods=['POST'])
def api_login():
    payload_data = request.json
    print(request.json)
    user = User.query.filter_by(phone_number=payload_data['phone_number']).first()
    print(user)
    if user and bcrypt.check_password_hash(user.password, payload_data['password']):
        print("login ok, we're here :P")
        user_token = generate_token(user.id)
        print(user_token)
        print(type(user_token))
        data = {"token":user_token, "redirect_url": "/chat"}
        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json')
        return response
    else:
       return make_response('could not verify', 400, {'Authentication': 'login required"'})   

@app.route(f"/{api_url_prefix}/register", methods=['POST'])
def api_register():
    #print(request.json)
    data = {"message": "User registered"}
    payload_data = request.json
    hashed_password = bcrypt.generate_password_hash(payload_data['password']).decode('utf-8')
    user = User(full_name=payload_data['full_name'],
                    phone_number=payload_data['phone_number'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
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