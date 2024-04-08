from config.db import Database

class ClientDAO:

    def __init__(self):
        self.db = Database()

    def getAllClients(self):
        cur = self.db.connection.cursor()
        query = """SELECT * FROM client;"""
        cur.execute(query)
        client_list = cur.fetchall()
        self.db.close()
        cur.close()
        return client_list

    def getClientById(self, clid):
        cur = self.db.connection.cursor()
        query = """SELECT * FROM client where clid = %s;"""
        cur.execute(query, (clid,))
        result = cur.fetchone()
        cur.close()
        return result

    def insertClient(self, fname, lname, age, memberyear):
        cur = self.db.connection.cursor()
        query = "insert into client(fname, lname, age, memberyear) values (%s,%s,%s,%s) returning clid;"
        cur.execute(query, (fname, lname, age, memberyear,))
        clid = cur.fetchone()[0]
        self.db.connection.commit()
        cur.close()
        return clid

    def updateClient(self, clid, fname, lname, age, memberyear):
        cur = self.db.connection.cursor()
        query = "update client set fname =%s, lname =%s, age =%s, memberyear =%s where clid =%s"
        cur.execute(query, (fname, lname, age, memberyear, clid))
        self.db.connection.commit()
        cur.close()
        return True

    def deleteClient(self, clid):
        cur = self.db.connection.cursor()
        query = "delete from client where clid=%s;"
        cur.execute(query, (clid,))
        affected_rows = cur.rowcount
        self.db.connection.commit()
        return affected_rows != 0


