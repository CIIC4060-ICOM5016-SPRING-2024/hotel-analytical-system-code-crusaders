from flask import Flask, jsonify, request
from flask_cors import CORS

from config.Database import Database
from controller.LoginController import LoginController
from controller.RoomDescription import RoomDescription

# Define the server type
SERVER = "docker"
# Load database credentials
Database.load_credentials(SERVER)

# Create the Flask application
app = Flask(__name__)
# Instantiate the app with CORS
CORS(app)

# Define a dictionary mapping resource names to controller classes
controller_mapping = {
    'login':           LoginController,
    'roomdescription': RoomDescription
}

@app.route('/code-crusaders/<entity>', methods = ['GET'])
def handle_request_all(entity):
    # Check if the entity is valid
    if entity not in controller_mapping:
        return jsonify(f'Invalid entity: {entity} provided'), 404

    # Instantiate the corresponding controller object
    controller_class = controller_mapping[entity]
    controller = controller_class()

    if request.method == 'GET':
        return controller.get_all()
    
    else:
        # return error
        return jsonify(f"Method: {request.method} Not Allowed"), 405

@app.route('/code-crusaders/<entity>/<int:id>', methods = ['GET', 'POST', 'DELETE'])
def handle_request_byID(entity, id):
    # Check if the entity is valid
    if entity not in controller_mapping:
        return jsonify(f'Invalid entity: {entity} provided'), 404
    
    # Instantiate the corresponding controller object
    controller_class = controller_mapping[entity]
    controller = controller_class()

    # Handle the request method
    if request.method == 'GET':
        return controller.get_byID(id)
    
    elif request.method == 'POST':
        return controller.put_byID(id)
    
    elif request.method == 'DELETE':
        return controller.delete_byID(id)
    
    else:
        # return error
        return jsonify(f"Method: {request.method} Not Allowed"), 405

# Run the application on debug mode
if __name__ == "__main__":
    app.run(debug = True)