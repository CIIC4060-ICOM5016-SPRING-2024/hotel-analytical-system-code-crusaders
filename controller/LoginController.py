from flask import jsonify
from model.LoginDAO import LoginDAO
from controller.BaseController import BaseController

class LoginController(BaseController):

    login_columns = ['lid', 'eid', 'username', 'password']

    def __init__(self):
        self.dao = LoginDAO()

    def make_json(self, table):
        # Turn the data to json
        fullJson = []

        for tuple in table:
            dictionary = {
                self.login_columns[0]: tuple[0],
                self.login_columns[1]: tuple[1],
                self.login_columns[2]: tuple[2],
                self.login_columns[3]: tuple[3],
            }
            fullJson.append(dictionary)
        return self.handle_one_element(fullJson)

    def get_all(self):
        result = self.dao.get_all()

        if result is None:
            return jsonify(f"No login users in database to display")

        return self.make_json(result)

    def get_byID(self, id):
        result = self.dao.get_byID(id)

        if result is None:
            return jsonify(f"No matching login user for ID:{id}")

        return self.make_json(result)
    
    def delete_byID(self, id):
        result = self.dao.delete_byID(id)

        if result is None:
            return jsonify(f"No matching login user to delete for ID:{id}")

        return self.make_json(result)

    def update_byID(self, id, data):
        
        # Check if the data contains valid columns
        invalid_columns = [col for col in data.keys() if col not in self.login_columns]
        if invalid_columns:
            return jsonify(f"Invalid columns provided: {', '.join(invalid_columns)}"), 400

        if len(data) == 0:
            return jsonify(f"No columns provided to update Record at Login ID:{id}")
       
        result = self.dao.update_byID(id, data)

        return jsonify(result) 


    def create(self, data):
        # Check if the data contains the right ammount of columns of single record
        if len(data) is not len(self.login_columns) - 1:
            return jsonify(f"Invalid count of columns provided: {len(data)}"), 400
        
        # Check if the data contains valid columns
        invalid_columns = [col for col in data.keys() if col not in self.login_columns]
        if invalid_columns:
            return jsonify(f"Invalid columns provided: {', '.join(invalid_columns)}"), 400
        
        result = self.dao.create_record(data)

        if not result:
            return jsonify(f"Could not insert record Login"), 400
        else:
            return jsonify(result)
        

    # def login_user(self, hid, data):
    #     if len(data) != 2:
    #         return ("Incorrect Username or Password", False)
        
    #     # Check if the data contains valid columns
    #     invalid_columns = [col for col in data.keys() if col not in self.login_columns]
    #     if invalid_columns:
    #         return ("Incorrect Username or Password", False)
        
    #     result = self.dao.login_user(data['username'], data['password'])

    #     if result is None:
    #         return ("Incorrect Username or Password", False)
        
    #     accessLevel = {
    #         'position': result[0],
    #         'hid'     : result[1],
    #         'chid'    : result[2]
    #     }

    #     if accessLevel['position'] == 'Regular' and accessLevel['hid'] != hid:
    #         return ("Incorrect Username or Password", False)
        
    #     if accessLevel['position'] == 'Supervisor' and accessLevel['chid'] != self.dao.get_hotel_chain(hid):
    #         return ("Incorrect Username or Password", False)
        
    #     return (accessLevel, True)
    
    def logon(self, data):
        if len(data) != 2:
            return ("Incorrect Username or Password", False)
        
        # Check if the data contains valid columns
        invalid_columns = [col for col in data.keys() if col not in self.login_columns]
        if invalid_columns:
            return ("Incorrect Username or Password", False)
        
        result = self.dao.login_user(data['username'], data['password'])

        if result is None:
            return ("Incorrect Username or Password", False)
        
        accessLevel = {
            'position': result[0],
            'hid'     : result[1],
            'chid'    : result[2]
        }
        
        return (accessLevel, True)
    
    def validate_login(self, hid, accessLevel):
        if accessLevel[0]['position'] == 'Regular' and accessLevel[0]['hid'] != hid:
            return False
        
        if accessLevel[0]['position'] == 'Supervisor' and accessLevel[0]['chid'] != self.dao.get_hotel_chain(hid):
            return False
        
        return True