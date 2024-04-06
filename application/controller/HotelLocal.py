from flask import jsonify

class HotelLocal:

    login_columns = ['hid', 'chid', 'hname', 'hcity']

    def __init__(self):
        pass

    def make_json(self, table):
        # Turn the data to json
        fullJson = []

        for tuple in table:
            dictionary = {
                self.login_columns[0]: tuple[0],
                self.login_columns[1]: tuple[1],
                self.login_columns[2]: tuple[2],
                self.login_columns[3]: tuple[3],
            }
            fullJson.append(dictionary)
        
        if len(fullJson) == 1:
            return fullJson[0]
        else:
            return fullJson

    def getLeastReserve(self, id):
        return jsonify("least reserve got")
