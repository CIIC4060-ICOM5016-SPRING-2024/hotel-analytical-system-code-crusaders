from flask import jsonify
from model.employee import EmployeeDAO
from model.hotels import HotelsDAO
from model.local_stat import local_stat_dao


######################################################
#           when to validate use this code           #
######################################################
#      if self.validateEmployee(hid, json):
#           [PUT YOUR STATISTIC CONTROLLER HERE]
#      else:
#           return jsonify("cannot access statistic")
######################################################


class local_stat:

    def SupervisorAccess(self, hid, employee_hid):  # checks that supervisor can see other hotel of the same chain
        # hotel chain of the employee
        hc_e_dao = HotelsDAO()
        hotel_hain_of_employee = hc_e_dao.getHotelbyID(employee_hid)
        chain_of_hotel_of_employee = hotel_hain_of_employee[1]
        # hotel chain
        hc_dao = HotelsDAO()
        hotel_chain = hc_dao.getHotelbyID(hid)
        chain_of_hotel = hotel_chain[1]
        if chain_of_hotel_of_employee == chain_of_hotel:
            return True
        else:
            return False

    def validateEmployee(self, hid, json):  # validate the employee by compareing its position and hotel working
        eid = json['eid']
        dao = EmployeeDAO()
        employee = dao.getEmployeebyID(eid)
        if not employee:
            return False
        else:
            employee_hid = employee[1]
            position = employee[5]
            if position == 'Regular':
                if employee_hid == hid:
                    return True
                else:
                    return False
            elif position == 'Supervisor':
                if self.SupervisorAccess(hid, employee_hid):
                    return True
                else:
                    return False
            elif position == 'Administrator':
                return True
            else:
                return False

    def getHighestPaid(self, hid, json):  # Get the top 3 Highest Paid Employee
        if self.validateEmployee(hid, json):
            dao = local_stat_dao()
            highest_paid = dao.getHighestPaid(hid)
            result = []
            for element in highest_paid:
                result.append({"fname": element[0], "lname": element[1], "position": element[2], "salary": element[3]})
            return jsonify(result)
        else:
            return jsonify("cannot access statistic")