from flask import Flask, jsonify
from flask_cors import CORS

from config.Database import Database
from controller.LoginController import LoginController

# Define the server type
SERVER = "docker"
# Load database credentials
Database.load_credentials(SERVER)

# Create the Flask application
app = Flask(__name__)
# Instantiate the app with CORS
CORS(app)


@app.route('/code-crusaders/login', methods = ['GET'])
def getAllUsers():
    if request.method == 'GET':
        loginController = LoginController()
        return jsonify(loginController.getAllUsers())
    else:
        return jsonify("Operation not supported"), 404

# Run the application on debug mode
if __name__ == "__main__":
    app.run(debug = True)