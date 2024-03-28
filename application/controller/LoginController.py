
from model.LoginDAO import LoginDAO

class LoginController:

    def make_json(self, table):
        # Turn the data to json
        fullJson = []

        for tuple in table:
            dictionary = {
                "lid": tuple[0],
                "eid": tuple[1],
                "username": tuple[2],
                "password": tuple[3],
            }
            fullJson.append(dictionary)
        return fullJson

    def getAllUsers(self):
        # Build new DAO

        dao = LoginDAO()

        result = dao.getAllUsers()

        answer = self.make_json(result)

        return answer
