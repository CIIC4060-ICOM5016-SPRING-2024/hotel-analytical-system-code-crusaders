from config.Database import Database

class ClientDAO:

    def __init__(self):
        pass
    
    def getAllClients(self):
        client_list = Database().querySelectFrom(
            """SELECT * FROM client;""",
            ()
        )
        return client_list

    def getClientById(self, clid):
        result = Database().querySelectFrom(
            """
            SELECT * FROM client where clid = %s;
            """,
            (clid,)
        )
        return result

    def insertClient(self, fname, lname, age, memberyear):
        clid = Database().queryInsertFetch(
            """
            insert into client(fname, lname, age, memberyear) values (%s,%s,%s,%s) returning clid;
            """,
            (fname, lname, age, memberyear,)
        )
        return clid

    def updateClient(self, clid, fname, lname, age, memberyear):
        updated = Database().queryUpdate(
            """
            update client set fname =%s, lname =%s, age =%s, memberyear =%s where clid =%s;
            """,
            (fname, lname, age, memberyear, clid,)
        )
        return updated

    def deleteClient(self, clid):
        deleted = Database().queryDelete(
            """
            delete from client where clid=%s;
            """,
            (clid,)
        )
        return deleted


