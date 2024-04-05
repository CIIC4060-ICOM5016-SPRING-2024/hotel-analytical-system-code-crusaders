from model.db import Database
class EmployeeDAO:
    def __init__(self):
        self.db = Database()
    def getAllEmployees(self):
        cur = self.db.connection.cursor()
        query = """SELECT * FROM employee"""
        cur.execute(query)
        employee_list = cur.fetchall()
        self.db.close()
        cur.close()
        return employee_list
    def getEmployeebyID(self,eid):
        cur = self.db.connection.cursor()
        query = """SELECT * FROM employee where eid = %s;"""
        cur.execute(query, (eid,))
        employee_list = cur.fetchone()
        self.db.close()
        cur.close()
        return employee_list
    def createEmployee(self,hid,fname,lname,age,position,salary):
        cur = self.db.connection.cursor()
        query1 = """INSERT INTO employee (hid,fname,lname,age,position,salary) VALUES (%s,%s,%s,%s,%s,%s) returning eid"""
        query2 = """SELECT * FROM employee where eid = %s"""
        cur.execute(query1,(hid,fname,lname,age,position,salary))
        employee_id = cur.fetchone()[0]
        cur.execute(query2,(employee_id,))
        employee_list = cur.fetchone()
        self.db.connection.commit()
        self.db.close()
        cur.close()
        return employee_list
    def deleteEmployee(self,eid):
        cur = self.db.connection.cursor()
        query1 = """SELECT * FROM employee where eid = %s"""
        query2 = """DELETE FROM employee where eid = %s"""
        cur.execute(query1,(eid,))
        employee_list = cur.fetchone()
        cur.execute(query2,(eid,))
        self.db.connection.commit()
        self.db.close()
        cur.close()
        return employee_list
    def updateEmployee(self,eid,hid,fname,lname,age,position,salary):
        cur = self.db.connection.cursor()
        query1 = """UPDATE employee SET hid = %s, fname = %s, lname = %s, age = %s, position = %s, salary = %s WHERE eid = %s"""
        query2 = """SELECT eid,hid,fname,lname,age,position,salary FROM employee where eid = %s"""
        cur.execute(query1,(hid,fname,lname,age,position,salary,eid))
        cur.execute(query2,(eid,))
        employee_list = cur.fetchone()
        self.db.connection.commit()
        self.db.close()
        cur.close()
        return employee_list