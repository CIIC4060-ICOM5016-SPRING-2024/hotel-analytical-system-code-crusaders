from config.db import Database
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
    def createHotel(self,chid,hname,hcity):
        cur = self.db.connection.cursor()
        query1 = """INSERT INTO hotel (chid,hname,hcity) VALUES (%s,%s,%s) returning hid"""
        query2 = """SELECT * FROM hotel where hid = %s"""
        cur.execute(query1,(chid,hname,hcity))
        hotel_id = cur.fetchone()[0]
        cur.execute(query2,(hotel_id,))
        hotel_list = cur.fetchone()
        self.db.connection.commit()
        self.db.close()
        cur.close()
        return hotel_list
    def deleteHotel(self,hid):
        cur = self.db.connection.cursor()
        query1 = """SELECT * FROM hotel where hid = %s"""
        query2 = """DELETE FROM hotel where hid = %s"""
        query3 = """SELECT setval('hotel_hid_seq', max(hid)) FROM hotel;"""
        cur.execute(query1,(hid,))
        hotel_list = cur.fetchone()
        cur.execute(query2,(hid,))
        cur.execute(query3,(hid,))
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