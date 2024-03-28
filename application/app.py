from flask import Flask
from flask_cors import CORS

from config.Database import Database
from controller.LoginController import LoginController

SERVER = "heroku"

# Create the Flask application
app = Flask(__name__)
# Instantiate the app with CORS
CORS(app)

@app.route('/duro', methods=['GET'])
def hello_world():
    loginController = LoginController()

    return loginController.getAllUsers()

# Run the application on debug mode
if __name__ == "__main__":
    Database.load_credentials(SERVER)
    app.run(debug = True)