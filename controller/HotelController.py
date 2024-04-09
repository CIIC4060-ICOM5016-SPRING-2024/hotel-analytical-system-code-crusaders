from flask import jsonify
from model.HotelDAO import HotelDAO

class HotelController:
    
    def make_json(self, tuples):
        result = []
        for tup in tuples:
            d = dict()
            d['hid'] = tup[0]
            d['chid'] = tup[1]
            d['hname'] = tup[2]
            d['hcity'] = tup[3]
            result.append(d)
        return result
    def make_json_one(self, tuples):
        result = []

        for tup in tuples:
            d = dict()
            d['hid'] = tup[0]
            d['chid'] = tup[1]
            d['hname'] = tup[2]
            d['hcity'] = tup[3]
            result.append(d)
    
        if len(result) == 1:
            return result[0]
        else:
            return result
    
    def getAllHotels(self):
        model = HotelDAO()
        result = model.getAllHotels()
        response = self.make_json(result)
        return response
    
    def getHotelbyID(self,hid):
        model = HotelDAO()
        hotel = model.getHotelbyID(hid)

        if not hotel:
            return jsonify("Not found"), 404
        else:
            response = self.make_json_one(hotel)
            return response
        
    def createHotel(self, json):
        chid = json['chid']
        hname = json['hname']
        hcity = json['hcity']
        model = HotelDAO()
        hotel = model.createHotel(chid,hname,hcity)
        if not hotel:
            return jsonify("Not found"), 404
        else:
            response = self.make_json_one(hotel)
            return response
        
    def deleteHotel(self, hid):
        model = HotelDAO()
        hotel = model.deleteHotel(hid)
        if not hotel:
            return jsonify("Not found"), 404
        else:
            response =  self.make_json_one(hotel)
            return response
        
    def updateHotel(self, json):
        hid = json['hid']
        chid = json['chid']
        hname = json['hname']
        hcity = json['hcity']
        model = HotelDAO()
        hotel = model.updateHotel(hid,chid,hname,hcity)
        if not hotel:
            return jsonify("Not found"), 404
        else:
            response = self.make_json_one(hotel)
            return response