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


# def getListingExternalClient():
#     # Fetch the data from the model
#     role_id = request.args.get('role_id', default=None, type=int)
#     data = getDataExternalClient(role_id)

#     # Format the data as a list of dictionaries to make it JSON-serializable
#     response = []
#     for user in data:
#         response.append({
#             'id': user[0],        
#             'username': user[1],  
#             'email': user[2],
#             'role_id':user[4],   
#             'created_at':user[6]
#         })

#     # Return the response as JSON
#     return jsonify(response)



# def getListingExternalClient():
#     try:
#         # Fetch the data from the model
#         role_id = request.args.get('role_id', default=None, type=int)
#         data = getDataExternalClient(role_id)

#         # Format the data as a list of dictionaries to make it JSON-serializable
#         response = []
#         for user in data:
#             response.append({
#                 'id': user[0],        
#                 'username': user[1],  
#                 'email': user[2],
#                 'role_id': user[4],   
#                 'created_at': user[6]
#             })

#         # Return the response as JSON
#         return jsonify(response)

#     except Exception as e:
#         # Log the exception (optional: you could use logging to capture this)
#         print(f"Error in getListingExternalClient: {str(e)}")
        
#         # Return a JSON error message
#         return jsonify({'error': 'An error occurred while fetching data'}), 500


def getListingExternalClient():
    try:
        # Fetch pagination parameters from request
        page = request.args.get('page', default=1, type=int)  # Default to page 1
        per_page = request.args.get('per_page', default=10, type=int)  # Default to 10 items per page
        role_id = request.args.get('role_id', default=None, type=int)

        # Fetch the data from the model with pagination
        data, total_items = getDataExternalClient(role_id, page, per_page)

        # Format the data as a list of dictionaries to make it JSON-serializable
        response = []
        for user in data:
            response.append({
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'role_id': user[4],
                'created_at': user[6]
            })

        # Add pagination info in the response
        pagination = {
            'page': page,
            'per_page': per_page,
            'total_items': total_items,
            'total_pages': (total_items // per_page) + (1 if total_items % per_page > 0 else 0)
        }

        return jsonify({
            'data': response,
            'pagination': pagination
        })

    except Exception as e:
        print(f"Error in getListingExternalClient: {str(e)}")
        return jsonify({'error': 'An error occurred while fetching data'}), 500



#delete user functionality starts here


#ends here


