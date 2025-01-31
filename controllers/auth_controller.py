from flask import request, jsonify
from models.user_model import register_user, authenticate_user
from views.responses import json_response

# Registration route
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role_id = data.get('role_id')
    if not role_id:
        role_id = 1
    else:
        role_id = int(role_id)

    if not username or not password or not email:
        return json_response({'message': 'Username, password and email are required', 'status': 3}, 400)

    success, message = register_user(username, email, password,role_id)
    if success:
        return json_response({'message': message, 'status': 1}, 201)
    return json_response({'message': message, 'status': 2}, 400)

# Login route
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return json_response({'message': 'Email and password are required', 'status': 3}, 400)

    token, message,role_id = authenticate_user(email, password)
    if token:
        return json_response({'status': 1, 'message': 'Login successful', 'token': token,'role_id':role_id}, 200)
    return json_response({'status': 2, 'message': message}, 401)
