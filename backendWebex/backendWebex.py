from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
import psycopg2
from datetime import date, datetime
from threading import Thread, Lock
import time
import requests


from takefreeSlot import check_space_for_device, cleanResult, check_space_for_cabinet


"""------------------------ CONNESSIONE AL DATABASE--------------------------------------- """
conn = psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="ciao",
                        port="5432")


cursor = conn.cursor() #accesso al database.
""" ---------------------------------------------------------------------"""



"""  ------ CREAZIONE APP FLASK -----   """ 
app = Flask("Conexo") #creiamo l'app Flask
api = Api(app) #la rendiamo ogetto restful




"""   ----- VARIABILI  GLOBALI ---- 
- matricola e email: utili per mantenere lo stato dell'autenticazione.
- mutex: per gestire la mutua escluzione all'accesso delle variabili matricola e email, conteso tra metodo e Thread.
""" 

matricola = None 
email = None

mutex = Lock() 




""" ----- CLASSE CABINET REST ---- 

Utilizza le variabili globali cursor, email e matricola. 

METODI IMPLEMENTATI: GET 

GET: La get può avere due valenze. Di seuito sono riportate le valenze e le funzionalità:
- /cabinet/<int:selector>/<string:position>: viene inviato un selettore e la posizione attuale (sede)

    - Se il selettore è 0, allora mi restituisce tutti i cabinet della posizione inviata.
    - Se il selettore è 1, allora mi permette di prendere lo spazio libero contiguo massimo tra i cabinet di una sede.

-/cabinet/<int:selector>/<string:position>: Mi permette di prender quei cabinet che hanno una posizione massima contigua maggiore o uguale di quella inviata.

"""
class Cabinet(Resource):

    global cursor
    global email
    global matricola

    

    def get(self, position=None, dimension=None, selector=None):

        if email==None or matricola==None:

            response = "Session expired."
            return make_response(response, 419)

        #prendo i cabinet con una certa posizione e una certa dimensione residua massima 

        if dimension == None and selector == 0 : #volgio solo i cabinet della posizione

            try: 
                cursor.execute('SELECT * FROM CABINET WHERE idPOP = ( SELECT idPOP FROM POP WHERE popPosition = %s)', [position])

                allCabinets = cursor.fetchall()

                if len(allCabinets) != 0:
                    
                    
                    response = jsonify(allCabinets)
                    return make_response(response, 200)

                else:
                    response = "No cabinets found for the given position"
                    return make_response(response, 404)


            except (Exception, psycopg2.DatabaseError, TypeError) as error:
                print(error)
                response = "An error is occured"
                return make_response(response, 500)


        elif position != None and dimension != None and selector == None: #voglio i cabinet di quella posizione che abbiano una dimensione residua maggiore di quella inviata


            try:

                #cursor.execute('SELECT c.idCabinet, COALESCE(l.slotOccupati, 0) AS slotOccupati, c.numOfSlot - COALESCE(l.slotOccupati, 0) AS slotLiberi FROM cabinet c LEFT JOIN (SELECT idCabinet, slotOccupati,ROW_NUMBER() OVER(PARTITION BY idCabinet ORDER BY timeLog DESC) AS rn FROM log WHERE timeLog = (SELECT MAX(timeLog) FROM log l2 WHERE l2.idCabinet = log.idCabinet)) l ON c.idCabinet = l.idCabinet AND l.rn = 1 INNER JOIN PoP p ON c.idPOP = p.idPOP WHERE p.popPosition = %s GROUP BY c.idCabinet, c.numOfSlot, l.slotOccupati HAVING (c.numOfSlot - COALESCE(l.slotOccupati, 0)) >= %s', [position, str(dimension)])
                
                cursor.execute('SELECT idCabinet, numOfSlot from Cabinet AS C join Pop As P on C.idPOP = P.idPOP WHERE P.popPosition = %s', [position])

                max_dimensions = cursor.fetchall()

                dictionary_max_dimensions = {elem[0] : elem[1] for elem in max_dimensions}

                cursor.execute('SELECT C.idCabinet, COALESCE(D.usedSlot, CAST(0 AS VARCHAR(15))) FROM Device AS D JOIN Cabinet AS C ON D.idCabinet= C.idCabinet JOIN POP AS P ON p.idPOP = C.idPOP WHERE P.popPosition = %s AND D.usedSlot != %s GROUP BY C.idCabinet, D.usedSlot ORDER BY usedSlot', [position, '-'])

                result = cursor.fetchall()


                listEffective, all_free = cleanResult(result, dimension, dictionary_max_dimensions) #pulisco il risultato


                listEffective = sorted(listEffective, key=sorting_key)
                print(listEffective)
                print(all_free)

                resp = check_space_for_device(dimension, listEffective, dictionary_max_dimensions) #preparo la risposta

                resp.append(all_free)

                print(resp)

                if len(resp) != 0:
                    
                    return make_response(resp, 200)

                else:
                    response = "No cabinets found for the given position and dimension."
                    return make_response(response, 404)

            except (Exception, psycopg2.DatabaseError, TypeError) as error:
                print(error)
                response = "An error is occured"
                return make_response(response, 500)


        elif dimension == None and selector == 1: #devo prendere gli slot liberi massimi residui di una certa posizione 

                try:

                    #cursor.execute('SELECT MAX(c.numOfSlot - COALESCE(l.slotOccupati, 0)) AS MaxOccupied FROM cabinet c LEFT JOIN log l ON l.idCabinet = c.idCabinet AND l.timeLog = (SELECT MAX(l2.timeLog) FROM log l2 WHERE l2.idCabinet = c.idCabinet) INNER JOIN  PoP p ON c.idPOP = p.idPOP WHERE p.popPosition = %s', [position])

                    #result = cursor.fetchone()


                    cursor.execute('SELECT idCabinet, numOfSlot from Cabinet AS C join Pop As P on C.idPOP = P.idPOP WHERE P.popPosition = %s', [position])

                    max_dimensions = cursor.fetchall()

                    dictionary_max_dimensions = {elem[0] : elem[1] for elem in max_dimensions}

                    print(dictionary_max_dimensions)

                    cursor.execute('SELECT C.idCabinet, COALESCE(D.usedSlot, CAST(0 AS VARCHAR(15))) FROM Device AS D JOIN Cabinet AS C ON D.idCabinet= C.idCabinet JOIN POP AS P ON p.idPOP = C.idPOP WHERE P.popPosition = %s AND D.usedSlot != %s GROUP BY C.idCabinet, D.usedSlot ORDER BY usedSlot', [position, '-'])

                    result = cursor.fetchall()


                    listEffective, all_free = cleanResult(result, 0, dictionary_max_dimensions) #pulisco il risultato


                    listEffective = sorted(listEffective, key=sorting_key)

                    print("List_effective:")
                    print(listEffective)
                    print("All_free:")
                    print(all_free)


                    resp = []
                    maxval = 0

                    if len(listEffective) != 0:
                        resp = check_space_for_cabinet(listEffective, dictionary_max_dimensions) #preparo la risposta

                        if len(all_free) != 0:
                            all_free_max = max(all_free)

                            if len(resp) != 0 and all_free_max > max(resp):
                                maxval  = all_free_max

                            elif len(resp) == 0:
                                maxval = all_free_max

                            else:
                                maxval = max(resp)
                        else:
                            maxval = max(resp)

                    elif len(all_free) != 0:
                        maxval = max(all_free)

                    
                    
 
                    if maxval > 0:
                        
                        
                        response = jsonify(maxval)
                        return make_response(response, 200)

                    else:
                        response = "No slot dimension found."
                        return make_response(response, 404)

                except (psycopg2.DatabaseError, TypeError) as error:
                    print(error)
                    response = "An error is occured"
                    return make_response(response, 500)

                except (ValueError) as error:
                    print(error)
                    response = "No slot dimension found."
                    return make_response(response, 404)





