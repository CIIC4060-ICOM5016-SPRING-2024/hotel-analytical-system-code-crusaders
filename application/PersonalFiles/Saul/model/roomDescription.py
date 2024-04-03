from model.db import Database

class roomDescriptionDAO:

    def __init__(self):
        self.db = Database()

    def getAllRoomDescription(self):
        cur = self.db.connection.cursor()
        query = """SELECT * FROM roomdescription;"""
        cur.execute(query)
        rd_list = cur.fetchall()
        self.db.close()
        cur.close()
        return rd_list

    def getRoomDescriptionsById(self, rdid):
        cur = self.db.connection.cursor()
        query = """SELECT * FROM roomdescription where rdid = %s;"""
        cur.execute(query, (rdid,))
        result = cur.fetchone()
        return result

    def insertRoomDescription(self, rname, rtype, capacity, ishandicap):
        cur = self.db.connection.cursor()
        query = "insert into roomdescription(rname, rtype, capacity, ishandicap) values (%s,%s,%s,%s) returning rdid;"
        cur.execute(query, (rname, rtype, capacity, ishandicap,))
        rdid = cur.fetchone()[0]
        self.db.connection.commit()
        cur.close()
        return rdid

    def updateRoomDescription(self, rdid, rname, rtype, capacity, ishandicap):
        cur = self.db.connection.cursor()
        query = "update roomdescription set rname =%s, rtype =%s, capacity =%s, ishandicap =%s where rdid =%s;"
        cur.execute(query, (rname, rtype, capacity, ishandicap, rdid))
        self.db.connection.commit()
        cur.close()
        return True

    def deleteRoomDescription(self, rdid):
        cur = self.db.connection.cursor()
        query = "delete from roomdescription where rdid =%s;"
        cur.execute(query, (rdid,))
        affected_rows = cur.rowcount
        self.db.connection.commit()
        return affected_rows != 0

