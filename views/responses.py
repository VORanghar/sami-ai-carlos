from flask import jsonify

def json_response(message, status_code):
    return jsonify(message), status_code