""" ----- CLASSE DEVICE REST ---- 

Utilizza le variabili globali cursor, email e matricola. 

METODI IMPLEMENTATI: GET, POST,  DELETE

GET: La get può avere due valenze. Di seguito ne sono riportate le funzionalità (/device/<string:cabinet>):
    - Se il cabinet non è fornito, restituisco tutti i device (Debugging)
    - Se ilcabinet è fornito, fornisco i device di quel cabinet.

POST: Permette di aggiungere un dispositivo e aggiornare il log. Il suo comportamento è diverso a seconda se risulta essere un inserimento di un dispositivo 
o una sostituzione. Questo viene capito dal JSON creato appositamente per distinguere le due richieste.


DELETE: Permette di mettere in stato "Removed" un dispositivo e aggiornare il log. Il suo comportamento è diverso a seconda se risulta essere una rimozione di un dispositivo 
o una sostituzione. Questo viene capito dal JSON creato appositamente per distinguere le due richieste.

"""


class Device(Resource):

    global cursor
    global matricola
    global email


    def get(self, cabinet=None):

        if email==None or matricola==None:

            response = "Session expired."
            return make_response(response, 419)


        if cabinet==None:

            try:
                cursor.execute("SELECT DT.DeviceType, D.serialnumber, D.producerdevice,D.statusdevice, D.iddevice FROM Device AS D LEFT JOIN DeviceType AS DT ON D.idDeviceType=DT.idDeviceType")

                devices = cursor.fetchall()

                if len(devices) != 0:


                    response = jsonify(devices)
                    return make_response(response, 200)

                else:

                    response = "*Nessun dispositivo trovato*"
                    return make_response(response, 404)

            except (Exception, psycopg2.DatabaseError, TypeError) as error:
                print(error)
                response = "An error is occured"
                return make_response(response, 500)



        else:

            #prende i dispositivi attivi o inattivi in un certo cabinet (può essere pure dismesso)

            try:

                cursor.execute("SELECT DT.DeviceType, D.serialnumber, D.producerdevice,D.statusdevice, D.iddevice, D.usedSlot FROM Device AS D LEFT JOIN DeviceType AS DT ON D.idDeviceType=DT.idDeviceType WHERE (D.statusDevice = 'Active' OR D.statusDevice = 'Inactive') AND D.idCabinet= %s", [cabinet])

                devices = cursor.fetchall()

                if len(devices) != 0:

                    response = jsonify(devices)
                    return make_response(response, 200)

                else:

                    response = "*Nessun dispositivo trovato*"
                    return make_response(response, 404)

            except (Exception, psycopg2.DatabaseError, TypeError) as error:
                print(error)
                response = "An error is occured"
                return make_response(response, 500)


          

    #questa ci permetterà di aggiornare un dispositivo come "Rimosso"
    def delete(self): 

        if email==None or matricola==None:

            response = "Session expired."
            return make_response(response, 419)
        
        try:

                data = request.get_json()

                idDevice = data["idDevice"]

                opType = data["type"]



                cursor.execute("UPDATE Device SET statusDevice = 'Removed', usedSlot='-' WHERE idDevice=%s AND (statusDevice = 'Active' OR statusDevice = 'Inactive')", [str(idDevice)]) # dopo aver fatto update, devo creare un nuovo log in cui indico l'azione fatta 

                
                if cursor.rowcount != 0:

                   
                
                    cursor.execute("SELECT L.slotOccupati, D.idCabinet, D.sizeDevice FROM Log AS L JOIN Device AS D ON  D.idCabinet = L.idCabinet WHERE D.idCabinet = (SELECT idCabinet FROM Device WHERE idDevice=%s) AND L.timeLog = (SELECT MAX(timeLog) FROM Log where idCabinet=D.idCabinet)", [str(idDevice)]) #mi prendo la dimensione del cabinet 


                    result = cursor.fetchall()

                    res = result[len(result)-1]

                    
                    slotOccupati=res[0]
                    idCabinet=res[1]
                    sizeDevice=res[2]
                    

                    newOccupied = slotOccupati-sizeDevice 


                    mutex.acquire()

                    if email != None and matricola != None:

                    
                        if opType == "delete": #operazione di eliminazione

                            current_timestamp = datetime.now()# prende data e ora        
                            cursor.execute("INSERT INTO Log (dateLog, timeLog, slotOccupati, idDevice, idEmployee, idCabinet, idAction)  values(%s, %s, %s, %s, %s, %s, %s)", (date.today(), current_timestamp.strftime("%Y-%m-%d %H:%M:%S"), newOccupied, str(idDevice), str(matricola), idCabinet, 2))

                        elif opType == "update": #operazione di update

                            current_timestamp = datetime.now()# prende data e ora       
                            cursor.execute("INSERT INTO Log (dateLog, timeLog, slotOccupati, idDevice, idEmployee, idCabinet, idAction)  values(%s, %s, %s, %s, %s, %s, %s)", (date.today(), current_timestamp.strftime("%Y-%m-%d %H:%M:%S"), newOccupied, str(idDevice), str(matricola), idCabinet, 3))



                        if cursor.rowcount != 0:

                            conn.commit()
                            mutex.release()
                            result = "Dispositivo rimosso correttamente, Log aggiornato."
                            requests.get("http://192.168.1.14:3000/notify")
                            return make_response(result, 200)

                        else:
                            mutex.release()
                            conn.rollback()
                            response = "Errore nell'aggiornamento, riprova più tardi."
                            return make_response(response, 404)


                    else:
                        conn.rollback()
                        response = "Session Expired."
                        mutex.release()
                        return make_response(response, 419)

                    
                else:
                    conn.rollback()
                    response = "Nessun dispositivo trovato che rispetti i criteri. "
                    return make_response(response, 404)
                
                
        
        except (Exception, psycopg2.DatabaseError, TypeError) as error:
                print(error)
                mutex.release()
                response = "An error is occured."
                return make_response(response, 500)


    def post(self):

        if email==None or matricola==None:

            response = "Session expired."
            return make_response(response, 419)


        data = request.get_json()

        try:

            #facciamo query inserimento prima come dispositivo, poi il Log

            idDeviceType = 0
            if data["deviceType"] == "Router":
                idDeviceType = 1
            elif data["deviceType"] == "Switch":
                idDeviceType = 2    
            elif data["deviceType"] == "Firewall":
                idDeviceType = 3
            elif data["deviceType"] == "PowerSupply":
                idDeviceType = 4
            

            mutex.acquire()

            if email != None and matricola != None:
                
                cursor.execute("INSERT INTO Device (serialNumber, sizeDevice, producerDevice, yearProduction, statusDevice, usedSlot, idDeviceType, idEmployee, idCabinet) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", [data["serial"], data["dimension"], data["producer"], data["yearOfProduction"], data["statusDevice"], data["usedSlot"], str(idDeviceType), str(matricola), data["idCabinet"]]) 
            
                if cursor.rowcount != 0:

                    cursor.execute("SELECT max(idDevice) from Device")

                    idDevice = cursor.fetchone()[0]

                    print(idDevice)

                    cursor.execute('SELECT slotOccupati FROM Log WHERE timeLog = (SELECT MAX(timeLog) FROM Log WHERE idCabinet = %s)', [data["idCabinet"]])

                    res = cursor.fetchone()

                    occupiedSlot=""

                    if res != None:
                        occupiedSlot = str(res[0] + int(data["dimension"]))
                    else:
                        occupiedSlot = str(int(data["dimension"]))

                    print(occupiedSlot)

                    if data["updatedDevice"] == None:

                        current_timestamp = datetime.now()# prende data e ora       
                        cursor.execute("INSERT INTO Log (dateLog, timeLog, slotOccupati, idDevice, idEmployee, idCabinet, idAction)  values (%s, %s, %s, %s, %s, %s, %s)", [date.today(), current_timestamp.strftime("%Y-%m-%d %H:%M:%S"), occupiedSlot, str(idDevice), str(matricola), data["idCabinet"], 1])

                    else:
                        current_timestamp = datetime.now()# prende data e ora       
                        cursor.execute("INSERT INTO Log (dateLog, timeLog, slotOccupati, idDevice, idEmployee, idCabinet, idAction, idDeviceReplaced)  values (%s, %s, %s, %s, %s, %s, %s, %s)", [date.today(), current_timestamp.strftime("%Y-%m-%d %H:%M:%S"), occupiedSlot, str(idDevice), str(matricola), data["idCabinet"], 3, data["updatedDevice"]])



                    response = "Device inserted correctly."

                    conn.commit()
                    mutex.release()
                    requests.get("http://192.168.1.14:3000/notify") #notifica
                    return make_response(response, 200)
                    
                else:
                    conn.rollback()
                    response = "An error is occured."
                    mutex.release()
                    return make_response(response, 500)
                   


            else:
                conn.rollback()
                response = "Session Expired."
                mutex.release()
                return make_response(response, 419)


        except (Exception, psycopg2.DatabaseError, TypeError) as error:

            print(error)
            mutex.release()
            conn.rollback()
            response = "An error is occured."
            return make_response(response, 500)




