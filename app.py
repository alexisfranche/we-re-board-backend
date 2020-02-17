from flask import Flask, request, jsonify, abort, make_response, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash

import os
import re

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

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

def checkEmail(email):

    if(re.search(regex,email)):
        print("valid password")

    else:
        abort(400, {'message': 'Invalid Email'})


def password_check(passwd):

    SpecialSym =['$', '@', '#', '%']
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

# endpoint to login user
@app.route("/login", methods=["POST", "GET"])
def login_user():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        user = User.query.filter_by(email=email).first()
        # error handling
        if user is None:
            flash('Invalid Credentials. Please try again.')
            abort(404)
        elif not check_password_hash(user.password, password):
            flash('Invalid Credentials. Please try again.')
            abort(401)
        else:
            flash('You were logged in')
    return make_response(jsonify({'data': 'Please login'}), 200)

# endpoint to logout user
@app.route("/logout", methods=["GET"])
def logout_user():
    return make_response(jsonify({'data': 'You were logged out'}), 200)

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

    #db.session.update(user)
    db.session.commit()
    return user_schema.jsonify(user)

#endpoint to update my name
@app.route("/user/profile/name/<email>", methods=["PUT"])
def user_update_name(email):
    user = User.query.filter_by(email=email).first()
    name = request.json['name']

    user.name = name

    #dp.session.update(user)
    db.session.commit()
    return user_schema.jsonify(user)

#endpoint to update my desc
@app.route("/user/profile/desc/<email>", methods=["PUT"])
def user_update_desc(email):
    user = User.query.filter_by(email=email).first()
    description = request.json['description']

    user.description = description

    #dp.session.update(user)
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

    #db.session.update(user)
    db.session.commit()
    return user_schema.jsonify(user)

# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

#Endpoint to check email exists
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

#error 404 handling
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
    
#error 400 handling
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