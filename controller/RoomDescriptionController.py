from flask import jsonify
from controller.BaseController import BaseController
from model.RoomDescriptionDAO import RoomDescriptionDAO

class RoomDescriptionController(BaseController):

    roomDescription_columns = ['rdid', 'rname', 'rtype', 'capacity', 'ishandicap']

    def __init__(self):
        self.dao = RoomDescriptionDAO()

    def handle_one_element(self, fullJson):
        if len(fullJson) == 1:
            return fullJson[0]
        else:
            return fullJson

    def make_json(self, table):
        # Turn the data to json
        fullJson = []

        for tuple in table:
            dictionary = {
                self.roomDescription_columns[0]: tuple[0],
                self.roomDescription_columns[1]: tuple[1],
                self.roomDescription_columns[2]: tuple[2],
                self.roomDescription_columns[3]: tuple[3],
                self.roomDescription_columns[4]: tuple[4],
            }
            fullJson.append(dictionary)
        return self.handle_one_element(fullJson)

    def get_all(self):
        result = self.dao.get_all()

        if result is None:
            return jsonify(f"No room description in database to display")

        return self.make_json(result)

    def get_byID(self, id):
        result = self.dao.get_byID(id)

        if result is None:
            return jsonify(f"No matching room description for ID:{id}")

        return self.make_json(result)
    
    def delete_byID(self, id):
        result = self.dao.delete_byID(id)

        if result is None:
            return jsonify(f"No matching room description to delete for ID:{id}")

        return self.make_json(result)

    def update_byID(self, id, data):
        
        # Check if the data contains valid columns
        invalid_columns = [col for col in data.keys() if col not in self.roomDescription_columns]
        if invalid_columns:
            return jsonify(f"Invalid columns provided: {', '.join(invalid_columns)}"), 400

        if len(data) == 0:
            return jsonify(f"No columns provided to update Record at room description ID:{id}")
       
        result = self.dao.update_byID(id, data)

        if result == True:
            return jsonify(f"Updated Record at room description ID:{id}") 

        return jsonify(f"Could not update Record at room description ID:{id}")


    def create(self, data):
        # Check if the data contains the right ammount of columns of single record
        if len(data) is not len(self.roomDescription_columns) - 1:
            return jsonify(f"Invalid count of columns provided: {len(data)}"), 400
        
        # Check if the data contains valid columns
        invalid_columns = [col for col in data.keys() if col not in self.roomDescription_columns]
        if invalid_columns:
            return jsonify(f"Invalid columns provided: {', '.join(invalid_columns)}"), 400
        
        result = self.dao.create_record(data)

        if not result:
            return jsonify(f"Could not insert record room description"), 400
        else:
            return jsonify(result) 
