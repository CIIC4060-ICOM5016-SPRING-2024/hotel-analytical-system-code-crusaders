from flask import jsonify
from model.global_stat import global_stat_dao


class global_stat():

    def getMostCapacity(self):
        dao = global_stat_dao()
        highestCapacity = dao.getMostCapacity()
        if not highestCapacity:
            return 'not found'
        else:
            result = []
            for element in highestCapacity:
                result.append({"hname": element[0], "total_capacity": element[1]})
            return jsonify(result)

    def getMostProfitMonth(self):
        dao = global_stat_dao()
        MostProfitMonth = dao.getMostProfitMonth()
        if not MostProfitMonth:
            return 'not found'
        else:
            result = []
            for element in MostProfitMonth:
                result.append({"chain_name": element[0],"year": element[1],"month": element[2],"total_reservations": element[3]})
            return jsonify(result)

