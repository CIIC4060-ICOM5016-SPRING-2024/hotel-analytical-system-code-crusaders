from flask import Flask, request
from flask_cors import CORS
from controller.hotels import Hotels
from controller.chains import Chains
from controller.employee import Employee
from controller.clients import clients
from controller.reserve import reserve

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return "Hello"
#############################################
#                HOTEL
#############################################


@app.route('/codecrusaders/hotel', methods=['GET', 'POST'])
def handleHotels():
    handler = Hotels()
    if request.method == 'POST':
        return handler.createHotel(request.json)
    else:
        return handler.getAllHotels()

@app.route('/codecrusaders/hotel/<int:hid>', methods=['GET','PUT','DELETE'])
def handleHotelsbyID(hid):
    handler = Hotels()
    if request.method == 'GET':
        return handler.getHotelbyID(hid)
    elif request.method == 'PUT':
        return handler.updateHotel(request.json)
    elif request.method == 'DELETE':
        return handler.deleteHotel(hid)

#############################################
#                CHAINS
#############################################


@app.route('/codecrusaders/chains', methods=['GET', 'POST'])
def handleChains():
    handler = Chains()
    if request.method == 'POST':
        return handler.createChain(request.json)
    else:
        return handler.getAllChains()

@app.route('/codecrusaders/chains/<int:chid>', methods=['GET','PUT','DELETE'])
def handleChainsbyID(chid):
    handler = Chains()
    if request.method == 'GET':
        return handler.getChainbyID(chid)
    elif request.method == 'PUT':
        return handler.updateChain(request.json)
    elif request.method == 'DELETE':
        return handler.deleteChain(chid)


#############################################
#                EMPLOYEE
#############################################


@app.route('/codecrusaders/employee', methods=['GET', 'POST'])
def handleEmployees():
    handler = Employee()
    if request.method == 'POST':
        return handler.createEmployee(request.json)
    else:
        return handler.getAllEmployees()
@app.route('/codecrusaders/employee/<int:eid>', methods=['GET','PUT','DELETE'])
def handleEmployeesbyID(eid):
    handler = Employee()
    if request.method == 'GET':
        return handler.getEmployeebyID(eid)
    elif request.method == 'PUT':
        return handler.updateEmployee(request.json)
    elif request.method == 'DELETE':
        return handler.deleteEmployee(eid)


##################################################
#                    ClIENT
##################################################
@app.route('/codecrusaders/client', methods = ['GET', 'POST'])
def handle_clients():
    handler = clients()
    if request.method == 'GET':
        return clients().getAllClients()
    elif request.method == 'POST':
        return handler.addNewClient(request.json)


@app.route('/codecrusaders/client/<int:clid>', methods = ['GET', 'PUT', 'DELETE'])
def handle_clientById(clid):
    if request.method == 'GET':
        return clients().getClientByID(clid)
    elif request.method == 'PUT':
        return clients().updateClient(request.json)
    elif request.method == 'DELETE':
        return clients().deleteClient(clid)
    else:
        return jsonify("method Not Allowed"), 405


##################################################
#                 Reserve
##################################################
@app.route('/codecrusaders/reserve', methods = ['GET', 'POST'])
def handle_reserve():
    if request.method == 'GET':
        return reserve().getAllReserve()
    elif request.method == 'POST':
        return reserve().addNewReserve(request.json)


@app.route('/codecrusaders/reserve/<int:reid>', methods = ['GET', 'PUT', 'DELETE'])
def handle_reserveById(reid):
    if request.method == 'GET':
        return reserve().getReserveById(reid)
    elif request.method == 'PUT':
        return reserve().updateReserve(request.json)
    elif request.method == 'DELETE':
        return reserve().deleteReserve(reid)
    else:
        return jsonify("method Not Allowed"), 405


if __name__ == '__main__':
    app.run(debug=True)