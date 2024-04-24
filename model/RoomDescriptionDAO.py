from config.Database import Database

class RoomDescriptionDAO:
    
    def __init__(self):
        pass

    def get_all(self):
        result = Database().querySelectFrom(
            """
            select * from roomdescription;
            """,
            ()
        )
        return result
    
    def get_byID(self, id):
        result = Database().querySelectFrom(
            """
            select distinct * from roomdescription where rdid = %s limit 1;
            """,
            (id,)
        )
        return result

    def delete_byID(self, id):

        # Obtain the record before deleting
        result = Database().querySelectFrom(
            f"""
            select distinct * from roomdescription where rdid = %s limit 1;
            """,
            (id,)
        )

        # Delete record
        deletionResult = Database().queryDelete(
            f"""
            delete from roomdescription where rdid = %s;
            """,
            (id,)
        )

        if not deletionResult:
            return None
        
        return result

    def update_byID(self, id, data):
        # Construct the SET clause
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        
        # Construct the parameter values
        params = tuple(data.values()) + (id,)

        result = Database().queryUpdate(
            f"""
            update roomdescription set {set_clause} where rdid = %s;
            """,
            params
        )
        return result
    
    def create_record(self, data):
        # Construct columns
        columns = ', '.join(data.keys())

        # Construct palceholders
        placeholders = ', '.join(['%s'] * len(data))

        # Construct the parameter values
        params = tuple(data.values())

        result = Database().queryInsert(
            f"""
            insert into roomdescription ({columns}) values ({placeholders}) returning rdid;
            """,
            params
        )
        return result