from model.roomDescription import roomDescriptionDAO
from flask import jsonify

class roomDescription:

    def DictBuild(self, row):
        a_dict = {"rdid": row[0], "rname": row[1], "rtype": row[2], "capacity": row[3], "ishandicap": row[4]}
        return a_dict

    def build_attr_dict(self, rdid, rname, rtype, capacity, ishandicap):
        result = {}
        result["rdid"] = rdid
        result["rname"] = rname
        result["rtype"] = rtype
        result["capacity"] = capacity
        result["ishandicap"] = ishandicap
        return result

    def getAllRoomDescription(self):
        dao = roomDescriptionDAO()
        rd_dict = dao.getAllRoomDescription()
        result = []
        for element in rd_dict:
            result.append(self.DictBuild(element))

        return jsonify(result)

    def getRoomDescriptionByID(self, rdid):
        dao = roomDescriptionDAO()
        rd_dict  = dao.getRoomDescriptionsById(rdid)
        if not rd_dict:
            return jsonify("not found"), 404
        else:
            result = []
            result.append(self.DictBuild(rd_dict))
            return jsonify(result)


    def addNewRoomDescription(self, json):
        rname = json["rname"]
        rtype = json["rtype"]
        capacity = json["capacity"]
        ishandicap = json["ishandicap"]
        dao = roomDescriptionDAO()
        insertrd = dao.insertRoomDescription(rname, rtype, capacity, ishandicap)
        result = self.build_attr_dict(insertrd, rname, rtype, capacity, ishandicap) # rdcreate returns of inserted tuple
        if not insertrd:
            return jsonify("not added"), 404
        else:
            return jsonify(result), 201


    def updateRoomDescription(self, json):
        rdid = json["rdid"]
        rname = json["rname"]
        rtype = json["rtype"]
        capacity = json["capacity"]
        ishandicap = json["ishandicap"]
        dao = roomDescriptionDAO()
        updaterd = dao.updateRoomDescription(rdid, rname, rtype, capacity, ishandicap)
        result = self.build_attr_dict(rdid, rname, rtype, capacity, ishandicap)
        if not updaterd:
            return jsonify('not updated'), 404
        else:
            return jsonify(result), 200

    def deleteRoomDescription(self, rdid):
        dao = roomDescriptionDAO()
        result = dao.deleteRoomDescription(rdid)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT DELETED"), 404