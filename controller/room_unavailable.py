from model.room_unavailable import RoomUnavailableDAO
from flask import jsonify 

class RoomUnavailableController:

    def DictBuild(self,row):
        ru_dict = {'ruid': row[0], 'rid': row[1], 'startdate': row[2], 'enddate': row[3]}
        return ru_dict
    
    @staticmethod
    def json_dict(tuples):
         result = []
         for tup in tuples:
             rmu_dict = {
                 'ruid': tup[0],
                 'rid': tup[1],
                 'startdate': tup[2],
                 'enddate': tup[3],
             }
             result.append(rmu_dict)
         return result


    def getAllRoomsUnavailable(self):
        dao = RoomUnavailableDAO()
        rum_dict = dao.getAllRoomsUnavailable()
        result = []
        for element in rum_dict:
            result.append(self.DictBuild(element))


        return jsonify(result)
    
    def getRoomUnavailablebyID(self,ruid):
        dao = RoomUnavailableDAO()
        roomun = dao.getRoomUnavailablebyID(ruid)
        if not roomun:
            return jsonify("Not Found"), 404 
        else: 
            result = self.json_dict(roomun)
            return result
        
    def createRoomUnavailablebyID(self,json):
        ruid = json['ruid']
        rid = json['rid']
        startdate = json['startdate']
        enddate = json['enddate']
        dao = RoomUnavailableDAO()
        roomun = dao.createRoomUnavailablebyID(ruid,rid,startdate,enddate)
        if not roomun:
            return jsonify("Not found") , 404 
        else: 
            result = self.json_dict(roomun)
            return result 
        
    def deleteRoomUnavailablebyID(self,ruid):
        dao = RoomUnavailableDAO()
        roomun = dao.deleteRoomUnavailablebyID(ruid)
        if not roomun:
            return jsonify("Not found") , 404
        else:
            result = self.json_dict(roomun)
            return result
        
    def updateRoomUnavailablebyID(self,json):
        ruid = json['ruid']
        rid = json['rid']
        startdate = json['startdate']
        enddate = json['enddate']
        dao = RoomUnavailableDAO()
        roomun = dao.updateRoomUnavailablebyID(ruid,rid,startdate,enddate)
        if not roomun:
            return jsonify("Not found") , 404
        else: 
            result = self.json_dict(roomun)
            return result