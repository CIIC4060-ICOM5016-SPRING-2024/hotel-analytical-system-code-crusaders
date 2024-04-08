from flask import Flask, request,jsonify
from flask_cors import CORS
from controller.RoomController import RoomController
from controller.RoomUnavailableController import RoomUnavailableController


app = Flask(__name__)
CORS(app)

@app.route('/')
def home_page():
    return "<p> Hello Code Crusaders <p>"


"""
===============================================
                    ROOM
===============================================
"""

@app.route('/codecrusaders/room', methods = ['GET','POST'])
def handle_room():
    handler = RoomController()
    if request.method == 'GET':
        return RoomController().getAllRooms()
    elif request.method == 'POST':
        return handler.createRoombyID(request.json)
    
@app.route('/codecrusaders/room/<int:rid', method = ['GET','PUT','DELETE'])
def handleRoomsbyID(rid):
    handler = RoomController()
    if request.method == 'GET':
        return handler.getRoombyid(rid)
    elif request.method == 'PUT':
        return handler.updateRoombyID(request.json)
    elif request.method == 'DELETE':
        return handler.deleteRoombyID(rid)
    

"""
===============================================
              ROOM UNAVAILABLE
===============================================
"""

@app.route('/codecrusaders/room_unavailable', methods=['GET', 'POST'])
def handleRoomUnavailable():
    handler = RoomUnavailableController()
    if request.method == 'POST':
        return handler.createRoomUnavailablebyID(request.json)
    else:
        return handler.getAllRoomsUnavailable()
    
@app.route('/codecrusaders/room_unavailable/<int:ruid>', methods=['GET','PUT','DELETE'])
def handleRoomUnavailablebyID(ruid):
    handler = RoomUnavailableController()
    if request.method == 'GET':
        return handler.getRoomUnavailablebyID(ruid)
    elif request.method == 'PUT':
        return handler.updateRoomUnavailablebyID(ruid)
    elif request.method == 'DELETE':
        return handler.deleteRoomUnavailablebyID(ruid)
    


if __name__ == '__main__':
    app.run(debug=True)