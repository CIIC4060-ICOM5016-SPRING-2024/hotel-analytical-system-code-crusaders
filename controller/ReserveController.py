from flask import jsonify
from model.ReserveDAO import ReserveDAO

class ReserveController:

    def DictBuild(self, row):
        result = []
        for tuples in row:
            d = dict()
            d['reid'] = tuples[0]
            d['ruid'] = tuples[1]
            d['clid'] = tuples[2]
            d['total_cost'] = tuples[3]
            d['payment'] = tuples[4]
            d['guests'] = tuples[5]
            result.append(d)
        return result

    def build_attr_dict(self, reid, ruid, clid, total_cost, payment, guests):
        result = {}
        result["reid"] = reid
        result["ruid"] = ruid
        result["clid"] = clid
        result["total_cost"] = total_cost
        result["payment"] = payment
        result["guests"] = guests
        return result

    def getAllReserve(self):
        dao = ReserveDAO()
        rd_dict = dao.getAllReserve()
        result = self.DictBuild(rd_dict)
        return jsonify(result)

    def getReserveById(self, reid):
        dao = ReserveDAO()
        rd_dict = dao.getReserveById(reid)
        if not rd_dict:
            return jsonify("not found"), 404
        else:
            result = self.DictBuild(rd_dict)
            return jsonify(result)


    def addNewReserve(self, json):
        ruid = json["ruid"]
        clid = json["clid"]
        total_cost = json["total_cost"]
        payment = json["payment"]
        guests = json["guests"]
        dao = ReserveDAO()
        insert_re = dao.insertReserve(ruid, clid, total_cost, payment, guests)
        if not insert_re:
            return jsonify("not added"), 404
        else:
            return jsonify(insert_re), 200 # ONLY THE ID NOT JSON


    def updateReserve(self, reid, json):
        ruid = json["ruid"]
        clid = json["clid"]
        total_cost = json["total_cost"]
        payment = json["payment"]
        guests = json["guests"]
        dao = ReserveDAO()
        update_re = dao.updateReserve(reid, ruid, clid, total_cost, payment, guests)
        result = self.build_attr_dict(reid, ruid, clid, total_cost, payment, guests)
        if not update_re:
            return jsonify('not updated'), 404
        else:
            return jsonify(result), 200

    def deleteReserve(self, reid):
        dao = ReserveDAO()
        result = dao.deleteReserve(reid)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT DELETED"), 404

