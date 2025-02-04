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


# def getDataExternalClient(role_id=None):
#     try:
#         # Connect to the database
#         connection = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="",
#             database="sami_ai"
#         )
#         cursor = connection.cursor()

#         # Execute the query
#         if role_id:
#             query = "SELECT * FROM users WHERE role_id = %s"
#             cursor.execute(query, (role_id,))
#         else:
#             query = "SELECT * FROM users"
#             cursor.execute(query)

#         # Fetch all the results
#         results = cursor.fetchall()

#         # Return the results
#         return results
    
#     except mysql.connector.Error as db_error:
#         # Handle database connection or query errors
#         print(f"Database error: {str(db_error)}")
#         raise  # Re-raise the exception to be handled by the calling function

#     except Exception as e:
#         # Handle any other errors
#         print(f"Error in getDataExternalClient: {str(e)}")
#         raise  # Re-raise the exception

#     finally:
#         # Ensure that the database connection and cursor are always closed
#         if cursor:
#             cursor.close()
#         if connection:
#             connection.close()


def getDataExternalClient(role_id=None, page=1, per_page=10):
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="Mrmoon@1234",
            database="sami_ai"
        )
        cursor = connection.cursor()

        # Calculate the OFFSET based on page and per_page
        offset = (page - 1) * per_page

        # Execute the query with LIMIT and OFFSET for pagination
        if role_id:
            query = "SELECT * FROM users WHERE role_id = %s LIMIT %s OFFSET %s"
            cursor.execute(query, (role_id, per_page, offset))
        else:
            query = "SELECT * FROM users LIMIT %s OFFSET %s"
            cursor.execute(query, (per_page, offset))

        # Fetch all the results
        results = cursor.fetchall()

        # Get the total number of items (without LIMIT and OFFSET)
        count_query = "SELECT COUNT(*) FROM users"
        if role_id:
            count_query = "SELECT COUNT(*) FROM users WHERE role_id = %s"
            cursor.execute(count_query, (role_id,))
        else:
            cursor.execute(count_query)

        total_items = cursor.fetchone()[0]  # Get the total number of rows

        # Return both the results and the total item count
        return results, total_items

    except mysql.connector.Error as db_error:
        print(f"Database error: {str(db_error)}")
        raise

    except Exception as e:
        print(f"Error in getDataExternalClient: {str(e)}")
        raise

    finally:
        # Ensure that the database connection and cursor are always closed
        if cursor:
            cursor.close()
        if connection:
            connection.close()


#delete user by id starts here

def delete_user_by_id(user_id):
    try:
        # Establish a connection to the MySQL database
        conn = mysql.connector.connect(
            host="your_host",           # e.g. "localhost"
            user="your_username",       # e.g. "root"
            password="your_password",   # your database password
            database="your_database"    # your database name
        )
        cursor = conn.cursor()

        # Write the delete query, using placeholders to avoid SQL injection
        delete_query = "DELETE FROM users WHERE id = %s"
        
        # Execute the query with the user ID
        cursor.execute(delete_query, (user_id,))
        
        # Commit the changes to the database
        conn.commit()

        # Check how many rows were affected (i.e., deleted)
        if cursor.rowcount > 0:
            return True
        else:
            return False
        
    except mysql.connector.Error as e:
        print(f"Error deleting user: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


#ends here            