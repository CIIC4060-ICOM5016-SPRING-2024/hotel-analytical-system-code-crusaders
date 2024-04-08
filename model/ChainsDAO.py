from config.Database import Database

class ChainsDAO:

    def __init__(self):
        pass

    def getAllChains(self):
        chains_list = Database().querySelectFrom(
            """
            SELECT * FROM chains
            """,
            ()
        )
        return chains_list
    
    def getChainbyID(self,chid):
        chains_list = Database().querySelectFrom(
            """
            SELECT * FROM chains where chid = %s
            """,
            (chid,)
        )
        return chains_list
    
    def createChain(self,cname,springmkup,summermkup,fallmkup,wintermkup):
        chid = Database().queryInsertFetch(
            """
            INSERT INTO chains (cname,springmkup,summermkup,fallmkup,wintermkup) VALUES (%s,%s,%s,%s,%s) returning chid
            """,
            (cname, springmkup, summermkup, fallmkup, wintermkup, )
        )

        chains_list = Database().querySelectFrom(
            """
            SELECT * FROM chains where chid = %s
            """,
            (chid,)
        )
        return chains_list
    
    def deleteChain(self,chid):
        chains_list = Database().querySelectFrom(
            """
            SELECT * FROM chains where chid = %s
            """,
            (chid,)
        )

        result = Database().queryDelete(
            """
            DELETE FROM chains where chid = %s
            """,
            (chid,)
        )

        if result is False:
            return []

        return chains_list
    def updateChain(self,chid,cname,springmkup,summermkup,fallmkup,wintermkup):
        result = Database().queryUpdate(
            """
            UPDATE chains SET cname = %s, springmkup = %s, summermkup = %s, fallmkup = %s, wintermkup = %s WHERE chid = %s
            """,
            (cname,springmkup,summermkup,fallmkup,wintermkup,chid,)
        )

        if result is False:
            return []

        chains_list = Database().querySelectFrom(
            """
            SELECT chid,cname,springmkup,summermkup,fallmkup,wintermkup FROM chains where chid = %s
            """,
            (chid,)
        )

        return chains_list