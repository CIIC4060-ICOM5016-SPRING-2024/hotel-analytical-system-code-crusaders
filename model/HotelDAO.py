from config.Database import Database

class HotelDAO:

    def __init__(self):
        pass

    def getAllHotels(self):
        hotel_list = Database().querySelectFrom(
            """SELECT * FROM hotel""",
            ()
        )
        return hotel_list
    
    def getHotelbyID(self,hid):
        hotel_list = Database().querySelectFrom(
            """SELECT * FROM hotel where hid = %s""",
            (hid,)
        )
        return hotel_list
    
    def createHotel(self,chid,hname,hcity):
        hid = Database().queryInsertFetch(
            """INSERT INTO hotel (chid,hname,hcity) VALUES (%s,%s,%s) returning hid""",
            (chid,hname,hcity)
        )

        hotel_list = Database().querySelectFrom(
            """SELECT * FROM hotel where hid = %s""",
            (hid,)
        )
        return hotel_list
    
    def deleteHotel(self,hid):
        hotel_list = Database().querySelectFrom(
            """SELECT * FROM hotel where hid = %s""",
            (hid,)
        )

        result = Database().queryDelete(
            """DELETE FROM hotel where hid = %s""",
            (hid,)
        )

        if result is False:
            return []
        
        return hotel_list
    
    def updateHotel(self,hid,chid,hname,hcity):
        result = Database().queryUpdate(
            """UPDATE hotel SET chid = %s, hname = %s, hcity = %s WHERE hid = %s""",
            (chid,hname,hcity,hid)
        )

        if result is False:
            return []

        hotel_list = Database().querySelectFrom(
            """SELECT hid,chid,hname,hcity FROM hotel where hid = %s""",
            (hid)
        )
        return hotel_list