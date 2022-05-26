from distutils.log import error
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
    phone_number = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    #user_image - add later
    def __repr__(self) -> str: #remove password from this
        return f"User('{self.id}', '{self.full_name}', '{self.phone_number}', '{self.password}')"

# friends table
class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # friend request sender is user1
    user1 = db.Column(db.Integer, nullable=False)
    # friend request receiver is user2
    user2 = db.Column(db.Integer, nullable=False)
    # status == 1 means friend request from user1 to user2 is PENDING
    # status == 2 means friend request from user1 to user2 is ACCEPTED
    # status == 3 means friend request from user1 to user2 is REJECTED
    status = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"Friend('{self.id}', '{self.user1}', '{self.user2}', '{self.status}')"

# generate jwt token
def generate_token(user_id):
    try:
        payload = {
            'id': user_id,
            'created_at':time.time(),
            'exp': time.time() + 7*24*60*60
        }
        return jwt.encode(payload, app.config.get('SECRET_KEY'), algorithm='HS256')
    except Exception as e:
        return e

def verify_token(token):
    try:
        check_payload = jwt.decode(token, app.config.get('SECRET_KEY'), algorithms=["HS256"])
        return check_payload['id']
    except jwt.ExpiredSignatureError:
        return "Token Error: Signature has expired"


error_messages = {
                    'password_error' : 'Password incorrect. Please Try again',
                    'user_error' : 'User Not found. Please Register'
                }
# {"error_message":error_message['user_error']}

@app.route(f"/{api_url_prefix}/login", methods=['POST'])
def api_login():
    payload_data = request.json
    #print(payload_data['phone_number'])
    user = User.query.filter_by(phone_number=payload_data['phone_number']).first()
    print(user)
    if user and bcrypt.check_password_hash(user.password, payload_data['password']):
        # want to pass flash message 
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
        if user: # we here so password not correct
            return make_response({'error_message':error_messages["user_error"]}, 400, {'Content-Type': 'application/json'})
        else: # when user doesnot exist
           return make_response({'error_message': error_messages["user_error"]}, 400, {'Content-Type': 'application/json'})   

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
    print(request.json)
    data = {
        "friends":[ {"name": "<name>", "userId": "userId1"},
                    {"name": "<name>", "userId": "userId2"},]
        }
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json')
    return response

@app.route(f"/{api_url_prefix}/friends/add", methods=['POST'])
def api_add_friend():
    response_data = {"message":"friend request sent"}
    payload_data = request.json
    receiver_id = User.query.filter_by(phone_number=payload_data['phone_number']).first().id
    print(receiver_id)
    print(type(receiver_id))
    sender_id = verify_token(request.headers['UserToken'])
    print(sender_id)
    print(type(sender_id))
# Now to send request from this sender_id to receiver_id, need to commit entry into friend table
    friends = Friend(user1 =sender_id, user2 = receiver_id)
    db.session.add(friends)
    db.session.commit()
    response = app.response_class(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json')
    return response


@app.route(f"/{api_url_prefix}/friends/view-requests", methods=['GET'])
def api_view_friend_requests():
    viewer_id = verify_token(request.headers['UserToken'])
    print(viewer_id)
# now respond with all request to this user from friends table
    incoming_requests = Friend.query.filter_by(user2=viewer_id).all()
#incoming requests is an iterable with element_type = Friend('1', '3', '4', '1')
    print(incoming_requests)
    requests = []
    for each in incoming_requests:
        sender_name = User.query.filter_by(id=each.user1).first().full_name
        friend_request_id = each.id
        requests.append({'name':sender_name, 'friend_request_id':friend_request_id})
    response_data = {'requests':requests}
    response = app.response_class(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json')
    return response



@app.route(f"/{api_url_prefix}/friends/respond-to-requests", methods=['POST'])
def api_respond_to_requests():
    viewer_id = verify_token(request.headers['UserToken'])
    payload_data = request.json
    response_data = {'message': 'Success'}
    friend_request = Friend.query.filter_by(id=payload_data['friend_request_id']).first()
    # do i verify the validity of request by matching the viewer_id and user2 in the friend_request_id
    friend_request.status = payload_data['status']
    db.session.commit()
    response = app.response_class(
        response=json.dumps(response_data),
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
# need change names for below 2 routes
@app.route(f"/friends/add")
def add_friend():
    return render_template("addFriends.html")

@app.route(f"/friends/view-requests")
def view_friend_requests():
    return render_template("friendRequests.html")
# sample routes end



if __name__ == '__main__':
    app.run(debug=True)