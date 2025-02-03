import hashlib
import datetime
import jwt
from flask import current_app
from mysql.connector import Error
from mysql.connector import connect
from os import environ as env
from dotenv import load_dotenv
load_dotenv()


blacklist = set()

# MySQL connection details
def get_db_connection():
    connection = connect(
        host=env['DB_HOST'],         # Your MySQL host
        user=env['DB_USER'],              # Your MySQL username
        password=env['DB_PASSWORD'],              # Your MySQL password
        database=env['DATABASE']        # Your database name
    )
    return connection

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to create JWT token
def create_token(user_id):
    SECRET_KEY = current_app.config['SECRET_KEY']  # Access the SECRET_KEY from current_app
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 1-hour expiration
    token = jwt.encode({
        'user_id': user_id,
        'exp': expiration_time
    }, SECRET_KEY, algorithm='HS256')
    return token

# Function to register a new user
def register_user(username, email, password,role_id):
    hashed_password = hash_password(password)
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        # user = cursor.fetchone()
        
        # if user:
        #     return None, "Username already exists"
        
        cursor.execute("INSERT INTO users (username, password,email,role_id) VALUES (%s, %s,%s,%s)", (username, hashed_password,email,role_id))
        connection.commit()
        cursor.close()
        connection.close()
        return True, "User registered successfully"
        
    except Error as e:
        return None, str(e)


# Function to fetch permissions for a given role_id
def get_permissions_for_role(role_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Assuming permissions are stored in a many-to-many relation between roles and permissions
        cursor.execute("""
            SELECT p.permission_slug
            FROM permissions p
            JOIN role_permissions rp ON p.id = rp.permission_id
            WHERE rp.role_id = %s
        """, (role_id,))
        permissions = cursor.fetchall()
        #print(permissions)

        cursor.close()
        connection.close()

        # Return list of permission names (if there are any)
        return [permission[0] for permission in permissions] if permissions else []

    except Error as e:
        return []        

# Function to authenticate user during login
# def authenticate_user(email, password):
#     hashed_password = hash_password(password)
#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor()

#         cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, hashed_password))
#         user = cursor.fetchone()

#         cursor.close()
#         connection.close()

#         if user:
#             user_id = user[0]
#             role_id = user[4]
#             permissions = get_permissions_for_role(role_id)
#             #print(permissions);
#             token = create_token(user_id)
#             return token,role_id,permissions,None
#         else:
#             return None, "Invalid email or password"
        
#     except Error as e:
#         return None, str(e)

def authenticate_user(email, password):
    hashed_password = hash_password(password)
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, hashed_password))
        user = cursor.fetchone()  # Fetch the first row (if any)

        # If there's any unread result, we should consume it properly
        cursor.fetchall()  # This ensures that any remaining result is cleared

        cursor.close()
        connection.close()

        if user:
            user_id = user[0]
            role_id = user[4]
            username = user[1]
            email = user[2]
            permissions = get_permissions_for_role(role_id)
            token = create_token(user_id)
            # Check if token is in bytes, then decode it to string
            if isinstance(token, bytes):
                token = token.decode('utf-8')
            return token, role_id, permissions,user_id,username,email
        else:
            return None, "Invalid email or password"
        
    except Error as e:
        return None, str(e)




# def logout():
#     token = request.headers.get('Authorization')
#     if not token:
#         return jsonify({'message': 'Token is missing'}), 400

#     try:
#         # Remove the "Bearer " prefix
#         token = token.split(' ')[1]
#         # Optionally, you could also verify the token's validity here
#         decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
#         # Add token to blacklist (in real systems, use Redis or a database)
#         blacklist.add(token)
        
#         return jsonify({'message': 'Logged out successfully'})

#     except jwt.ExpiredSignatureError:
#         return jsonify({'message': 'Token has expired'}), 401
#     except jwt.InvalidTokenError:
#         return jsonify({'message': 'Invalid token'}), 401


def logout_user(token):
    from sami_ai_python.app import SECRET_KEY  # Import SECRET_KEY from app.py
    if not token:
        return {'message': 'Token is missing'}, 400

    try:
        jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        blacklist.add(token)  # Blacklist the token
        return {'message': 'Logged out successfully'}, 200

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return {'message': 'Invalid or expired token'}, 401

