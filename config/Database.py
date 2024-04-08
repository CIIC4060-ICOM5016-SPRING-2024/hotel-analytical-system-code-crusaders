import json
import psycopg2

class Database:
    connection_credentials = None

    # Load the credentials to static connection_url dictionary
    @staticmethod
    def load_credentials(SERVER):
        # Load JSON credentials from file
        with open('./application/config/credentials.json', 'r') as file:
            credentials = json.load(file)

        # Iterate through each server configuration in the JSON credentials
        for server_config in credentials:
            if server_config['server'] == SERVER:
                # Found a match, save the credentials as a dictionary and return
                Database.connection_credentials = {
                    'server':   server_config['server'],
                    'host':     server_config['host'],
                    'user':     server_config['user'],
                    'password': server_config['pass'],
                    'database': server_config['database'],
                    'port':     server_config['port']
                }
                return

        Database.connection_credentials = None
        print("No matching server for database credentials")


    # Create a new connection
    def __init__(self):
        if(Database.connection_credentials is None):
            print("Cannot create Database instance with no valid connection URL")
            return

        self.connection = psycopg2.connect(
            host     = Database.connection_credentials['host'],
            user     = Database.connection_credentials['user'],
            password = Database.connection_credentials['password'],
            port     = Database.connection_credentials['port'],
            database = Database.connection_credentials['database']
        )

    def querySelectFrom(self, query, params):
        if(Database.connection_credentials is None):
            return None
        
        try:
            # Create a cursor object
            cursor = self.connection.cursor()

            # Execute the query
            cursor.execute(query, params)

            # Fetch all rows from the result set
            result = cursor.fetchall()

            # Close the cursor
            cursor.close()
            self.connection.close()

            if len(result) == 0:
                return None
            else:
                return result
        except (Exception, psycopg2.Error) as error:
            print("Error executing query:", error)
            return None
        
    def queryUpdate(self, query, params):
        if(Database.connection_credentials is None):
            return False
        
        try:
            # Create a cursor object
            cursor = self.connection.cursor()

            # Execute the query
            cursor.execute(query, params)

            # Complete transaction
            self.connection.commit()

            # Close the cursor
            cursor.close()
            self.connection.close()

            return True
        except (Exception, psycopg2.Error) as error:
            print("Error executing query:", error)
            return False
        
    def queryInsert(self, query, params):
        if(Database.connection_credentials is None):
            return False
        
        try:
            # Create a cursor object
            cursor = self.connection.cursor()

            # Execute the query
            cursor.execute(query, params)

            # Commit the transaction to make the changes permanent
            self.connection.commit()

            # Close the cursor
            cursor.close()
            self.connection.close()

            return True
        except (Exception, psycopg2.Error) as error:
            print("Error executing query:", error)
            return False
        
    def queryInsertFetch(self, query, params):
        if(Database.connection_credentials is None):
            return None
        
        try:
            # Create a cursor object
            cursor = self.connection.cursor()

            # Execute the query
            cursor.execute(query, params)

            fetchedValue = cursor.fetchone()[0]

            # Commit the transaction to make the changes permanent
            self.connection.commit()

            # Close the cursor
            cursor.close()
            self.connection.close()

            return fetchedValue
        except (Exception, psycopg2.Error) as error:
            print("Error executing query:", error)
            return None
        
    def queryDelete(self, query, params):
        if(Database.connection_credentials is None):
            return False
        
        try:
            # Create a cursor object
            cursor = self.connection.cursor()

            # Execute the query
            cursor.execute(query, params)

            # Commit the transaction to make the changes permanent
            self.connection.commit()

            # Close the cursor
            cursor.close()
            self.connection.close()

            return True
        except (Exception, psycopg2.Error) as error:
            print("Error executing query:", error)
            return False
        
    def create_function(self, query):
        if(Database.connection_credentials is None):
                return False
        try:
            # Create a cursor object
            cursor = self.connection.cursor()

            # Execute the query
            cursor.execute(query)

            # Commit the transaction
            self.connection.commit()

            # Close the cursor
            cursor.close()

            print("Function created successfully")
        except (Exception, psycopg2.Error) as error:
            print("Error creating function:", error)