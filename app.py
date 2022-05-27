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

# messages table
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, nullable=False)
    receiver = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    def __repr__(self):
        return f"Message('{self.id}', '{self.sender}', '{self.receiver}', '{self.content}')"

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
                    'user_error' : 'User Not found. Please Register',
                    'some_error' : 'Something wasn\'t right. Please Try again',
                    'not_friend_error' : 'Kindly add friend first.'
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
            return make_response({'error_message':error_messages["password_error"]}, 400, {'Content-Type': 'application/json'})
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
    incoming_requests = Friend.query.filter_by(user2=viewer_id, status=1).all()
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
    # Verifying the validity of request by matching the viewer_id and user2 in the friend_request_id
    # i.e. if the viewer actually received such a request for which response request is generated
    # another validation check is that the 'status' in payload_data must be 1 or 2 or 3
    if viewer_id == friend_request.user2 and payload_data['status'] in [1,2,3,'1','2','3']:
        friend_request.status = int(payload_data['status'])
        db.session.commit()
        response = app.response_class(
            response=json.dumps(response_data),
            status=200,
            mimetype='application/json')
        return response
    else:
        return make_response({'error_message':error_messages["some_error"]}, 400, {'Content-Type': 'application/json'})

@app.route(f"/{api_url_prefix}/friends", methods=['GET'])
def api_friends():
    viewer_id = verify_token(request.headers['UserToken'])
    # need to search friend table twice, once as user1 then as user2
    # friends_requested are all entries with this user as user1
    friends_requested = Friend.query.filter_by(user1=viewer_id,status=2).all()
    friends_added = Friend.query.filter_by(user2=viewer_id,status=2).all()
    all_friends = []
    for each in friends_requested:
        friend = User.query.filter_by(id=each.user2).first()
        all_friends.append({"name":friend.full_name, "userId":friend.id})
    for each in friends_added:
        friend = User.query.filter_by(id=each.user1).first()
        all_friends.append({"name":friend.full_name, "userId":friend.id})
    response = app.response_class(
        response=json.dumps(all_friends),
        status=200,
        mimetype='application/json')
    return response

####### MESSAGES API ####### 

@app.route(f"/{api_url_prefix}/messages/<int:userId1>", methods=['POST'])
def api_send_message(userId1):
    sender_id = verify_token(request.headers['UserToken'])
    #print(sender_id)
    #print(type(sender_id))
    #userId1 is the receiver, now we check if they are friends in the friend table
    response_data = {"status":"success"}
    payload_data = request.json
    relation_status1 = Friend.query.filter_by(user1=sender_id,user2=userId1).first()
    if relation_status1 is None:
        relation_status2 = Friend.query.filter_by(user1=userId1,user2=sender_id).first()
        if relation_status2 is None:
            # this means there is no entry in friends table
            # raise not_friend-error >> send friend request first
            return make_response({'error_message':error_messages["not_friend_error"]}, 400, {'Content-Type': 'application/json'})
        else:
            # they have entry in Friend table, lets check status
            if relation_status2.status in [2,'2']:
                #this means they are friends
                # commit message content to message table
### PENDING >>  # need to add content check if content == None , do not commit
                message = Message(sender=sender_id, receiver=userId1, content=payload_data['content'])
                db.session.add(message)
                db.session.commit()
                response = app.response_class(
                    response=json.dumps(response_data),
                    status=200,
                    mimetype='application/json')
                return response
            elif relation_status2.status in [1,'1']:
                #this means that sender_id is yet to accept
                #raise not_friend_error >> you have to accept friend request first
                return make_response({'error_message':error_messages["not_friend_error"]}, 400, {'Content-Type': 'application/json'})

            else: # i.e. relation_status2.status in [3,'3']
                #this means sender_id rejected userId1's request
                #raise not_friend_error >> you rejected userId1's friend request
                return make_response({'error_message':error_messages["not_friend_error"]}, 400, {'Content-Type': 'application/json'})
    else:
        # they have entry in Friend table, lets check status now
        if relation_status1.status in [2,'2']:
            #this means they are friends
            # commit message content to message table
            message = Message(sender_id=sender_id, receiver_id=userId1)
            db.session.add(message)
            db.session.commit()
            response = app.response_class(
                response=json.dumps(response_data),
                status=200,
                mimetype='application/json')
            return response
        elif relation_status2.status in [1,'1']:
            #this means that sender_id is yet to accept
            #raise not_friend_error >> you have to accept friend request first
            return make_response({'error_message':error_messages["not_friend_error"]}, 400, {'Content-Type': 'application/json'})

        else: # i.e. relation_status2.status in [3,'3']
            #this means sender_id rejected userId1's request
            #raise not_friend_error >> you rejected userId1's friend request
            return make_response({'error_message':error_messages["not_friend_error"]}, 400, {'Content-Type': 'application/json'})


