from config.Database import Database

class LoginDAO:
    
    def __init__(self):
        
        pass

    def get_loginTable(self):
        self.db_connection = Database()
        
        result = self.db_connection.querySelectFrom(
            """
            select * from login limit 10;
            """
        )
        return result

