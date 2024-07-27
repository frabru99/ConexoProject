from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import psycopg2





"""------------------------ CONNESSIONE AL DATABASE--------------------------------------- """
conn = psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="ciao",
                        port="5432")


""" ---------------------------------------------------------------------"""



"""  ------ CREAZIONE APP FLASK -----   """ 
app = Flask("ConexoWeb") #creiamo l'app Flask
api = Api(app) #la rendiamo ogetto restful
# Dopo la creazione dell'app
# Abilita CORS per tutte le richieste
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app, resources={r"/*": {"origins": "*"}})

class POP(Resource):

    def get(self):

        cursor = conn.cursor()
        cursor.execute("SELECT popPosition from POP")

        data = cursor.fetchall()

        print(data)
        
        data.sort()

        response = [{"title": pos[0], "caption": "POP di " + str(pos[0]), "icon": 'public'} for pos in data]
        
        
        cursor.close()
        return make_response(jsonify(response), 200)


class Device(Resource):

    def get(self, position):

        cursor = conn.cursor()
        print(position)
        cursor.execute("SELECT D.idDevice, D.serialNumber, D.sizeDevice, D.producerdevice, D.yearProduction, D.statusDevice, D.usedSlot, DT.deviceType, D.idCabinet, L.timelog, L.iddevicereplaced FROM Device AS D JOIN DeviceType AS DT ON D.idDeviceType=DT.idDeviceType JOIN Log As L on L.idDevice=D.idDevice WHERE D.idCabinet IN (SELECT idCabinet FROM Cabinet AS C JOIN POP AS P ON p.idPOP=C.idPOP WHERE P.popPosition = %s) and L.timelog = (SELECT MAX(l2.timelog) FROM Log as l2 WHERE l2.idDevice = D.idDevice)", [position])

        d = cursor.fetchall()

        print(d)

        response = []
        for device in d:
            diz = [{"iddevice": device[0], 
            "serialnumber": device[1], 
            "devicesize": device[2], 
            "producer": device[3], 
            "yearofproduction": device[4], 
            "status": device[5],
            "usedslot": device[6],
            "devicetype": device[7],
            "idcabinet": device[8],
            "timelog": device[9],
            "devicereplaced": device[10]
            } for device in d]

        if len(d) == 0:
            diz = 0
        response.append(diz)
        
        

        cursor.close()
        
        return make_response(jsonify(response), 200)


class Notification(Resource):

    def get(self, position):
        
        socketio.emit('update_data', {'position': position}) #alla get, emissione sulla porta, sui cui sarà in ascolto la webApp





api.add_resource(POP, "/luoghi")
api.add_resource(Device, "/device/<string:position>")
api.add_resource(Notification, "/notify/<string:position>")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
