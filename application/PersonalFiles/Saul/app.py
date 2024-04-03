from flask import Flask, request, jsonify
from flask_cors import CORS
from controller.clients import clients
from controller.roomDescription import roomDescription

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return "Hello World!"


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
#                RoomDescription
##################################################
@app.route('/codecrusaders/roomdescription', methods = ['GET', 'POST'])
def handle_roomDescription():
    if request.method == 'GET':
        return roomDescription().getAllRoomDescription()
    elif request.method == 'POST':
        return roomDescription().addNewRoomDescription(request.json)


@app.route('/codecrusaders/roomdescription/<int:rdid>', methods = ['GET', 'PUT', 'DELETE'])
def handle_roomDescpriptionById(rdid):
    if request.method == 'GET':
        return roomDescription().getRoomDescriptionByID(rdid)
    elif request.method == 'PUT':
        return roomDescription().updateRoomDescription(request.json)
    elif request.method == 'DELETE':
        return roomDescription().deleteRoomDescription(rdid)
    else:
        return jsonify("method Not Allowed"), 405

if __name__ == '__main__':
    app.run(debug=True)