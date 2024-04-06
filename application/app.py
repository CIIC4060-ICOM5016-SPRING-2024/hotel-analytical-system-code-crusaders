from flask import Flask, jsonify, request
from flask_cors import CORS

from config.Database import Database
from controller.LoginController import LoginController
from controller.RoomDescriptionController import RoomDescriptionController
from controller.StatisticsController import StatisticsController

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
    'roomdescription': RoomDescriptionController
}

@app.route('/code-crusaders/<entity>', methods = ['GET', 'POST'])
def handle_request_all(entity):

    if entity not in controller_mapping:
        return jsonify(f'Invalid entity: {entity} provided'), 404
    
    # Instantiate the corresponding controller object
    controller_class = controller_mapping[entity]
    controller = controller_class()

    if request.method == 'GET':
        return controller.get_all()
    
    elif request.method == 'POST':
        if request.is_json:
            return controller.create(request.json)
        else:
            return jsonify(f"The request does not contain JSON data"), 400
    else:
        # return error
        return jsonify(f"Method: {request.method} Not Allowed"), 405
    
@app.route('/code-crusaders/<entity>/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
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
    
    elif request.method == 'DELETE':
        return controller.delete_byID(id)
    
    elif request.method == 'PUT':
        if request.is_json:
            return controller.update_byID(id, request.json)
        else:
            return jsonify(f"The request does not contain JSON data"), 400
    else:
        # return error
        return jsonify(f"Method: {request.method} Not Allowed"), 405



@app.route('/code-crusaders/hotel/<int:id>/<string:local_statistic>', methods = ['POST'])
def handle_local_statistic_request_byID(id, local_statistic):

    # validate login request 
    if not request.is_json:
        return jsonify(f"The request does not contain JSON data"), 400
    
    # Instantiate the corresponding controller object
    controller = StatisticsController()

    # user validation before reading statistics
    userlogon = LoginController()
    accessLevel = userlogon.login_user(request.json)

    if accessLevel is None:
        return jsonify(f"Incorrect Username or Password"), 400
    
    if accessLevel['position'] == 'Regular' and accessLevel['hid'] != id:
        return jsonify(f"Regular employees cannot watch statistics of other hotels")
    

    # Handle the request method
    if local_statistic == 'handicaproom':
        return controller.get_Handicaproom(id)
    if local_statistic == 'mostdiscount':
        return controller.get_MostDiscount(id)
    else:
        # return error
        return jsonify(f"local_statistic: {local_statistic} does not exist!"), 404


@app.route('/code-crusaders/most/<string:type>', methods = ['POST'])
def handle_global_statistics(type): 
    # validate login request 
    if not request.is_json:
        return jsonify(f"The request does not contain JSON data"), 400
    
    # Instantiate the corresponding controller object
    controller = StatisticsController()

    # user validation before reading statistics
    userlogon = LoginController()
    accessLevel = userlogon.login_user(request.json)

    if accessLevel is None:
        return jsonify(f"Incorrect Username or Password"), 400

    if accessLevel['position'] != 'Administrator':
        return jsonify(f"Only Admins can watch global statistics")

    # Handle the request method
    if type == 'revenue':
        return controller.get_MostRevenue()
    else:
        # return error
        return jsonify(f"global_statistic: {type} does not exist!"), 404


# Run the application on debug mode
if __name__ == "__main__":
    app.run(debug = True)