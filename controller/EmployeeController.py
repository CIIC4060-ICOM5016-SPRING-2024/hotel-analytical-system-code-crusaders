from flask import jsonify
from model.EmployeeDAO import EmployeeDAO

class EmployeeController:
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
        return result
    def make_json_one(self, tuples):
        result = []
        d = dict()
        d['eid'] = tuples[0]
        d['hid'] = tuples[1]
        d['fname'] = tuples[2]
        d['lname'] = tuples[3]
        d['age'] = tuples[4]
        d['position'] = tuples[5]
        d['salary'] = tuples[6]
        result.append(d)
        return result
    def getAllEmployees(self):
        model = EmployeeDAO()
        result = model.getAllEmployees()
        response = self.make_json(result)
        return response
    def getEmployeebyID(self,eid):
        model = EmployeeDAO()
        employee = model.getEmployeebyID(eid)
        if not employee:
            return jsonify("Not found"), 404
        else:
            response =  self.make_json_one(employee)
            return response
    def createEmployee(self, json):
        hid = json['hid']
        fname =json['fname']
        lname = json['lname']
        age = json['age']
        position = json['position']
        salary = json['salary']
        model = EmployeeDAO()
        employee = model.createEmployee(hid,fname,lname,age,position,salary)
        if not employee:
            return jsonify("Not found"), 404
        else:
            response = self.make_json_one(employee)
            return response
    def deleteEmployee(self, eid):
        model = EmployeeDAO()
        employee = model.deleteEmployee(eid)
        if not employee:
            return jsonify("Not found"), 404
        else:
            response = self.make_json_one(employee)
            return response
    def updateEmployee(self, json):
        eid = json['eid']
        hid = json['hid']
        fname =json['fname']
        lname = json['lname']
        age = json['age']
        position = json['position']
        salary = json['salary']
        model = EmployeeDAO()
        employee = model.updateEmployee(eid,hid,fname,lname,age,position,salary)
        if not employee:
            return jsonify("Not found"), 404
        else:
            response = self.make_json_one(employee)
            return response