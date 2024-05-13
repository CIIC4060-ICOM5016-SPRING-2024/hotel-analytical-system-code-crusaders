from config.Database import Database 
import json
import psycopg2
import flask, abort
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
    
    def createRoomUnavailablebyID(self,rid,startdate,enddate):
        inserted = Database().queryInsertFetch(
            """INSERT into roomunavailable (rid, startdate, enddate) VALUES (%s, %s, %s) returning ruid""",
            (rid, startdate, enddate)
        )
        return inserted
    
    def deleteRoomUnavailablebyID(self,ruid):
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM reserve WHERE ruid = %s", (ruid,))
        count = cursor.fetchone()[0]

        if count > 0:
            cursor.close()
            self.connection.close()
            abort(401)  # Unauthorized because associated orders exist

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