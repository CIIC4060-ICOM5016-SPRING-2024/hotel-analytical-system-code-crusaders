from flask import jsonify
from model.ChainsDAO import ChainsDAO

class ChainsController:

    def __init__(self):
        pass

    def handle_one_element(self, fullJson):
        if len(fullJson) == 1:
            return fullJson[0]
        else:
            return fullJson
        
    def make_json(self, tuples):
        result = []
        for tup in tuples:
            d = dict()
            d['chid'] = tup[0]
            d['cname'] = tup[1]
            d['springmkup'] = tup[2]
            d['summermkup'] = tup[3]
            d['fallmkup'] = tup[4]
            d['wintermkup'] = tup[5]
            result.append(d)
        return self.handle_one_element(result)
    
    def getAllChains(self):
        model = ChainsDAO()
        result = model.getAllChains()
        response = self.make_json(result)
        return response
    
    def getChainbyID(self, chid):
        model = ChainsDAO()
        chain = model.getChainbyID(chid)
        if not chain:
            return jsonify("Not found"), 404
        else:
            response = self.make_json(chain)
            return response
        
    def createChain(self,json):
        cname = json['cname']
        springmkup = json['springmkup']
        summermkup = json['summermkup']
        fallmkup = json['fallmkup']
        wintermkup = json['wintermkup']
        model = ChainsDAO()
        chain = model.createChain(cname,springmkup,summermkup,fallmkup,wintermkup)
        if not chain:
            return jsonify("Not found"), 404
        else:
            response = self.make_json(chain)
            return response
        
    def deleteChain(self, chid):
        model = ChainsDAO()
        chain = model.deleteChain(chid)
        if not chain:
            return jsonify("Not found"), 404
        else:
            response = self.make_json(chain)
            return response
        
    def updateChain(self,json):
        chid = json['chid']
        cname = json['cname']
        springmkup = json['springmkup']
        summermkup = json['summermkup']
        fallmkup = json['fallmkup']
        wintermkup = json['wintermkup']
        model = ChainsDAO()
        chain = model.updateChain(chid,cname,springmkup,summermkup,fallmkup,wintermkup)
        if not chain:
            return jsonify("Not found"), 404
        else:
            response = self.make_json(chain)
            return response