@app.route(f"/{api_url_prefix}/messages/<int:userId1>", methods=['GET'])
def api_get_all_message(userId1):
    viewer_id = verify_token(request.headers['UserToken'])
    #print(sender_id)
    #print(type(sender_id))
    #userId1 is the receiver, now we check if they are friends in the friend table
    response_data = {}
    relation_status1 = Friend.query.filter_by(user1=viewer_id,user2=userId1).first()
    if relation_status1 is None:
        relation_status2 = Friend.query.filter_by(user1=userId1,user2=viewer_id).first()
        if relation_status2 is None:
            # this means there is no entry in friends table
            # raise not_friend-error >> send friend request first
            return make_response({'error_message':error_messages["not_friend_error"]}, 400, {'Content-Type': 'application/json'})
        else:
            # they have entry in Friend table, lets check status
            if relation_status2.status in [2,'2']:
                #this means they are friends
                # commit message content to message table
                messages1 = Message.query.filter_by(sender=viewer_id, receiver=userId1).all()
                messages2 = Message.query.filter_by(sender=userId1, receiver=viewer_id).all()
                chat_history = []
                for each in messages1:
                    chat_history.append((each.id, {"sender":"self", "content":each.content} ))
                for each in messages2:
                    chat_history.append((each.id, {"sender":"friend", "content":each.content} ))

                chat_history = sorted(chat_history, key=lambda x:x[0])
                ordered_chat_history = []
                response_data = {"messages":ordered_chat_history}
                for i, each in enumerate(chat_history):
                    ordered_chat_history.append(chat_history[i][1])
                response = app.response_class(
                    response=json.dumps(response_data),
                    status=200,
                    mimetype='application/json')
                return response
            elif relation_status2.status in [1,'1']:
                #this means that sender_id is yet to accept
                #raise not_friend_error >> you have to accept friend request first
                return make_response({'error_message':error_messages["not_friend_error"]}, 400, {'Content-Type': 'application/json'})

            else: # i.e. relation_status2.status in [3,'3']
                #this means sender_id rejected userId1's request
                #raise not_friend_error >> you rejected userId1's friend request
                return make_response({'error_message':error_messages["not_friend_error"]}, 400, {'Content-Type': 'application/json'})
    else:
        # they have entry in Friend table, lets check status now
        if relation_status1.status in [2,'2']:
            #this means they are friends
            messages1 = Message.query.filter_by(sender=viewer_id, receiver=userId1).all()
            messages2 = Message.query.filter_by(sender=userId1, receiver=viewer_id).all()
            chat_history = []
            for each in messages1:
                chat_history.append((each.id, {"sender":"self", "content":each.content} ))
            for each in messages2:
                chat_history.append((each.id, {"sender":"friend", "content":each.content} ))

            chat_history = sorted(chat_history, key=lambda x:x[0])
            ordered_chat_history = []
            response_data = {"messages":ordered_chat_history}
            for i, each in enumerate(chat_history):
                ordered_chat_history.append(chat_history[i][1])
            response = app.response_class(
                response=json.dumps(response_data),
                status=200,
                mimetype='application/json')
            return response
        elif relation_status2.status in [1,'1']:
            #this means that sender_id is yet to accept
            #raise not_friend_error >> you have to accept friend request first
            return make_response({'error_message':error_messages["not_friend_error"]}, 400, {'Content-Type': 'application/json'})

        else: # i.e. relation_status2.status in [3,'3']
            #this means sender_id rejected userId1's request
            #raise not_friend_error >> you rejected userId1's friend request
            return make_response({'error_message':error_messages["not_friend_error"]}, 400, {'Content-Type': 'application/json'})


# static routes
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