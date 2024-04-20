import subprocess

from flask_cors import CORS
from flask import Flask, request, jsonify 

from config.Database import Database

from controller.RoomController            import RoomController
from controller.HotelController           import HotelController
from controller.LoginController           import LoginController
from controller.ClientController          import ClientController
from controller.ChainsController          import ChainsController
from controller.ReserveController         import ReserveController
from controller.EmployeeController        import EmployeeController
from controller.RoomUnavailableController import RoomUnavailableController
from controller.RoomDescriptionController import RoomDescriptionController

from controller.StatisticsController import StatisticsController

app = Flask(__name__)
CORS(app)

# Define the server type
SERVER = "docker"
# Load database credentials
Database.load_credentials(SERVER)

# Define a dictionary mapping resource names to controller classes
controller_mapping = {
    'login':           LoginController,
    'roomdescription': RoomDescriptionController
}

@app.route('/')
def handle_application_start():
    return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>My Flask Application</title>
            </head>
            <body>
                <h1>Welcome to My Flask Application</h1>
                <p>This is the main page of the application.</p>
                <a href="/streamlit">Launch Streamlit</a>
            </body>
            </html>
            '''

@app.route('/streamlit')
def streamlit_route():
    # Launch Streamlit as a subprocess
    subprocess.Popen(['streamlit', 'run', './view/loginView.py'])
    return "Launching Streamlit..."

@app.route('/login', methods = ['POST'])
def handle_firsttime_login(): 
    
    if not request.is_json:
        return jsonify(f"The request does not contain JSON data"), 400
    
    # user validation before reading statistics
    userlogon = LoginController()
    accessLevel = userlogon.login_user(-1, request.json)

    if accessLevel[1] is False:
        return jsonify(accessLevel[0]), 404

    return jsonify(accessLevel)

#############################################
#                HOTEL
#############################################

@app.route('/codecrusaders/hotel', methods=['GET', 'POST'])
def handleHotels():
    handler = HotelController()
    if request.method == 'POST':
        return handler.createHotel(request.json)
    else:
        return handler.getAllHotels()

@app.route('/codecrusaders/hotel/<int:hid>', methods=['GET','PUT','DELETE'])
def handleHotelsbyID(hid):
    handler = HotelController()
    if request.method == 'GET':
        return handler.getHotelbyID(hid)
    elif request.method == 'PUT':
        return handler.updateHotel(hid, request.json)
    elif request.method == 'DELETE':
        return handler.deleteHotel(hid)
    else:
        return jsonify(f"Method: {request.method} Not Allowed"), 405

#############################################
#                CHAINS
#############################################


@app.route('/codecrusaders/chains', methods=['GET', 'POST'])
def handleChains():
    handler = ChainsController()
    if request.method == 'POST':
        return handler.createChain(request.json)
    else:
        return handler.getAllChains()

@app.route('/codecrusaders/chains/<int:chid>', methods=['GET','PUT','DELETE'])
def handleChainsbyID(chid):
    handler = ChainsController()
    if request.method == 'GET':
        return handler.getChainbyID(chid)
    elif request.method == 'PUT':
        return handler.updateChain(chid, request.json)
    elif request.method == 'DELETE':
        return handler.deleteChain(chid)
    else:
        return jsonify(f"Method: {request.method} Not Allowed"), 405


#############################################
#                EMPLOYEE
#############################################


@app.route('/codecrusaders/employee', methods=['GET', 'POST'])
def handleEmployees():
    handler = EmployeeController()
    if request.method == 'POST':
        return handler.createEmployee(request.json)
    else:
        return handler.getAllEmployees()
@app.route('/codecrusaders/employee/<int:eid>', methods=['GET','PUT','DELETE'])
def handleEmployeesbyID(eid):
    handler = EmployeeController()
    if request.method == 'GET':
        return handler.getEmployeebyID(eid)
    elif request.method == 'PUT':
        return handler.updateEmployee(eid, request.json)
    elif request.method == 'DELETE':
        return handler.deleteEmployee(eid)
    else:
        return jsonify(f"Method: {request.method} Not Allowed"), 405


##################################################
#                    ClIENT
##################################################
@app.route('/codecrusaders/client', methods = ['GET', 'POST'])
def handle_clients():
    handler = ClientController()
    if request.method == 'GET':
        return handler.getAllClients()
    elif request.method == 'POST':
        return handler.addNewClient(request.json)
    else:
        return jsonify(f"Method: {request.method} Not Allowed"), 405


@app.route('/codecrusaders/client/<int:clid>', methods = ['GET', 'PUT', 'DELETE'])
def handle_clientById(clid):
    handler = ClientController()
    if request.method == 'GET':
        return handler.getClientByID(clid)
    elif request.method == 'PUT':
        return handler.updateClient(clid, request.json)
    elif request.method == 'DELETE':
        return handler.deleteClient(clid)
    else:
        return jsonify(f"Method: {request.method} Not Allowed"), 405


##################################################
#                 Reserve
##################################################
@app.route('/codecrusaders/reserve', methods = ['GET', 'POST'])
def handle_reserve():
    handler = ReserveController()
    if request.method == 'GET':
        return handler.getAllReserve()
    elif request.method == 'POST':
        return handler.addNewReserve(request.json)
    else:
        return jsonify(f"Method: {request.method} Not Allowed"), 405


@app.route('/codecrusaders/reserve/<int:reid>', methods = ['GET', 'PUT', 'DELETE'])
def handle_reserveById(reid):
    handler = ReserveController()
    if request.method == 'GET':
        return handler.getReserveById(reid)
    elif request.method == 'PUT':
        return handler.updateReserve(reid, request.json)
    elif request.method == 'DELETE':
        return handler.deleteReserve(reid)
    else:
        return jsonify(f"Method: {request.method} Not Allowed"), 405
    

#################################################
#                   ROOM
#################################################


@app.route('/codecrusaders/room', methods = ['GET','POST'])
def handle_room():
    handler = RoomController()
    if request.method == 'GET':
        return handler.getAllRooms()
    elif request.method == 'POST':
        return handler.createRoombyID(request.json)
    else:
        return jsonify(f"Method: {request.method} Not Allowed"), 405
    
@app.route('/codecrusaders/room/<int:rid>', methods = ['GET','PUT','DELETE'])
def handleRoomsbyID(rid):
    handler = RoomController()
    if request.method == 'GET':
        return handler.getRoombyid(rid)
    elif request.method == 'PUT':
        return handler.updateRoombyID(rid, request.json)
    elif request.method == 'DELETE':
        return handler.deleteRoombyID(rid)
    else:
        return jsonify(f"Method: {request.method} Not Allowed"), 405
    


###############################################
#             ROOM UNAVAILABLE
###############################################


@app.route('/codecrusaders/roomunavailable', methods=['GET', 'POST'])
def handleRoomUnavailable():
    handler = RoomUnavailableController()
    if request.method == 'POST':
        return handler.createRoomUnavailablebyID(request.json)
    else:
        return handler.getAllRoomsUnavailable()
    
@app.route('/codecrusaders/roomunavailable/<int:ruid>', methods=['GET','PUT','DELETE'])
def handleRoomUnavailablebyID(ruid):
    handler = RoomUnavailableController()
    if request.method == 'GET':
        return handler.getRoomUnavailablebyID(ruid)
    elif request.method == 'PUT':
        return handler.updateRoomUnavailablebyID(ruid, request.json)
    elif request.method == 'DELETE':
        return handler.deleteRoomUnavailablebyID(ruid)
    else:
        return jsonify(f"Method: {request.method} Not Allowed"), 405

###############################################
#             Login & Room Description
###############################################

@app.route('/codecrusaders/<entity>', methods = ['GET', 'POST'])
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
        return jsonify(f"Method: {request.method} Not Allowed"), 405
    
@app.route('/codecrusaders/<entity>/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def handle_request_byID(entity, id):

    if entity not in controller_mapping:
        return jsonify(f'Invalid entity: {entity} provided'), 404
    
    # Instantiate the corresponding controller object
    controller_class = controller_mapping[entity]
    controller = controller_class()

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
        return jsonify(f"Method: {request.method} Not Allowed"), 405


@app.route('/codecrusaders/hotel/<int:hid>/<string:local_statistic>', methods = ['POST'])
def handle_local_statistic_request_byID(hid, local_statistic):

    # validate login request 
    if not request.is_json:
        return jsonify(f"The request does not contain JSON data"), 400
    
    # Instantiate the corresponding controller object
    controller = StatisticsController()

    # user validation before reading statistics
    userlogon = LoginController()
    accessLevel = userlogon.login_user(hid, request.json)

    if accessLevel[1] is False:
        return jsonify(accessLevel[0]), 404
    
    # Handle the request method
    if local_statistic == 'handicaproom':
        return controller.get_Handicaproom(hid)
    elif local_statistic == 'leastreserve':
        return controller.get_LeastReserve(hid)
    elif local_statistic == 'mostcreditcard':
        return controller.get_MostCreditCard(hid)
    elif local_statistic == 'highestpaid':
        return controller.get_HighestPaid(hid)
    elif local_statistic == 'mostdiscount':
        return controller.get_MostDiscount(hid)
    elif local_statistic == 'roomtype':
        return controller.get_RoomType(hid)
    elif local_statistic == 'leastguests':
        return controller.get_LeastGuests(hid)
    else:
        # return error
        return jsonify(f"local_statistic: {local_statistic} does not exist!"), 404


@app.route('/codecrusaders/most/<string:type>', methods = ['POST'])
def handle_most_global_statistics(type): 
    
    if not request.is_json:
        return jsonify(f"The request does not contain JSON data"), 400
    
    # Instantiate the corresponding controller object
    controller = StatisticsController()

    # user validation before reading statistics
    userlogon = LoginController()
    accessLevel = userlogon.login_user(-1, request.json)

    if accessLevel[1] is False:
        return jsonify(accessLevel[0]), 404

    # Handle the request method
    if type == 'revenue':
        return controller.get_MostRevenue()
    elif type == 'capacity':
        return controller.get_MostCapacity()
    elif type == 'reservation':
        return controller.get_MostReservation()
    elif type == 'profitmonth':
        return controller.get_MostProfitMonth()
    else:
        # return error
        return jsonify(f"global_statistic: {type} does not exist!"), 404


@app.route('/codecrusaders/least/<string:type>', methods = ['POST'])
def handle_least_global_statistics(type): 
    
    if not request.is_json:
        return jsonify(f"The request does not contain JSON data"), 400
    
    # Instantiate the corresponding controller object
    controller = StatisticsController()

    # user validation before reading statistics
    userlogon = LoginController()
    accessLevel = userlogon.login_user(-1, request.json)

    if accessLevel[1] is False:
        return jsonify(accessLevel[0]), 404

    # Handle the request method
    if type == 'rooms':
        return controller.get_LeastRooms()
    else:
        # return error
        return jsonify(f"global_statistic: {type} does not exist!"), 404

@app.route('/codecrusaders/paymentmethod', methods = ['POST'])
def handle_general_global_statistics(): 
    
    if not request.is_json:
        return jsonify(f"The request does not contain JSON data"), 400
    
    # Instantiate the corresponding controller object
    controller = StatisticsController()

    # user validation before reading statistics
    userlogon = LoginController()
    accessLevel = userlogon.login_user(-1, request.json)

    if accessLevel[1] is False:
        return jsonify(accessLevel[0]), 404

    # Handle the request method
    return controller.get_PaymentMethod()

if __name__ == '__main__':
    app.run(debug=True)