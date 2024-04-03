from config.Database import Database

class LoginDAO:
    
    def __init__(self):
        pass

    def get_loginTable(self):
        self.db_connection = Database()
        
        result = self.db_connection.querySelectFrom(
            """
            select * from login;
            """,
            ()
        )
        return result
    
    def get_loginByID(self, lid):
        self.db_connection = Database()
        
        result = self.db_connection.querySelectFrom(
            """
            select * from login where lid = %s;
            """,
            (lid,)
        )
        return result

    def delete_loginByID(self, id):

        # Obtain the record before deleting
        result = Database().querySelectFrom(
            f"""
            select distinct * from login where lid = %s limit 1;
            """,
            (id,)
        )

        # Delete record
        deletionResult = Database().queryDelete(
            f"""
            delete from login where lid = %s;
            """,
            (id,)
        )

        if not deletionResult:
            return None
        
        return result

    def update_loginByID(self, lid, data):
        self.db_connection = Database()
        
        # Construct the SET clause
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        
        # Construct the parameter values
        params = tuple(data.values()) + (lid,)

        result = self.db_connection.queryUpdate(
            f"""
            update login set {set_clause} where lid = %s;
            """,
            params
        )
        return result
    
    def create_loginRecord(self, data):
        self.db_connection = Database()
        
        # Construct columns
        columns = ', '.join(data.keys())

        # Construct palceholders
        placeholders = ', '.join(['%s'] * len(data))

        # Construct the parameter values
        params = tuple(data.values())

        result = self.db_connection.queryInsert(
            f"""
            insert into login ({columns}) values ({placeholders});
            """,
            params
        )
        return result