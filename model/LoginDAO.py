from config.Database import Database

class LoginDAO:
    
    def __init__(self):
        pass

    def get_all(self):
        result = Database().querySelectFrom(
            """
            select * from login;
            """,
            ()
        )
        return result
    
    def get_byID(self, id):
        result = Database().querySelectFrom(
            """
            select * from login where lid = %s;
            """,
            (id,)
        )
        return result

    def delete_byID(self, id):

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

    def update_byID(self, id, data):
        # Construct the SET clause
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        
        # Construct the parameter values
        params = tuple(data.values()) + (id,)

        result = Database().queryUpdate(
            f"""
            update login set {set_clause} where lid = %s;
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
            insert into login ({columns}) values ({placeholders});
            """,
            params
        )
        return result
    
    def login_user(self, username, password):
        result = Database().querySelectFrom(
            """
            select position, hid, chid
                from employee
                    natural inner join login
                    natural inner join hotel
                where
                    username = %s and
                    password = %s;
            """,
            (username, password,)
        )
        # if no matching user was found in database, return none
        # this will get handled by controller
        if not result:
            return None
        
        return result[0]
    
    def get_hotel_chain(self, hid):
        result = Database().querySelectFrom(
            """
            select chid from hotel where hid = %s;
            """,
            (hid,)
        )
        if not result:
            return -1
        
        return result[0][0]