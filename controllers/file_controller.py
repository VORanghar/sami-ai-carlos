from flask import request, jsonify
from models.file_model import process_uploaded_file
from views.responses import json_response

# File upload route
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
