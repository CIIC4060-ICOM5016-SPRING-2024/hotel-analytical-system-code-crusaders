from config.db import Database
class ChainsDAO:
    def __init__(self):
        self.db = Database()
    def getAllChains(self):
        cur = self.db.connection.cursor()
        query = """SELECT * FROM chains"""
        cur.execute(query)
        chains_list = cur.fetchall()
        self.db.close()
        cur.close()
        return chains_list
    def getChainbyID(self,chid):
        cur = self.db.connection.cursor()
        query = """SELECT * FROM chains where chid = %s"""
        cur.execute(query, (chid,))
        chains_list = cur.fetchone()
        self.db.close()
        cur.close()
        return chains_list
    def createChain(self,cname,springmkup,summermkup,fallmkup,wintermkup):
        cur = self.db.connection.cursor()
        query1 = """INSERT INTO chains (cname,springmkup,summermkup,fallmkup,wintermkup) VALUES (%s,%s,%s,%s,%s) returning chid"""
        query2 = """SELECT * FROM chains where chid = %s"""
        cur.execute(query1,(cname,springmkup,summermkup,fallmkup,wintermkup))
        chain_id = cur.fetchone()[0]
        cur.execute(query2,(chain_id,))
        chains_list = cur.fetchone()
        self.db.connection.commit()
        self.db.close()
        cur.close()
        return chains_list
    def deleteChain(self,chid):
        cur = self.db.connection.cursor()
        query1 = """SELECT * FROM chains where chid = %s"""
        query2 = """DELETE FROM chains where chid = %s"""
        query3 = """SELECT setval('chains_chid_seq', max(chid)) FROM chains;"""
        cur.execute(query1,(chid,))
        chains_list = cur.fetchone()
        cur.execute(query2,(chid,))
        cur.execute(query3,(chid,))
        self.db.connection.commit()
        self.db.close()
        cur.close()
        return chains_list
    def updateChain(self,chid,cname,springmkup,summermkup,fallmkup,wintermkup):
        cur = self.db.connection.cursor()
        query1 = """UPDATE chains SET cname = %s, springmkup = %s, summermkup = %s, fallmkup = %s, wintermkup = %s WHERE chid = %s"""
        query2 = """SELECT chid,cname,springmkup,summermkup,fallmkup,wintermkup FROM chains where chid = %s"""
        cur.execute(query1,(cname,springmkup,summermkup,fallmkup,wintermkup,chid))
        cur.execute(query2,(chid,))
        chains_list = cur.fetchone()
        self.db.connection.commit()
        self.db.close()
        cur.close()
        return chains_list