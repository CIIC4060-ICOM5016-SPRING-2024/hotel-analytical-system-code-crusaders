from config.db import Database 
import psycopg2


class RoomDAO:

    def __init__(self):
        self.db = Database()

    def getAllRooms(self):
        cur = self.db.connection.cursor()
        query = """SELECT * FROM room"""
        cur.execute(query)
        rooms_list = cur.fetchall()

        self.db.close()
        cur.close()

        return rooms_list
    def getRoomID(self,rid):
        cur = self.db.connection.cursor()
        query = """SELECT * FROM room WHERE rid = %s"""
        cur.execute(query,(rid,))
        rooms_list = cur.fetchall()

        self.db.close()
        cur.close()

        return rooms_list
    def createRoombyID(self, rid, hid, rdid, rprice):
        cur = self.db.connection.cursor()
        query1 = """INSERT into room (rid, hid, rdid, rprice) VALUES (%s, %s, %s, %s)"""
        query2 = """SELECT rid, hid, rdid, rpice FROM room WHERE rid = %s"""
        cur.execute(query1, (rid, hid, rdid, rprice))
        cur.execute(query2,(rid,))
        self.db.connection.commit()
        rooms_list = cur.fetchone()

        self.db.close()
        cur.close()

        return rooms_list
    
    def deleteRoombyID(self, rid):
        cur = self.db.connection.cursor()
        query1 = """SELECT * FROM room WHERE rid = %s"""
        query2 = """DELETE FROM room WHERE rid = %s"""
        cur.execute(query1,(rid,))
        rooms_list = cur.fetchone()
        cur.execute(query2,(rid,))
        self.db.connection.commit()

        self.db.close()
        cur.close()

        return rooms_list
    
    def updateRoombyID(self,rid,hid,rdid,rprice):
        cur = self.db.connection.cursor()
        query1 = """UPDATE room SET hid = %s, rdid = %s, rprice = %s WHERE rid = %s"""
        query2 = """SELECT rid,hid,rdid,rprice FROM roomdescription WHERE rid = %s"""
        cur.execute(query1,(rid,hid,rdid,rprice))
        cur.execute(query2,(rid,))
        rooms_list = cur.fetchone()
        self.db.connection.commit()

        self.db.close()
        cur.close()

        return rooms_list