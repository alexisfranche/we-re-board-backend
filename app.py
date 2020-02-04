from flask import Flask, request , jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash

import os

# Init app
app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://ozqhfdunsqxrnj:758183f57a6468bbfd5f6f4f99c6a753f1e3a2afae37699c8922ca520a488bd3@ec2-52-203-98-126.compute-1.amazonaws.com:5432/d674iu1eqcu3l9"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

    def __init__(self, name, email, password):
        self.name=name
        self.email=email
        self.password=password

# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password')

# Init Schema User
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/', methods=['GET'])
def hello():
    return "<h1> were board backend!!! </h1>"

# Create a user
@app.route('/user', methods=['POST'])
def add_user():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    bio = []

    new_user = User(name, email, generate_password_hash(password), bio)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

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
    #error handling
    print(user.password)
    if user is None:
       abort(404)
    return user_schema.jsonify(user)

# endpoint to get user detail by id (returns restricted information about user)
@app.route("/user/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    #error handling
    if user is None:
       abort(404)
    entriesToRemove = ('password', 'email')
    user.password = None
    user.email = None
    return user_schema.jsonify(user)


# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']

    user.email = email
    user.username = username

    db.session.commit()
    return user_schema.jsonify(user)


# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)
db.create_all()



#error 404 handling
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# Run Server 
if __name__ == '__main__':
    app.run(debug=True)
