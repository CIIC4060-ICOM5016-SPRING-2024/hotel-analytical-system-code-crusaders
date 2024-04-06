from flask import jsonify
from model.StatisticsDAO import StatisticsDAO

class StatisticsController:

    def __init__(self):
        self.dao = StatisticsDAO()

    def make_handicap_json(self, table):
        fullJson = []

        for tuple in table:
            dictionary = {
                'rdid': tuple[0],
                'rname': tuple[1],
                'rtype': tuple[2],
                'reservation_count': tuple[3]
            }
            fullJson.append(dictionary)
        
        if len(fullJson) == 1:
            return fullJson[0]
        else:
            return fullJson
        
    def make_most_discount_json(self, table):
        fullJson = []
     
        for tuple in table:
            dictionary = {
                'clid': tuple[0],
                'full_name': tuple[1],
                'discount': tuple[2]
            }
            fullJson.append(dictionary)
        
        if len(fullJson) == 1:
            return fullJson[0]
        else:
            return fullJson
        
    def make_most_revenue_json(self, table):
        fullJson = []
        
        for tuple in table:
            dictionary = {
                'chid': tuple[0],
                'cname': tuple[1],
                'total_revenue': tuple[2]
            }
            fullJson.append(dictionary)
        
        if len(fullJson) == 1:
            return fullJson[0]
        else:
            return fullJson

    #
    #
    # LOCAL STATISTICS
    #
    #

    def get_Handicaproom(self, id):
        result = self.dao.get_Handicaproom(id)

        if result is not None:
            return self.make_handicap_json(result)
        return jsonify(f"There is no top 5 handicap rooms on hotel {id}:("), 404 
    
    def get_MostDiscount(self, id):
        result = self.dao.get_MostDiscount(id)

        if result is not None:
            return self.make_most_discount_json(result)
        return jsonify(f"There is no top 5 most discount on hotel {id} :("), 404
    
    # 
    #
    # GLOBAL STATISTICS
    #
    #

    def get_MostRevenue(self):
        result = self.dao.get_MostRevenue()

        if result is not None:
            return self.make_most_revenue_json(result)
        return jsonify(f"There is no most revenue :("), 404 
