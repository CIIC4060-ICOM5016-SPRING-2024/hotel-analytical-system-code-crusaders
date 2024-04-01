from model.chains import ChainsDAO
from flask import jsonify
class Chains:
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
        return result
    def make_json_one(self,tuples):
        result = []
        d = dict()
        d['chid'] = tuples[0]
        d['cname'] = tuples[1]
        d['springmkup'] = tuples[2]
        d['summermkup'] = tuples[3]
        d['fallmkup'] = tuples[4]
        d['wintermkup'] = tuples[5]
        result.append(d)
        return result
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
            response = self.make_json_one(chain)
            return response
    def createChain(self,chid,cname,springmkup,summermkup,fallmkup,wintermkup):
        if not chid and not cname and not springmkup and not summermkup and not fallmkup and not wintermkup:
            return jsonify("Please verify submission values"), 404
        model = ChainsDAO()
        chain = model.createChain(chid,cname,springmkup,summermkup,fallmkup,wintermkup)
        if not chain:
            return jsonify("Not found"), 404
        else:
            response = self.make_json_one(chain)
            return response
    def deleteChain(self, chid):
        model = ChainsDAO()
        chain = model.deleteChain(chid)
        if not chain:
            return jsonify("Not found"), 404
        else:
            response = self.make_json_one(chain)
            return response
    def updateChain(self,chid,cname,springmkup,summermkup,fallmkup,wintermkup):
        if not chid and not cname and not springmkup and not summermkup and not fallmkup and not wintermkup:
            return jsonify("Please verify submission values"), 404
        model = ChainsDAO()
        chain = model.updateChain(chid,cname,springmkup,summermkup,fallmkup,wintermkup)
        if not chain:
            return jsonify("Not found"), 404
        else:
            response = self.make_json_one(chain)
            return response