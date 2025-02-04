from flask import request, jsonify
from models.file_model import process_uploaded_file,getDataExternalClient
from views.responses import json_response

# File upload route
# def upload_file():
#     if 'file' not in request.files:
#         return json_response({"error": "No file part"}, 400)
    
#     file = request.files['file']
    
#     if file.filename == '':
#         return json_response({"error": "No selected file"}, 400)
    
#     if file and file.filename.endswith('.csv'):
#         data, error = process_uploaded_file(file)
#         if error:
#             return json_response({"error": error}, 400)
        
#         return jsonify({"data": data})

#     return json_response({"error": "Invalid file format, please upload a CSV file."}, 400)

def upload_file():
    if 'file' not in request.files:
        return json_response({"error": "No file part"}, 400)
    
    file = request.files['file']
    
    if file.filename == '':
        return json_response({"error": "No selected file"}, 400)
    
    if file and file.filename.endswith('.csv'):
        data, error = process_uploaded_file(file)
        if error:
            return json_response({"error": error}, 400)
        
        return jsonify({"data": data})

    return json_response({"error": "Invalid file format, please upload a CSV file."}, 400)    




# def getListingExternalClient():


#     data=getDataExternalClient()


#     return json({response})


def getListingExternalClient():
    # Fetch the data from the model
    data = getDataExternalClient()

    # Format the data as a list of dictionaries to make it JSON-serializable
    response = []
    for user in data:
        response.append({
            'id': user[0],        
            'username': user[1],  
            'email': user[2],   
            'created_at':user[6]
        })

    # Return the response as JSON
    return jsonify(response)


