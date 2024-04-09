from config.Database import Database

class EmployeeDAO:

    def __init__(self):
        pass

    def getAllEmployees(self):
        employee_list = Database().querySelectFrom(
            """SELECT * FROM employee""",
            ()
        )
        return employee_list
    
    def getEmployeebyID(self,eid):
        employee_list = Database().querySelectFrom(
            """SELECT * FROM employee where eid = %s;""",
            (eid,)
        )
        return employee_list
    
    def createEmployee(self,hid,fname,lname,age,position,salary):
        eid = Database().queryInsertFetch(
            """INSERT INTO employee (hid,fname,lname,age,position,salary) VALUES (%s,%s,%s,%s,%s,%s) returning eid""",
            (hid,fname,lname,age,position,salary)
        )

        employee_list = Database().querySelectFrom(
            """SELECT * FROM employee where eid = %s""",
            (eid,)
        )
        return employee_list

    def deleteEmployee(self,eid):
        employee_list = Database().querySelectFrom(
            """SELECT * FROM employee where eid = %s""",
            (eid,)
        )

        result = Database().queryDelete(
            """DELETE FROM employee where eid = %s""",
            (eid,)
        )

        if not result:
            return []
        return employee_list
    
    def updateEmployee(self,eid,hid,fname,lname,age,position,salary):
        result = Database().queryUpdate(
            """UPDATE employee SET hid = %s, fname = %s, lname = %s, age = %s, position = %s, salary = %s WHERE eid = %s""",
            (hid,fname,lname,age,position,salary,eid)
        )

        if result is False:
            return []

        employee_list = Database().querySelectFrom(
            """SELECT eid,hid,fname,lname,age,position,salary FROM employee where eid = %s""",
            (eid)
        )
        return employee_list