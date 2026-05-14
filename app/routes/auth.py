from flask import Flask, request, jsonify, Blueprint, render_template, current_app
from flask_login import login_user, login_required, logout_user
from app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/register', methods=['POST'])
def register():
    db = current_app.db
    data = request.get_json()
    if db.users.find_one({"username": data.get("username")}):
        return jsonify({"message": "Usuário já existe"}), 400
    hashed = bcrypt.generate_password_hash(data.get("password")).decode('utf-8')
    result = db.users.insert_one({
        "username": data.get("username"),
        "password": hashed
    })

    return jsonify({'message': 'User registered successfully'})


@auth_bp.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    db = current_app.db
    data = request.get_json()
    user_data = db.users.find_one({"username": data.get("username")})

    
    if user_data and bcrypt.check_password_hash(user_data['password'], data.get('password')):
        user = User(user_data['_id'], user_data['username'], user_data['password'])
        login_user(user)
        return  jsonify({"message": "logged in successfully"})

    return  jsonify({"message": "Unauthorized. Invalid credentials"}), 401


@auth_bp.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successfully"})

