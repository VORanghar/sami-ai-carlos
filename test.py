from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import mysql.connector
from mysql.connector import Error
import hashlib
import datetime
import jwt

#upload csv import starts here
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import os
from sklearn.preprocessing import LabelEncoder
#ends here


SECRET_KEY = 'your_secret_key'

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

# MySQL connection details
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',         # Your MySQL host
        user='admin',              # Your MySQL username
        password='Mrmoon@1234', # Your MySQL password
        database='user_db'        # Your database name
    )
    return connection

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

 # Function to create JWT token
def create_token(user_id):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 1-hour expiration
    token = jwt.encode({
        'user_id': user_id,
        'exp': expiration_time
    }, SECRET_KEY, algorithm='HS256')
    return token   

# Registration route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not password or not email:
        return jsonify({'message': 'Username,password and email are required','status':3}), 400

    # Hash the password before storing it
    hashed_password = hash_password(password)

    # Connect to the database and insert the new user
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if the username already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            return jsonify({'message': 'Username already exists','status':2}), 400

        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, password,email) VALUES (%s, %s,%s)", (username, hashed_password,email))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'User registered successfully','status':1}), 201

    except Error as e:
        return jsonify({'message': str(e)}), 500

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required','status':3}), 400

    # Hash the password to compare with stored one
    hashed_password = hash_password(password)

    # Connect to the database and check if the user exists
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if the username and password match
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, hashed_password))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            user_id = user[0]
            token = create_token(user_id)
            return jsonify({'status':1,'message': 'Login successful','token': token}), 200
        else:
            return jsonify({'status':2,'message': 'Invalid email or password'}), 401

    except Error as e:
        return jsonify({'message': str(e)}), 500



# Define a route to upload the CSV file
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if a file is part of the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    # If no file is selected
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Process the file
    if file and file.filename.endswith('.csv'):
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file)
            
            # Ensure the 'Industry' column is present
            if 'Industry' not in df.columns:
                return jsonify({"error": "'Industry' column not found in the file."}), 400

            # Encode the 'Industry' column as numeric data using LabelEncoder
            le = LabelEncoder()
            df['Industry_encoded'] = le.fit_transform(df['Industry'])
            
            # Example: We’ll assume you're predicting something (e.g., business performance or category) and have 'label' column
            # Replace 'label' with your actual target column if you have one
            if 'label' not in df.columns:
                return jsonify({"error": "'label' column not found in the file."}), 400

            X = df[['Industry_encoded']]  # Features: encoded industry column
            y = df['label']  # Target: Assuming you have a 'label' column

            # Initialize and fit the model
            model = RandomForestClassifier()
            model.fit(X, y)

            # Use the model to make predictions
            predictions = model.predict(X)
            df['predictions'] = predictions

            # Convert the updated dataframe back to JSON format
            result = df.to_dict(orient="records")
            return jsonify({"data": result})

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"error": "Invalid file format, please upload a CSV file."}), 400


# Run the app
if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='103.164.67.19', port=5000, debug=True)