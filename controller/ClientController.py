from flask import jsonify
from model.ClientDAO import ClientDAO

class ClientController:

    def DictBuild(self, row):
        result = []
        for tuples in row:
            d = dict()
            d['clid'] = tuples[0]
            d['fname'] = tuples[1]
            d['lname'] = tuples[2]
            d['age'] = tuples[3]
            d['memberyear'] = tuples[4]
            result.append(d)
        return result

    def build_attr_dict(self, clid, fname, lname, age, memberyear):
        result = {}
        result['clid'] = clid
        result['fname'] = fname
        result['lname'] = lname
        result['age'] = age
        result['memberyear'] = memberyear
        return result

    def getAllClients(self):
        model = ClientDAO()
        client_dict = model.getAllClients()
        result = []
        for element in client_dict:
            result.append(self.DictBuild(element))

        return jsonify(result)


    def getClientByID(self, clid):
        model = ClientDAO()
        client_dict = model.getAllClients()
        result = self.DictBuild(client_dict)
        return jsonify(result)

    def addNewClient(self, json):
        fname = json['fname']
        lname = json['lname']
        age = json['age']
        memberyear = json['memberyear']
        dao = ClientDAO()
        insertclient = dao.insertClient(fname, lname, age, memberyear)
        result = self.build_attr_dict(insertclient, fname, lname, age, memberyear)  # insertClient returns id of tuple
        if not insertclient:
            return jsonify("not added"), 404
        else:
            return jsonify(result), 201

    def updateClient(self, json):
        clid = json['clid']
        fname = json['fname']
        lname = json['lname']
        age = json['age']
        memberyear = json['memberyear']
        dao = ClientDAO()
        updateclient = dao.updateClient(clid, fname, lname, age, memberyear)
        result = self.build_attr_dict(clid, fname, lname, age, memberyear)
        if not updateclient:
            return jsonify("not upadted"), 404
        else:
            return jsonify(result), 200

    def deleteClient(self, clid):
        dao = ClientDAO()
        result = dao.deleteClient(clid)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404