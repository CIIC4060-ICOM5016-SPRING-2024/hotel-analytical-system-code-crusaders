from model.db import Database


class reserveDAO:


    def __init__(self):
        self.db = Database()

    def getAllReserve(self):
        cur = self.db.connection.cursor()
        query = "SELECT * FROM reserve;"
        cur.execute(query)
        rd_list = cur.fetchall()
        self.db.close()
        cur.close()
        return rd_list

    def getReserveById(self, redid):
        cur = self.db.connection.cursor()
        query = "SELECT * FROM reserve where reid = %s;"
        cur.execute(query, (redid,))
        result = cur.fetchone()
        return result

    def insertReserve(self, ruid, clid, total_cost, payment, guests):
        cur = self.db.connection.cursor()
        query = "insert into reserve(ruid,clid,total_cost,payment,guests) values (%s,%s,%s,%s,%s) returning reid;"
        cur.execute(query, (ruid, clid, total_cost, payment, guests,))
        reid = cur.fetchone()[0]
        self.db.connection.commit()
        cur.close()
        return reid

    def updateReserve(self, reid, ruid, clid, total_cost, payment, guests):
        cur = self.db.connection.cursor()
        query = "update reserve set ruid =%s, clid =%s, total_cost =%s, payment =%s, guests =%s where reid =%s;"
        cur.execute(query, (ruid, clid, total_cost, payment, guests, reid))
        self.db.connection.commit()
        cur.close()
        return True

    def deleteReserve(self, reid):
        cur = self.db.connection.cursor()
        query = "delete from reserve where reid =%s;"
        cur.execute(query, (reid,))
        affected_rows = cur.rowcount
        self.db.connection.commit()
        return affected_rows != 0

