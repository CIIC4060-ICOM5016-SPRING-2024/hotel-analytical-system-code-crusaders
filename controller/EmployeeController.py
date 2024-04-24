from flask import jsonify
from model.EmployeeDAO import EmployeeDAO
from controller.BaseController import BaseController

class EmployeeController(BaseController):

    employee_columns = ['eid', 'hid', 'fname', 'lname', 'age', 'position', 'salary']

    def __init__(self):
        self.dao = EmployeeDAO()

    def make_json(self, tuples):
        result = []
        for tup in tuples:
            d = dict()
            d['eid'] = tup[0]
            d['hid'] = tup[1]
            d['fname'] = tup[2]
            d['lname'] = tup[3]
            d['age'] = tup[4]
            d['position'] = tup[5]
            d['salary'] = tup[6]
            result.append(d)
        return self.handle_one_element(result)
    
    def get_all(self):
        result = self.dao.getAllEmployees()
        return self.make_json(result)

    def get_byID(self, id):
        employee = self.dao.getEmployeebyID(id)
        if employee is None:
            return jsonify("Not found"), 404
        else:
            return self.make_json(employee)

    def create(self, data):
       # Check if the data contains the right ammount of columns of single record
        if len(data) is not len(self.employee_columns) - 1:
            return jsonify(f"Invalid count of columns provided: {len(data)}"), 400
        
        # Check if the data contains valid columns
        invalid_columns = [col for col in data.keys() if col not in self.employee_columns]
        if invalid_columns:
            return jsonify(f"Invalid columns provided: {', '.join(invalid_columns)}"), 400
        
        employee = self.dao.createEmployee(data)

        if not employee:
            return jsonify("Not found"), 404
        else:
            return jsonify(employee)
    
    def update_byID(self, id, data):
        # Check if the data contains valid columns
        invalid_columns = [col for col in data.keys() if col not in self.employee_columns]
        if invalid_columns:
            return jsonify(f"Invalid columns provided: {', '.join(invalid_columns)}"), 400

        if len(data) == 0:
            return jsonify(f"No columns provided to update Record at Login ID:{id}")
        
        employee = self.dao.updateEmployee(id, data)
    
        return jsonify(employee)

    def delete_byID(self, id):
        employee = self.dao.deleteEmployee(id)

        if not employee:
            return jsonify("Not found"), 404
        else:
            return self.make_json(employee)