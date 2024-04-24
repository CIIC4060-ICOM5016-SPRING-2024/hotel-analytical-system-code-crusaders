from flask import jsonify
from model.ChainsDAO import ChainsDAO
from controller.BaseController import BaseController

class ChainsController(BaseController):

    chain_columns = ['chid', 'cname', 'springmkup', 'summermkup', 'fallmkup', 'wintermkup']

    def __init__(self):
        self.dao = ChainsDAO()

    def make_json(self, tuples):
        fulljson = []
        for tup in tuples:
            d = dict()
            d['chid'] = tup[0]
            d['cname'] = tup[1]
            d['springmkup'] = tup[2]
            d['summermkup'] = tup[3]
            d['fallmkup'] = tup[4]
            d['wintermkup'] = tup[5]
            fulljson.append(d)
        return self.handle_one_element(fulljson)
    
    def get_all(self):
        result = self.dao.get_all()

        if result is None:
            return jsonify(f"Not found"), 404
        
        return self.make_json(result)

    def get_byID(self, id):
        chain = self.dao.get_byID(id)
        if not chain:
            return jsonify("Not found"), 404
        else:
            return self.make_json(chain)

    def create(self, data):
        if len(data) is not len(self.chain_columns) - 1:
            return jsonify(f"Invalid count of columns provided: {len(data)}"), 400
        
        # Check if the data contains valid columns
        invalid_columns = [col for col in data.keys() if col not in self.chain_columns]
        if invalid_columns:
            return jsonify(f"Invalid columns provided: {', '.join(invalid_columns)}"), 400
        
        chain = self.dao.createChain(data)
        
        if not chain:
            return jsonify("Not found"), 404
        else:
            return jsonify(chain)
    
    def update_byID(self, id, data):
        # Check if the data contains valid columns
        invalid_columns = [col for col in data.keys() if col not in self.chain_columns]
        if invalid_columns:
            return jsonify(f"Invalid columns provided: {', '.join(invalid_columns)}"), 400

        if len(data) == 0:
            return jsonify(f"No columns provided to update :{id}")
       
        result = self.dao.update_byID(id, data)

        return jsonify(result)

    def delete_byID(self, id):
        result = self.dao.delete_byID(id)

        if result is None:
            return jsonify(f"No matching login user to delete for ID:{id}")

        return self.make_json(result)