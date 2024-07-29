from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import psycopg2

from takefreeSlotWeb import cleanResult, check_space_for_cabinet



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
        cursor.execute("SELECT D.idDevice, D.serialNumber, D.sizeDevice, D.producerdevice, D.yearProduction, D.statusDevice, D.usedSlot, DT.deviceType, D.idCabinet, L.timelog, L.iddevicereplaced, L.idaction FROM Device AS D JOIN DeviceType AS DT ON D.idDeviceType=DT.idDeviceType JOIN Log As L on L.idDevice=D.idDevice WHERE D.idCabinet IN (SELECT idCabinet FROM Cabinet AS C JOIN POP AS P ON p.idPOP=C.idPOP WHERE P.popPosition = %s) and L.timelog = (SELECT MAX(l2.timelog) FROM Log as l2 WHERE l2.idDevice = D.idDevice)", [position])

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
            "devicereplaced": device[10],
            "idaction": device[11]
            } for device in d]

        if len(d) == 0:
            diz = 0
        response.append(diz)
        
        

        cursor.close()
        
        return make_response(jsonify(response), 200)
        
                

class Cabinet(Resource):

    def get(self, pos):

        keys, freeSpace, resp, active, inactive, removed, updates = getData(pos)

        response = {}
        for key in keys:
            
            


            info_for_cabinet = {
                "Spazio totale restante: ": next((space[1] for space in freeSpace if space[0] == key), '-'), #se non vale la condizione gli affido None, sennò non andrebbe avanti
                "Spazio massimo contiguo restante: ": resp.get(key, 0),
                "Totali Rimossi: ": next((rem[1] for rem in removed if rem[0] == key), '-'),
                "Totali Attivi: ": next((att[1] for att in active if att[0] == key), '-'),
                "Totali Inattivi: ": next((inatt[1] for inatt in inactive if inatt[0] == key), '-'),
                "Ultimo Aggiornamento: ": next((str(upd[1]) + " - ID Device: " + str(upd[2]) for upd in updates if upd[0] == key), '-')
            }

            if key not in response.keys():
                response[key] = info_for_cabinet



        return make_response(response, 200)
            


class Notification(Resource):

    def get(self, position):
        
        socketio.emit('update_data', {'position': position}) #alla get, emissione sulla porta, sui cui sarà in ascolto la webApp



def getData(pos):


    #PER LA MASSIMA SIMENSIONE DISPONIBILE
        #seleziono i dispositivi restanti
        cursor = conn.cursor()
        cursor.execute("SELECT C.idCabinet, C.numofslot - L.slotoccupati AS freeSpace FROM Cabinet as C  JOIN Log as L on L.idCabinet=C.idCabinet JOIN POP AS P on P.idPOP=C.idPOP JOIN Device D ON C.idCabinet=D.idCabinet WHERE L.idlog IN (SELECT MAX (l2.idlog) FROM Log as l2 WHERE C.idCabinet = l2.idCabinet) and P.popposition = %s GROUP BY C.idCabinet, C.numofslot - L.slotoccupati", [pos])
        
        freeSpace = cursor.fetchall()

        print(freeSpace)

        keys = []

        for elem in freeSpace:
            keys.append(elem[0])

        keys.sort()
        print(keys)


        #PER LA MASSIMA DIMENSIONE CONTIGUA DISPONIBILE

        cursor.execute('SELECT idCabinet, numOfSlot from Cabinet AS C join Pop As P on C.idPOP = P.idPOP WHERE P.popPosition = %s', [pos])

        max_dimensions = cursor.fetchall()

        dictionary_max_dimensions = {elem[0] : elem[1] for elem in max_dimensions}

        print(dictionary_max_dimensions)

        cursor.execute('SELECT C.idCabinet, COALESCE(D.usedSlot, CAST(0 AS VARCHAR(15))) FROM Device AS D JOIN Cabinet AS C ON D.idCabinet= C.idCabinet JOIN POP AS P ON p.idPOP = C.idPOP WHERE P.popPosition = %s AND D.usedSlot != %s GROUP BY C.idCabinet, D.usedSlot ORDER BY usedSlot', [pos, '-'])

        result = cursor.fetchall()


        listEffective, all_free = cleanResult(result, 0, dictionary_max_dimensions) #pulisco il risultato


        listEffective = sorted(listEffective, key=sorting_key)

        print("List_effective:")
        print(listEffective)
        print("All_free:")
        print(all_free)


        resp = check_space_for_cabinet(listEffective, dictionary_max_dimensions) #dizionario che contiene i massimi spazi contigui restati

        #Per i totali ATTIVI 
        cursor.execute("SELECT D.idCabinet, COUNT(D.idDevice) from Device as D JOIN Cabinet as C on C.idCabinet = D.idCabinet Join POP AS P on C.idPOP = P.idPOP WHERE D.statusdevice = 'Active' and P.popPosition=%s GROUP BY D.idCabinet", [pos]) 

        active= cursor.fetchall()

        #Per i totali INATTIVI

        cursor.execute("SELECT D.idCabinet, COUNT(D.idDevice) from Device as D JOIN Cabinet as C on C.idCabinet = D.idCabinet Join POP AS P on C.idPOP = P.idPOP WHERE D.statusdevice = 'Inactive' and P.popPosition=%s GROUP BY D.idCabinet", [pos]) 

        inactive = cursor.fetchall()

        #Per i totali RIMOSSI
        cursor.execute("SELECT D.idCabinet, COUNT(D.idDevice) from Device as D JOIN Cabinet as C on C.idCabinet = D.idCabinet Join POP AS P on C.idPOP = P.idPOP WHERE D.statusdevice = 'Removed' and P.popPosition=%s GROUP BY D.idCabinet", [pos]) 

        removed= cursor.fetchall()

        #Per l'ultimo aggiornamento

        cursor.execute("SELECT DISTINCT C.idCabinet, L.timelog, L.idDevice from Log as l JOIN Cabinet as C on C.idCabinet = L.idCabinet Join POP as P on C.idPOP=P.idPOP WHERE p.popPosition = %s AND L.timelog = (SELECT MAX(l2.timelog) FROM Log l2 WHERE l2.idCabinet = C.idCabinet ) ORDER BY C.idCabinet", [pos])

        updates = cursor.fetchall()

       

        if len(resp) == 0 and len(all_free)!=0:
            resp = all_free
        elif len(resp) != 0 and len(all_free) != 0:
            resp = {**resp, **all_free}

        return keys, freeSpace, resp, active, inactive, removed, updates


#funzione di utilità sorting key
def sorting_key(item):
    
    string = item[0]
    prefix, first_num, second_num = string.split()[0], int(string.split()[2]), int(string.split()[4])
    return (prefix, first_num, second_num)


api.add_resource(POP, "/luoghi")
api.add_resource(Device, "/device/<string:position>")
api.add_resource(Notification, "/notify/<string:position>")
api.add_resource(Cabinet, "/cabinet/<string:pos>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
