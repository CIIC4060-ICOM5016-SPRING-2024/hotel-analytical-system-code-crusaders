from flask import Flask, request,jsonify
from flask_cors import CORS
from controller.room import RoomController
from controller.room_unavailable import RoomUnavailableController


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

@app.route('/room')
def room():
    return RoomController().getAllRooms()

"""
===============================================
              ROOM UNAVAILABLE
===============================================
"""

@app.route('/roomdescription')
def roomdescription():
    return RoomUnavailableController.getRoomUnavailableby()

