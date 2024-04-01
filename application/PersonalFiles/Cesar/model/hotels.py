from model.db import Database
class HotelsDAO:
    def __init__(self):
        self.db = Database()
    def getAllHotels(self):
        cur = self.db.connection.cursor()
        query = """SELECT * FROM hotel"""
        cur.execute(query)
        hotel_list = cur.fetchall()
        self.db.close()
        cur.close()
        return hotel_list

    def getHotelbyID(self,hid):
        cur = self.db.connection.cursor()
        query = """SELECT * FROM hotel where hid = %s"""
        cur.execute(query,(hid,))
        hotel_list = cur.fetchone()
        self.db.close()
        cur.close()
        return hotel_list
    def createHotel(self,hid,chid,hname,hcity):
        cur = self.db.connection.cursor()
        query1 = """INSERT INTO hotel (hid,chid,hname,hcity) VALUES (%s,%s,%s,%s)"""
        query2 = """SELECT hid,chid,hname,hcity FROM hotel where hid = %s"""
        cur.execute(query1,(hid,chid,hname,hcity))
        cur.execute(query2,(hid,))
        hotel_list = cur.fetchone()
        self.db.connection.commit()
        self.db.close()
        cur.close()
        return hotel_list
    def deleteHotel(self,hid):
        cur = self.db.connection.cursor()
        query1 = """SELECT * FROM hotel where hid = %s"""
        query2 = """DELETE FROM hotel where hid = %s"""
        cur.execute(query1,(hid,))
        hotel_list = cur.fetchone()
        cur.execute(query2,(hid,))
        self.db.connection.commit()
        self.db.close()
        cur.close()
        return hotel_list
    def updateHotel(self,hid,chid,hname,hcity):
        cur = self.db.connection.cursor()
        query1 = """UPDATE hotel SET chid = %s, hname = %s, hcity = %s WHERE hid = %s"""
        query2 = """SELECT hid,chid,hname,hcity FROM hotel where hid = %s"""
        cur.execute(query1,(chid,hname,hcity,hid))
        cur.execute(query2,(hid,))
        hotel_list = cur.fetchone()
        self.db.connection.commit()
        self.db.close()
        cur.close()
        return hotel_list