import json
import psycopg2

class Database:
    connection_credentials = None

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

    def querySelectFrom(self, query):
        if(Database.connection_credentials is None):
            return []
        
        result = []

        # Create a new cursor from connection
        cursor = self.connection.cursor()
        # Run the query
        cursor.execute(query)

        # Append the data to a list
        for row in cursor:
            result.append(row)

        # End the connection
        self.connection.close()
        cursor.close()

        return result

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
