from config.Database import Database 

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
    
    def createRoombyID(self, rid, hid, rdid, rprice):
        rid = Database().queryInsertFetch(
            """INSERT into room (hid, rdid, rprice) VALUES (%s, %s, %s) returning rid""",
            (hid, rdid, rprice,)
        )

        rooms_list = Database().querySelectFrom(
            """SELECT rid, hid, rdid, rpice FROM room WHERE rid = %s""",
            (rid,)
        )
        return rooms_list
    
    def deleteRoombyID(self, rid):
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
            (rid,hid,rdid,rprice)
        )

        if updated is False:
            return[]

        rooms_list = Database().querySelectFrom(
            """SELECT rid,hid,rdid,rprice FROM roomdescription WHERE rid = %s""",
            (rid,)
        )
        return rooms_list