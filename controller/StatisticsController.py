from flask import jsonify
from model.StatisticsDAO import StatisticsDAO

class StatisticsController:

    def __init__(self):
        self.dao = StatisticsDAO()

    def handle_one_element(self, fullJson):
        if len(fullJson) == 1:
            return fullJson[0]
        else:
            return fullJson

    def make_json(self, table, columns):
        fullJson = [{columns[i]: row[i] for i in range(len(columns))} for row in table]

        return self.handle_one_element(fullJson)

    #
    #
    # LOCAL STATISTICS
    #
    #

    def get_Handicaproom(self, id):
        result = self.dao.get_Handicaproom(id)
        
        if result is not None:
            return self.make_json(result, ['rname', 'rtype', 'reservation_count'])
        return jsonify(f"There is no top 5 handicap rooms on hotel {id}:("), 404 
    
    def get_LeastReserve(self, id):
        result = self.dao.get_LeastReserve(id)
    
        if result is not None:
            return self.make_json(result, ['rid', 'datediff'])
        return jsonify(f"There is no top 3 rooms that were the least time unavailable at hotel {id}:("), 404 

    def get_MostCreditCard(self, id):
        result = self.dao.get_MostCreditCard(id)

        if result is not None:
            return self.make_json(result, ['full_name', 'count_reservation'])
        return jsonify(f"There is no top 5 clients under 30 that made the most reservation with a credit card at hotel {id}:("), 404 

    def get_HighestPaid(self, id):
        result = self.dao.get_HighestPaid(id)

        if result is not None:
            return self.make_json(result, ['eid', 'full_name', 'salary'])
        return jsonify(f"There is no top 3 highest paid regular employees at hotel {id}:("), 404 

    def get_MostDiscount(self, id):
        result = self.dao.get_MostDiscount(id)

        if result is not None:
            return self.make_json(result, ['full_name', 'discount'])
        return jsonify(f"There is no top 5 most discount on hotel {id} :("), 404

    def get_RoomType(self, id):
        result = self.dao.get_RoomType(id)

        if result is not None:
            return self.make_json(result, ['rtype', 'reservations_total'])
        return jsonify(f"There is no total reservation by room type at hotel {id} :("), 404

    def get_LeastGuests(self, id):
        result = self.dao.get_LeastGuests(id)

        if result is not None:
            return self.make_json(result, ['rid', 'ratio'])
        return jsonify(f"There is no top 3 rooms that were reserved that had the least guest-to-capacity ratio at hotel {id} :("), 404

    # 
    #
    # GLOBAL STATISTICS
    #
    #

    def get_MostRevenue(self):
        result = self.dao.get_MostRevenue()

        if result is not None:
            return self.make_json(result, ['chid', 'cname', 'total_revenue'])
        return jsonify(f"There is no top 3 chains with the highest total revenue. :("), 404
    
    def get_PaymentMethod(self):
        result = self.dao.get_PaymentMethod()

        if result is not None:
            return self.make_json(result, ['payment', 'percentage'])
        return jsonify(f"There is no total reservation percentage by payment method. :("), 404

    def get_LeastRooms(self):
        result = self.dao.get_LeastRooms()

        if result is not None:
            return self.make_json(result, ['cname', 'count_rooms'])
        return jsonify(f"There is no top 3 chain with the least rooms. :("), 404
    
    def get_MostCapacity(self):
        result = self.dao.get_MostCapacity()

        if result is not None:
            return self.make_json(result, ['hname', 'total_capacity'])
        return jsonify(f"There is no top 5 hotels with the most capacity. :("), 404
        
    def get_MostReservation(self):
        result = self.dao.get_MostReservation()

        if result is not None:
            return self.make_json(result, ['hname', 'reservations'])
        return jsonify(f"There is no top 10% hotels that had the most reservations. :("), 404
        
    def get_MostProfitMonth(self):
        result = self.dao.get_MostProfitMonth()
        if result is not None:
            return self.make_json(result, ['chid', 'name', 'month', 'total_reservations'])
        return jsonify(f"There is no top 3 month with the most reservation by chain. :("), 404
        
