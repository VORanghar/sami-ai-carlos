import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from dotenv import load_dotenv
import os
import mysql.connector  # Ensure this import is include
load_dotenv()

# def process_uploaded_file(file):
#     try:
#         # Read the CSV file into a DataFrame
#         df = pd.read_csv(file)
        
#         # Ensure the 'Industry' column is present
#         if 'Industry' not in df.columns:
#             return None, "'Industry' column not found in the file."
        
#         # Encode the 'Industry' column as numeric data using LabelEncoder
#         le = LabelEncoder()
#         df['Industry_encoded'] = le.fit_transform(df['Industry'])
        
#         # Ensure the 'label' column exists
#         # if 'label' not in df.columns:
#         #     return None, "'label' column not found in the file."

#         X = df[['Industry_encoded']]  # Features
#         y = df['label']  # Target
        
#         # Initialize and fit the model
#         model = RandomForestClassifier()
#         model.fit(X, y)

#         # Optionally make predictions
#         # predictions = model.predict(X)
#         # df['predictions'] = predictions

#         return df.to_dict(orient="records"), None

#     except Exception as e:
#         return None, str(e)



def process_uploaded_file(file):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file)
        
        # Ensure the 'Industry' column is present
        if 'Main Heading' not in df.columns:
            return None, "'Main Heading' column not found in the file."
        
        # Encode the 'Industry' column as numeric data using LabelEncoder
        le = LabelEncoder()
        df['Main_Heading_encoded'] = le.fit_transform(df['Main Heading'])
        
        # Ensure the 'label' column exists
        # if 'label' not in df.columns:
        #     return None, "'label' column not found in the file."

        X = df[['Main_Heading_encoded']]  # Features
        y = df['Sub Heading']  # Target
        
        # Initialize and fit the model
        model = RandomForestClassifier()
        model.fit(X, y)

        # Optionally make predictions
        # predictions = model.predict(X)
        # df['predictions'] = predictions

        return df.to_dict(orient="records"), None

    except Exception as e:
        return None, str(e)        



# def getDataExternalClient():
#     select * from users

#     return 




# def getDataExternalClient(role_id=None):
#     # Connect to the database
#     connection = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="",
#         database="sami_ai"
#     )
#     cursor = connection.cursor()
    
#     # Execute the query
#     if role_id:
#         query = "SELECT * FROM users WHERE role_id = %s"
#         cursor.execute(query, (role_id,))
#     else:
#         query = "SELECT * FROM users"
#         cursor.execute(query)
    
#     # Fetch all the results
#     results = cursor.fetchall()
    
#     # Close the connection
#     connection.close()
    
#     # Return the results
#     return results


def getDataExternalClient(role_id=None):
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sami_ai"
        )
        cursor = connection.cursor()

        # Execute the query
        if role_id:
            query = "SELECT * FROM users WHERE role_id = %s"
            cursor.execute(query, (role_id,))
        else:
            query = "SELECT * FROM users"
            cursor.execute(query)

        # Fetch all the results
        results = cursor.fetchall()

        # Return the results
        return results
    
    except mysql.connector.Error as db_error:
        # Handle database connection or query errors
        print(f"Database error: {str(db_error)}")
        raise  # Re-raise the exception to be handled by the calling function

    except Exception as e:
        # Handle any other errors
        print(f"Error in getDataExternalClient: {str(e)}")
        raise  # Re-raise the exception

    finally:
        # Ensure that the database connection and cursor are always closed
        if cursor:
            cursor.close()
        if connection:
            connection.close()