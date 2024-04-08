import psycopg2

class Database: 

    def __init__(self):
        self.connection = psycopg2.connect( 
            host = [http://ec2-52-20-188-247.compute-1.amazonaws.com/]
            user = [ddhibzzhtoskvy]
            password = [ldbfb32a8f464916c0282f585956963b79d5e094fcdab1015a0224bf7579ec10]
            port = [5432]
            database = [d9jhl82rojghvo]
            )

    def close(self):
        self.connection.close() 