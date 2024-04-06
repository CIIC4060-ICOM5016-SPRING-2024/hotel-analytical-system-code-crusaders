from model.room import RoomDAO
from flask import jsonify

class RoomController:

    def DictBuild(self,row):
        r_dict = {'rid': row[0], 'hid': row[1], 'rdid': row[2], 'rprice': row[3]}
        return r_dict
    
    @staticmethod
    def json_dict(tuples):
         result = []
         for tup in tuples:
             rm_dict = {
                 'rid': tup[0],
                 'hid': tup[1],
                 'rdid': tup[2],
                 'rprice': tup[3],
             }
             result.append(rm_dict)
         return result


    def getAllRooms(self):
        dao = RoomDAO()
        rm_dict = dao.getAllRooms()
        result = []
        for element in rm_dict:
            result.append(self.DictBuild(element))


        return jsonify(result)
    
    def getRoombyid(self,rid):
        dao = RoomDAO()
        room = dao.getHotelbyID(rid)
        if not room:
            return jsonify("Not Found"), 404 
        else: 
            result = self.json_dict(room)
            return result
    
    def createRoombyID(self,json):
        rid = json['rid']
        hid = json['hid']
        rdid = json['rdid']
        rprice = json['rprice']
        dao = RoomDAO()
        room = dao.createRoombyID(rid,hid,rdid,rprice)
        if not room:
            return jsonify("Not found") , 404 
        else: 
            result = self.json_dict(room)
            return result 
        
    def deleteRoomUnavailablebyID(self,ruid):
        dao = RoomDAO()
        room = dao.deleteRoom(ruid)
        if not room:
            return jsonify("Not found") , 404
        else:
            result = self.json_dict(room)
            return result
        
    def updateRoomUnavailablebyID(self,json):
        rid = json['rid']
        hid = json['hid']
        rdid = json['rdid']
        rprice = json['rprice']
        dao = RoomDAO()
        room = dao.updateRoom(rid,hid,rdid,rprice)
        if not room:
            return jsonify("Not found") , 404
        else: 
            result = self.json_dict(room)
            return result