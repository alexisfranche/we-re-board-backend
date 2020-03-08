from flask import Flask, request, jsonify, abort, make_response, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_enum import EnumField
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy import or_, and_
from datetime import datetime as dt
import enum
import os
import re
import urllib.parse

# Init app
app = Flask(__name__)

# Database
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "postgres://ozqhfdunsqxrnj:758183f57a6468bbfd5f6f4f99c6a753f1e3a2afae37699c8922ca520a488bd3@ec2-52-203-98-126.compute-1.amazonaws.com:5432/d674iu1eqcu3l9"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True

# Init db
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)


# User Class/Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    description = db.Column(db.String(300))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'description')


# Init Schema User
user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Event status enumeration
class EventStatus(enum.Enum):
    Upcoming = "upcoming"
    Finished = "finished"
    Cancelled = "cancelled"
    Rescheduled = "rescheduled"


# Event Class/Model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    game = db.Column(db.String(100))
    description = db.Column(db.String(200))
    datetime = db.Column(db.String(200))
    # status = db.Column(db.Enum(EventStatus))
    status = db.Column(db.String(100))
    event_manager_id = db.Column(db.Integer)

    # def __init__(self, name, address, game, description, datetime, event_manager_id):
    def __init__(self, name, address, game, description, datetime, status, event_manager_id):
        self.name = name
        self.address = address
        self.game = game
        self.description = description
        self.datetime = datetime
        self.status = status
        self.event_manager_id = event_manager_id


# Event Schema
class EventSchema(ma.Schema):
    # status = EnumField(EventStatus)
    class Meta:
        fields = ('id', 'name', 'address', 'game', 'description', 'datetime', 'status', 'event_manager_id')
        # fields = ('id', 'name', 'address', 'game', 'description', 'datetime', 'event_manager_id')


# Init Schema Event
event_schema = EventSchema()
events_schema = EventSchema(many=True)


# Event-User Class/Model #THIS CLASS ESTABLISHES A EVENT TO USER RELATIONSHIP
class Event_User(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, event_id, user_id):
        self.event_id = event_id
        self.user_id = user_id


# Event Schema
class Event_UserSchema(ma.Schema):
    class Meta:
        fields = ('event_id', 'user_id')


# Init Schema User
event_user_relationship_schema = Event_UserSchema()
event_user_relationships_schema = Event_UserSchema(many=True)


@app.route('/', methods=['GET'])
def hello():
    return "<h1> were board backend!!! </h1> You need to login first."


