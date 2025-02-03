from flask import request, jsonify
from models.user_model import register_user,authenticate_user,logout_user
from views.responses import json_response
import jwt


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
# def login():
#     #cache.clear()
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return json_response({'message': 'Email and password are required', 'status': 3}, 400)

#     #token,role_id,permissions,user_id = authenticate_user(email, password)
#     token,role_id,permissions,user_id = authenticate_user(email, password)
#     if token:
#         return json_response({'status': 1, 'message': 'Login successful', 'token': token,'role_id':role_id,'permissions':permissions}, 200)
#     return json_response({'status': 2, 'message': message}, 401)


def login():
    #cache.clear()
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return json_response({'message': 'Email and password are required', 'status': 3}, 400)

    # Authenticate user
    result = authenticate_user(email, password)
    
    # If result has 4 values (successful login), unpack them
    if len(result) == 4:
        token, role_id, permissions, user_id = result
        if token:
            return json_response({'status': 1, 'message': 'Login successful', 'token': token, 'role_id': role_id, 'permissions': permissions}, 200)
    # If result has 2 values (failure), handle the error
    elif len(result) == 2:
        token, message = result
        return json_response({'status': 2, 'message': message}, 401)
    
    return json_response({'status': 2, 'message': 'Unknown error occurred'}, 500)


#logout functionality

# def logout():
#     token = request.headers.get('Authorization', '').split(' ')[-1]
    
#     if not token:
#         return jsonify({'message': 'Token is missing'}), 400

#     try:
#         jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
#         blacklist.add(token)
#         return jsonify({'message': 'Logged out successfully'})

#     except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
#         return jsonify({'message': 'Invalid or expired token'}), 401


def logout():
    token = request.headers.get('Authorization', '').split(' ')[-1]
    response, status_code = logout_user(token)
    return jsonify(response), status_code





