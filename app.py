from flask import Flask
from controllers.auth_controller import register, login
from controllers.file_controller import upload_file
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Define the SECRET_KEY here

    CORS(app)  # Enable CORS if needed

    # Registering routes
    app.add_url_rule('/register', 'register', register, methods=['POST'])
    app.add_url_rule('/login', 'login', login, methods=['POST'])
    app.add_url_rule('/upload', 'upload', upload_file, methods=['POST'])

    return app

# This ensures the app is only created when we run it directly, avoiding circular imports
if __name__ == '__main__':
    app = create_app()
    # app.run(debug=True)
    app.run(host='103.164.67.19', port=5000, debug=True)
