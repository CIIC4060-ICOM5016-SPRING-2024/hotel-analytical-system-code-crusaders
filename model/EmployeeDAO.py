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
    
    def createEmployee(self, data):
        # Construct columns
        columns = ', '.join(data.keys())

        # Construct palceholders
        placeholders = ', '.join(['%s'] * len(data))

        # Construct the parameter values
        params = tuple(data.values())

        eid = Database().queryInsertFetch(
            f"""INSERT INTO employee ({columns}) values ({placeholders}) returning eid;""",
            params
        )
        return eid

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
            return None
        return employee_list
    
    def updateEmployee(self, id, data):
        # Construct the SET clause
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        
        # Construct the parameter values
        params = tuple(data.values()) + (id,)

        result = Database().queryUpdate(
            f"""UPDATE employee SET {set_clause} WHERE eid = %s""",
            params
        )
        return result