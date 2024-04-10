from config.Database import Database 

class RoomUnavailableDAO:

    def __init__(self):
        pass

    def getAllRoomsUnavailable(self):
        roomsun_list = Database().querySelectFrom(
            """SELECT * FROM roomunavailable""",
            ()
        )
        return roomsun_list
    
    def getRoomUnavailablebyID(self,ruid):
        roomsun_list = Database().querySelectFrom(
            """SELECT * FROM roomunavailable WHERE ruid = %s""",
            (ruid,)
        )
        return roomsun_list
    
    def createRoomUnavailablebyID(self,ruid,rid,startdate,enddate):
        inserted = Database().queryInsertFetch(
            """INSERT into roomunavailable (rid, startdate, enddate) VALUES (%s, %s, %s) returning ruid""",
            (rid, startdate, enddate)
        )

        roomsun_list = Database().querySelectFrom(
            """SELECT ruid, rid, startdate, enddate FROM roomunavailable WHERE ruid = %s""",
            (ruid,)
        )
        return roomsun_list
    
    def deleteRoomUnavailablebyID(self,ruid):
        roomsun_list = Database().querySelectFrom(
            """SELECT * FROM roomunavailable WHERE ruid = %s""",
            (ruid,)
        )

        deleted = Database().queryDelete(
            """DELETE FROM roomunavailable WHERE ruid = %s""",
            (ruid,)
        )
        
        if deleted is False:
            return []
        return roomsun_list
    
    def updateRoomUnavailablebyID(self,ruid,rid,startdate,enddate):

        updated = Database().queryUpdate(
            """UPDATE roomunavailable SET rid = %s, startdate = %s, enddate = %s WHERE ruid = %s""",
            (rid,startdate,enddate, ruid)
        )

        if updated is False:
            return []
        
        roomsun_list = Database().querySelectFrom(
            """SELECT ruid,rid,startdate,enddate FROM roomunavailable WHERE ruid = %s""",
            (ruid,)
        )
        return roomsun_list