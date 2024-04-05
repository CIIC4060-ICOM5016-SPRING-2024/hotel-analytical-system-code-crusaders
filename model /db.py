import psycopg2

class Database: 

    def __init__(self):
        self.connection = psycopg2.connect( 
            host = [ec2-174-129-100-198.compute-1.amazonaws.com]
            user = [kzdcvixdiicyfu]
            password = [be9bd083a8b90b0c94d2aa3581c5a46f5ee631ba6c871060bd3d9c2f3facd780]
            port = [5432]
            database = [dd6ro3tka19ama]
            )

    def close(self):
        self.connection.close() 