# Create a user
@app.route('/user', methods=['POST'])
def add_user():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    checkEmail(email)
    password_check(password)
    new_user = User(name, email, generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


# Create an event
@app.route('/event', methods=['POST'])
def add_event():
    isMissingField = False
    try:
        name = request.json['name']
        address = request.json['address']
        game = request.json['game']
        datetime = request.json['datetime']  # example format 2020-04-08 04:05:06
        description = request.json['description']
        status = "upcoming"#EventStatus.Upcoming.value
        event_manager_id = request.json['event_manager_id']
    except:
        isMissingField = True
    
    #error flows
    #Missing field
    if isMissingField:
        return make_response(jsonify({'error': 'Please complete all required fields'}), 400)
    #Invalid datetime
    if dt.strptime(datetime, '%Y-%m-%d %H:%M:%S')<dt.now():
        return make_response(jsonify({'error': 'Invalid date and time'}), 400)
   

    # new_event = Event(name, address, description, datetime, event_manager_id)
    new_event = Event(name, address, game, description, datetime, status, event_manager_id)

    db.session.add(new_event)
    db.session.commit()

    return event_schema.jsonify(new_event)


# Add a user to an event
@app.route('/join', methods=['POST'])
def add_event_user():
    event_id = request.json['event_id']
    user_id = request.json['user_id']
    new_event_user = Event_User(event_id, user_id)

    db.session.add(new_event_user)
    db.session.commit()

    return event_user_relationship_schema.jsonify(new_event_user)


regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

# endpoint check if user is applied to the event
@app.route("/event_user/exists", methods=['POST'])
def is_event_user():
    e_id = request.json['event_id']
    u_id = request.json['user_id']
    event_user = Event_User.query.filter_by(event_id = int(e_id), user_id = int(u_id)).first()
    bool = True
    if not event_user:
        bool = False
    print(event_user)
    return make_response(jsonify({'is_joined': bool}), 200)
    
def checkEmail(email):
    if (re.search(regex, email)):
        print("valid password")

    else:
        abort(400, {'message': 'Invalid Email'})


def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%']
    val = True

    if len(passwd) < 2:
        abort(400, {'message': 'length should be at least 6'})

        val = False

    if not any(char.isdigit() for char in passwd):
        print('Password should have at least one numeral')
        abort(400, {'message': 'Password should have at least one numeral'})

        val = False

    if not any(char.isupper() for char in passwd):
        print('Password should have at least one uppercase letter')
        abort(400, {'message': 'Password should have at least one uppercase letter'})

        val = False

    if not any(char.islower() for char in passwd):
        print('Password should have at least one lowercase letter')
        abort(400, {'message': 'Password should have at least one lowercase letter'})

        val = False

    if not any(char in SpecialSym for char in passwd):
        print('Password should have at least one of the symbols $@#')
        abort(400, {'message': 'Password should have at least one of the symbols $@#'})
        val = False
    if val:
        return val


# Get all users
@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


# Get all events
@app.route('/event', methods=['GET'])
def get_events():
    all_events = Event.query.all()
    result = events_schema.dump(all_events)
    return jsonify(result)

# Get all active events
@app.route('/event/active', methods=['GET'])
def get_active_events():
    active_events = Event.query.filter(or_(Event.status == "upcoming", Event.status == "rescheduled")).all()
    result = events_schema.dump(active_events)
    return jsonify(result)
    
# endpoint to get event info by id (returns everything about event)
@app.route("/event/<id>", methods=["GET"])
def event_detail(id):
    event = Event.query.get(id)
    # error handling
    if event is None:
        abort(404)
    return event_schema.jsonify(event)


# Get all events of one game type
@app.route('/event/category/<game>', methods=['GET'])
def get_events_by_category(game):
    game = urllib.parse.unquote_plus(game)
    category_events =  all_events = Event.query.filter(and_(Event.game == game, or_(Event.status == "upcoming", Event.status == "rescheduled"))).all()
    result = events_schema.dump(category_events)
    if not result:
        return make_response(jsonify({'error': 'No active events of this category.'}), 400)
    return jsonify(result)

# endpoint to get profile info by id (returns everything about user)
@app.route("/user/profile/<id>", methods=["GET"])
def profile_detail(id):
    user = User.query.get(id)
    # error handling
    if user is None:
        abort(404)
    return user_schema.jsonify(user)


# endpoint to get user detail by id (returns restricted information about user)
@app.route("/user/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    # error handling
    if user is None:
        abort(404)
    delattr(user, 'password')
    delattr(user, 'email')
    return user_schema.jsonify(user)


#Modify event
@app.route("/event/manage/<user_id>", methods=["GET"])
def event_manage(user_id):
    my_user_id = int(user_id)
    event_user_list = Event_User.query.filter_by(user_id=my_user_id).all()
    eventlist = []
    for event_user in event_user_list:
        event_id = event_user.event_id
        event = Event.query.get(event_id)
        eventlist.append(event)	
    output = events_schema.dump(eventlist)
    return jsonify(output)


# endpoint to login user
@app.route("/login", methods=["POST", "GET"])
def login_user():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        user = User.query.filter_by(email=email).first()
        # error handling
        if user is None:
            # flash('Invalid Credentials. Please try again.')
            abort(401)
        elif not check_password_hash(user.password, password):
            # flash('Invalid Credentials. Please try again.')
            abort(401)
        # else:
        # flash('You were logged in')
    return make_response(jsonify({'data': 'You were logged in.'}), 200)


# endpoint to logout user
@app.route("/logout", methods=["GET"])
def logout_user():
    return make_response(jsonify({'data': 'You were logged out.'}), 200)


@app.route('/event/manager/<manager_id>', methods=['GET'])
def get_Events_By_Manager(manager_id):
    events = Event.query.filter_by(event_manager_id=manager_id)
    result = events_schema.dump(events)
    return jsonify(result)


# endpoint to modify an event
@app.route('/event/<id>', methods=['PUT'])
def event_update(id):
    event = Event.query.get(id)
    name = request.json['name']
    address = request.json['address']
    game = request.json['game']
    datetime = request.json['datetime']  # example format 2020-04-08 04:05:06
    description = request.json['description']

    if not name == "": event.name = name
    if not address == "": event.address = address
    if not game == "": event.game = game
    if not datetime == "":
        event.datetime = request.json['datetime']
        event.status = EventStatus.Rescheduled.value
    if not description == "":
        event.description = description

    db.session.commit()
    return event_schema.jsonify(event)


# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    name = request.json['name']
    email = request.json['email']
    description = request.json['description']
    checkEmail(email)
    password_check(password)
    user.email = email
    user.name = name
    user.description = description

    # db.session.update(user)
    db.session.commit()
    return user_schema.jsonify(user)


# endpoint to update my name
@app.route("/user/profile/name/<email>", methods=["PUT"])
def user_update_name(email):
    user = User.query.filter_by(email=email).first()
    name = request.json['name']

    user.name = name

    # dp.session.update(user)
    db.session.commit()
    return user_schema.jsonify(user)


# endpoint to update my desc
@app.route("/user/profile/desc/<email>", methods=["PUT"])
def user_update_desc(email):
    user = User.query.filter_by(email=email).first()
    description = request.json['description']

    user.description = description

    # dp.session.update(user)
    db.session.commit()
    return user_schema.jsonify(user)





# modify
@app.route("/user/profile/<id>", methods=["PUT"])
def profile_update(id):
    user = User.query.get(id)
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    description = request.json['description']
    checkEmail(email)
    password_check(password)
    user.password = generate_password_hash(password)
    user.email = email
    user.name = name
    user.description = description

    # db.session.update(user)
    db.session.commit()
    return user_schema.jsonify(user)


# endpoint to cancel an event
@app.route('/event/cancel/<id>', methods=["PUT"])
def event_cancel(id):
    event = Event.query.get(id)
    if event is None:
        abort(404)
    event.status = EventStatus.Cancelled.value
    db.session.commit()

    return event_schema.jsonify(event)

# endpoint to delete an event_user
@app.route('/event_user/delete/<event_id>/<user_id>', methods=["DELETE"])
def event_user_delete(event_id, user_id):
    event_user = Event_User.query.filter_by(event_id=event_id, user_id=user_id).first()
    if event_user is None:
        abort(404)
    db.session.delete(event_user)
    db.session.commit()
    return


# endpoint to delete an event
@app.route('/event/<id>', methods=["DELETE"])
def event_delete(id):
    event = Event.query.get(id)
    if event is None:
        abort(404)
    db.session.delete(event)
    db.session.commit()

    return event_schema.jsonify(event)


# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


# Endpoint to check email exists
@app.route("/emailcheck/<email>", methods=["GET"])
def checkIfEmailTaken(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        return "None"
    return "Some"


@app.route("/email/<email>", methods=["GET"])
def getUserWithEmail(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        abort(404)
    return user_schema.jsonify(user)


# error 404 handling
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# error 400 handling
@app.errorhandler(400)
def update_error(error):
    return make_response(jsonify({'error': 'Invalid email or password'}), 400)


# error 401 handling
@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Invalid Credentials. Please try again.'}), 401)


# error 403 handling
@app.errorhandler(403)
def custom_unauthorized(error):
    return make_response(jsonify({'error': 'You need to login first.'}), 403)


db.create_all()

# Run Server
if __name__ == '__main__':
    app.run(debug=False)
