from config.Database import Database

class ChainsDAO:

    def __init__(self):
        pass

    def get_all(self):
        chains_list = Database().querySelectFrom(
            """
            SELECT * FROM chains
            """,
            ()
        )
        return chains_list
    
    def get_byID(self,chid):
        chains_list = Database().querySelectFrom(
            """
            SELECT * FROM chains where chid = %s
            """,
            (chid,)
        )
        return chains_list
    
    def createChain(self, data):

        # Construct columns
        columns = ', '.join(data.keys())

        # Construct palceholders
        placeholders = ', '.join(['%s'] * len(data))

        # Construct the parameter values
        params = tuple(data.values())

        chid = Database().queryInsertFetch(
            f"""
            INSERT INTO chains ({columns}) VALUES ({placeholders}) returning chid
            """,
            params
        )

        return chid
    
    def delete_byID(self, chid):
        chains_list = Database().querySelectFrom(
            """
            SELECT * FROM chains where chid = %s
            """,
            (chid,)
        )

        result = Database().queryDelete(
            """
            DELETE FROM chains where chid = %s
            """,
            (chid,)
        )

        if not result:
            return None

        return chains_list
    
    def update_byID(self, id, data):

        # Construct the SET clause
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        
        # Construct the parameter values
        params = tuple(data.values()) + (id,)

        result = Database().queryUpdate(
            f"""
            update chains set {set_clause} where chid = %s;
            """,
            params
        )
        return result