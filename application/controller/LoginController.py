from flask import jsonify
from model.LoginDAO import LoginDAO
from controller.BaseController import BaseController

class LoginController(BaseController):

    def __init__(self):
        self.dao = LoginDAO()

    def make_json(self, table):
        # Turn the data to json
        fullJson = []

        for tuple in table:
            dictionary = {
                "lid": tuple[0],
                "eid": tuple[1],
                "username": tuple[2],
                "password": tuple[3],
            }
            fullJson.append(dictionary)
        return fullJson

    def get_all(self):
        result = self.dao.get_loginTable()
        return self.make_json(result)

    def get_byID(self, id):
        return jsonify("Selected Login id")

    def put_byID(self, id):
        return jsonify("Inserted Login id")

    def update_byID(self, id):
        return jsonify("Updated Login id")

    def delete_byID(self, id):
        return jsonify("Deleted Login id")