""" ----- CLASSE EMPLOYEE REST ---- 

Utilizza le variabili globali cursor, email e matricola. 

METODI IMPLEMENTATI: GET, POST

GET: Utile per capire se il dipendente ha una sessione attiva o meno.

POST: Permette di effettuare l'accesso. 

"""



class Employee(Resource):
    
        def get(self): #questa mi serve semplicemente per capire se la sessione è attiva o meno 

            if email==None or matricola==None:

                response = "Session expired."
                return make_response(response, 419)

            else:
                response = "Sessione attiva."
                return make_response(response, 200) 

        def post(self):
            
            global email
            global matricola


            data = request.get_json()
            print(data)

            try:
                mat = data["matricola"]
                Email = data["email"]

                try:
                    cursor.execute("SELECT idEmployee, email FROM Employee WHERE (idEmployee = %s AND email = %s)", [mat, Email])

                    result = cursor.fetchall()

                    print(result)
                    
                    if len(result) != 0: #allora sono presente nel db, metto i dati

                        matricola=mat
                        email=Email

                        response = "Login successful."
                        return make_response(response, 200)

                    else:
                        response = "The user does not exist."
                        return make_response(response, 404)

                except (psycopg2.Error):
                    cursor.close()


            except (Exception, psycopg2.DatabaseError, TypeError) as error:
                print(error)
                response = "An error is occured."
                return make_response(response, 500)




def sorting_key(item):
    
    string = item[0]
    prefix, first_num, second_num = string.split()[0], int(string.split()[2]), int(string.split()[4])
    return (prefix, first_num, second_num)



def checkTime():

    global email
    global matricola
    global mutex

    while True:
        if email != None and matricola != None:
            time.sleep(1800)

            mutex.acquire()

            email=None
            matricola=None

            print("Sessione terminata.")
            mutex.release()

    

api.add_resource(Cabinet, '/cabinet/<string:position>/<int:dimension>','/cabinet/<int:selector>/<string:position>')
api.add_resource(Device, '/device', '/device/<string:cabinet>')
api.add_resource(Employee, '/employee')



if __name__ == '__main__':
    thread = Thread(target=checkTime)
    thread.start()
    app.run(host = "0.0.0.0", port=4000) #il parametro serve per far runnare l'app sull'IP Address

