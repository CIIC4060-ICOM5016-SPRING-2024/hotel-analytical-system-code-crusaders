from config.Database import Database

class ReserveDAO:

    def __init__(self):
        pass

    def getAllReserve(self):
        rd_list = Database().querySelectFrom(
            """
            SELECT * FROM reserve;
            """,
            ()
        )
        return rd_list

    def getReserveById(self, redid):
        result = Database().querySelectFrom(
            """
            SELECT * FROM reserve where reid = %s;
            """,
            (redid,)
        )
        return result

    def insertReserve(self, ruid, clid, total_cost, payment, guests):
        reid = Database().queryInsertFetch(
            """
            insert into reserve(ruid,clid,total_cost,payment,guests) values (%s,%s,%s,%s,%s) returning reid;
            """,
            (ruid, clid, total_cost, payment, guests,)
        )
        return reid

    def updateReserve(self, reid, ruid, clid, total_cost, payment, guests):
        result = Database().queryUpdate(
            """
            update reserve set ruid =%s, clid =%s, total_cost =%s, payment =%s, guests =%s where reid =%s;
            """,
            (ruid, clid, total_cost, payment, guests, reid)
        )
        return result

    def deleteReserve(self, reid):
        deleted = Database().queryDelete(
            """
            delete from reserve where reid =%s;
            """,
            (reid,)
        )
        return deleted

