import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

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



