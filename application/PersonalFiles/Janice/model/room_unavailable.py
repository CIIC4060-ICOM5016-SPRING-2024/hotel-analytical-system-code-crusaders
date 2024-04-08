from config.db import Database 
import psycopg2


class RoomUnavailableDAO:

    def __init__(self):
        self.db = Database()

    def getAllRoomsUnavailable(self):
        cur = self.db.connection.cursor()
        query = """SELECT * FROM roomunavailable"""
        cur.execute(query)
        roomsun_list = cur.fetchall()

        self.db.close()
        cur.close()

        return roomsun_list
    
    def getRoomUnavailablebyID(self,ruid):
        cur = self.db.connection.cursor()
        query = """SELECT * FROM roomunavailable WHERE ruid = %s"""
        cur.execute(query,(ruid,))
        roomsun_list = cur.fetchall()

        self.db.close()
        cur.close()

        return roomsun_list
    
    def createRoomUnavailablebyID(self,ruid,rid,startdate,enddate):
        cur = self.db.connection.cursor()
        query1 = """INSERT into roomunavailable (ruid, rid, startdate, enddate) VALUES (%s, %s, %s, %s)"""
        query2 = """SELECT ruid, rid, startdate, enddate FROM roomunavailable WHERE ruid = %s"""
        cur.execute(query1, (ruid, rid, startdate, enddate))
        cur.execute(query2,(ruid,))
        self.db.connection.commit()
        roomsun_list = cur.fetchone()

        self.db.close()
        cur.close()

        return roomsun_list
    
    def deleteRoomUnavailablebyID(self,ruid):
        cur = self.db.connection.cursor()
        query1 = """SELECT * FROM roomunavailable WHERE ruid = %s"""
        query2 = """DELETE FROM roomunavailable WHERE ruid = %s"""
        cur.execute(query1,(ruid,))
        roomsun_list = cur.fetchone()
        cur.execute(query2,(ruid,))
        self.db.connection.commit()

        self.db.close()
        cur.close()

        return roomsun_list
    
    def updateRoomUnavailablebyID(self,ruid,rid,startdate,enddate):
        cur = self.db.connection.cursor()
        query1 = """UPDATE roomunavailable SET rid = %s, startdate = %s, enddate = %s WHERE ruid = %s"""
        query2 = """SELECT ruid,rid,startdate,enddate FROM roomunavailable WHERE ruid = %s"""
        cur.execute(query1,(ruid,rid,startdate,enddate))
        cur.execute(query2,(ruid,))
        roomsun_list = cur.fetchone()
        self.db.connection.commit()

        self.db.close()
        cur.close()

        return roomsun_list