from flask import jsonify
from controller.BaseController import BaseController

class RoomDescription(BaseController):

    def __init__(self):

        pass

    def get_all(self):
        return jsonify("All Room id")

    def get_byID(self, id):
        return jsonify("Seleced Room id")

    def put_byID(self, id):
        return jsonify("Inserted Room id")

    def update_byID(self, id):
        return jsonify("Updated Room id")

    def delete_byID(self, id):
        return jsonify("Deleted Room id")