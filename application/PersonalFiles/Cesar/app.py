from flask import Flask
from flask_cors import CORS
from controller.hotels import Hotels
from controller.chains import Chains
from controller.employee import Employee

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return "Hello"
#############################################
#                HOTEL
#############################################


@app.route('/codecrusaders/hotel', methods=['GET'])
def handleHotels():
    handler = Hotels()
    return handler.getAllHotels()
@app.route('/codecrusaders/hotel/<int:hid>', methods=['GET'])
def handleHotelsbyID(hid):
    handler = Hotels()
    return handler.getHotelbyID(hid)
@app.route('/codecrusaders/hotel/<int:hid>/<int:chid>/<string:hname>/<string:hcity>', methods=['POST'])
def handleHotelCreation(hid, chid, hname, hcity):
    handler = Hotels()
    return handler.createHotel(hid,chid,hname,hcity)
@app.route('/codecrusaders/hotel/<int:hid>', methods=['DELETE'])
def handleHotelDelete(hid):
    handler = Hotels()
    return handler.deleteHotel(hid)
@app.route('/codecrusaders/hotel/<int:hid>/<int:chid>/<string:hname>/<string:hcity>', methods=['PUT'])
def handleupdateHotel(hid, chid, hname, hcity):
    handler = Hotels()
    return handler.updateHotel(hid,chid,hname,hcity)

#############################################
#                CHAINS
#############################################


@app.route('/codecrusaders/chains', methods=['GET'])
def handleChains():
    handler = Chains()
    return handler.getAllChains()
@app.route('/codecrusaders/chains/<int:chid>', methods=['GET'])
def handleChainsbyID(chid):
    handler = Chains()
    return handler.getChainbyID(chid)
@app.route('/codecrusaders/chains/<int:chid>/<string:cname>/<float:springmkup>/<float:summermkup>/<float:fallmkup>/<float:wintermkup>', methods =['POST'])
def handleChainsCreation(chid, cname, springmkup,summermkup,fallmkup,wintermkup):
    handler = Chains()
    return handler.createChain(chid,cname,springmkup,summermkup,fallmkup,wintermkup)
@app.route('/codecrusaders/chains/<int:chid>', methods=['DELETE'])
def handleChainsDelete(chid):
    handler = Chains()
    return handler.deleteChain(chid)
@app.route('/codecrusaders/chains/<int:chid>/<string:cname>/<float:springmkup>/<float:summermkup>/<float:fallmkup>/<float:wintermkup>', methods =['PUT'])
def handleupdateChains(chid, cname, springmkup,summermkup,fallmkup,wintermkup):
    handler = Chains()
    return handler.updateChain(chid,cname,springmkup,summermkup,fallmkup,wintermkup)


#############################################
#                EMPLOYEE
#############################################


@app.route('/codecrusaders/employee', methods=['GET'])
def handleEmployee():
    handler = Employee()
    return handler.getAllEmployees()
@app.route('/codecrusaders/employee/<int:eid>', methods=['GET'])
def handleEmployeesbyID(eid):
    handler = Employee()
    return handler.getEmployeebyID(eid)
@app.route('/codecrusaders/employee/<int:eid>/<int:hid>/<string:fname>/<string:lname>/<int:age>/<string:position>/<float:salary>', methods = ['POST'])
def handleEmployeeCreation(eid,hid,fname,lname,age,position,salary):
    handler = Employee()
    return handler.createEmployee(eid,hid,fname,lname,age,position,salary)
@app.route('/codecrusaders/employee/<int:eid>', methods=['DELETE'])
def handleEmployeeDelete(eid):
    handler = Employee()
    return handler.deleteEmployee(eid)
@app.route('/codecrusaders/employee/<int:eid>/<int:hid>/<string:fname>/<string:lname>/<int:age>/<string:position>/<float:salary>', methods = ['PUT'])
def handleUpdateEmployee(eid,hid,fname,lname,age,position,salary):
    handler = Employee()
    return handler.updateEmployee(eid,hid,fname,lname,age,position,salary)
if __name__ == '__main__':
    app.run(debug=True)