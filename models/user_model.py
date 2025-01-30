import hashlib
import datetime
import jwt
from flask import current_app
from mysql.connector import Error
from mysql.connector import connect

# MySQL connection details
def get_db_connection():
    connection = connect(
        host='localhost',         # Your MySQL host
        user='root',              # Your MySQL username
        password='',              # Your MySQL password
        database='sami_ai'        # Your database name
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
def register_user(username, email, password):
    hashed_password = hash_password(password)
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if user:
            return None, "Username already exists"
        
        cursor.execute("INSERT INTO users (username, password,email) VALUES (%s, %s,%s)", (username, hashed_password,email))
        connection.commit()
        cursor.close()
        connection.close()
        return True, "User registered successfully"
        
    except Error as e:
        return None, str(e)

# Function to authenticate user during login
def authenticate_user(email, password):
    hashed_password = hash_password(password)
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, hashed_password))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            user_id = user[0]
            token = create_token(user_id)
            return token, None
        else:
            return None, "Invalid email or password"
        
    except Error as e:
        return None, str(e)
