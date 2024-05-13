from config.Database import Database 
import json
import psycopg2
import flask, abort
class RoomDAO:

    def __init__(self):
        pass

    def getAllRooms(self):
        rooms_list = Database().querySelectFrom(
            """SELECT * FROM room""",
            ()
        )
        return rooms_list
    
    def getRoomID(self,rid):
        rooms_list = Database().querySelectFrom(
            """SELECT * FROM room WHERE rid = %s""",
            (rid,)
        )
        return rooms_list
    
    def createRoombyID(self, hid, rdid, rprice):
        rid = Database().queryInsertFetch(
            """INSERT into room (hid, rdid, rprice) VALUES (%s, %s, %s) returning rid""",
            (hid, rdid, rprice,)
        )

        rooms_list = Database().querySelectFrom(
            """SELECT rid, hid, rdid, rprice FROM room WHERE rid = %s""",
            (rid,)
        )
        return rooms_list
    
    def deleteRoombyID(self, rid):
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM roomunavailable WHERE rid = %s", (rid,))
        count = cursor.fetchone()[0]

        if count > 0:
            cursor.close()
            self.connection.close()
            abort(401)  # Unauthorized because associated orders exist
            
        rooms_list = Database().querySelectFrom(
            """SELECT * FROM room WHERE rid = %s""",
            (rid,)
        )

        result = Database().queryDelete(
            """DELETE FROM room WHERE rid = %s""",
            (rid,)
        )

        if result is False:
            return []
        return rooms_list
    
    def updateRoombyID(self,rid,hid,rdid,rprice):
        updated = Database().queryUpdate(
            """UPDATE room SET hid = %s, rdid = %s, rprice = %s WHERE rid = %s""",
            (hid,rdid,rprice,rid,)
        )

        if updated is False:
            return[]

        rooms_list = Database().querySelectFrom(
            """SELECT rid,hid,rdid,rprice FROM room WHERE rid = %s""",
            (rid,)
        )
        return rooms_list