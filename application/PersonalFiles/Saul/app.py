from flask import Flask, request, jsonify
from flask_cors import CORS
from controller.clients import clients
from controller.reserve import reserve

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