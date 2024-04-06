from model.db import Database

class local_stat_dao:

    def __init__(self):
        self.db = Database()

    def getHighestPaid(self, hid):
        cur = self.db.connection.cursor()
        query = """select fname, lname, position, salary 
                    from employee 
                    where position = 'Regular' and hid=%s 
                    order by salary desc 
                    limit 3;"""
        cur.execute(query, (hid,))
        result = cur.fetchall()
        cur.close()
        return result

