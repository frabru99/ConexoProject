import json
import requests
from message_functions import create_message_with_attachment, get_attachment_actions, ret_message
import ast 
from foundFields import foundFields

bot_email = "conexo@webex.bot"
teams_token = "NDkxMGIyNDAtNjgwZS00ZGM1LTkyMjAtY2ZmYTYwMDE3Zjc4NTUzZDU1MTEtOGRk_P0A1_9db452ae-a8fa-4c45-ad97-a9c6809f2db1"
bot_app_name = "Conexo"
bot_url = "https://f8ae-93-147-221-46.ngrok-free.app"


""" ------------------------------------ INSERIMENTO ----------------------------------------

Possiamo strutturare l'inserimento in questo modo:
- Da qui, chiediamo la dimensione del dispositivo (occuperemo poi gli slot disponibili in ordine nell'armadietto)
- A seconda di questo, poi chiediamo, IL TIPO DI DISPOSITIVO, L'ARMADIETTO (con quella dimensione disponibile), JSON preso dal QR scansionato dove prenderemo i dati. 

"""

devices = [
        {"title": "Router", "value": "Router"},
        {"title": "Firewall", "value": "Firewall"},
        {"title": "Switch", "value": "Switch"},
        {"title": "PowerSupply", "value": "PowerSupply"}
    ]


"""
SHOW_ADD_CARD_DIMENSION: Card per la scelta della dimensione.

- Richiede la dimensione contigua massima disponibile
- Genera ka card per la scleta di una dimensione per il device.

"""

def show_add_card_dimension(incoming_msg, pos, ipaddress):


    url = 'http://' +ipaddress + ':4000/cabinet/1/'+pos

    response = requests.get(url)


    if response.status_code == 200:

        maxvalue = response.json()


        dimensions = [
            {"title": str(i+1), "value": i+1} for i in range(maxvalue)
        ]
        
        attachment = """
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": "INSERIMENTO",
                        "weight": "bolder",
                        "size": "large",
                        "color": "Good"
                    },
                    {
                        "type": "TextBlock",
                        "text": "Inserisci una dimensione: ",
                        "weight": "bolder",
                        "size": "medium"
                    },
                    {
                        "type": "Input.ChoiceSet",
                        "id": "selectOption",
                        "choices": [""" + ','.join([f'{{"title": "{opt["title"]}", "value": "{opt["value"]}"}}' for opt in dimensions]) + """],
                        "style": "compact",
                        "isMultiSelect": false
                    }
                ],
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Conferma",
                        "data": {
                            "action": "dimension"
                        }
                    }
                ],
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.0"
            }
        }
        """


        backupmessage= "Messaggio di backup"

        c = create_message_with_attachment(
            incoming_msg["roomId"], msgtxt=backupmessage, attachment=json.loads(attachment)
        )

        print(c)
        return ""

    elif response.status_code==419:

        print("Sessione scaduta, invio messaggio di errore.")
        error_message = "*Sessione scaduta, effettuare l'accesso.*"
        
        c = create_message_with_attachment(
            incoming_msg["roomId"], msgtxt=error_message, attachment=None
        )

        return ""  

    elif response.status_code == 404:

        print("Nessun cabinet libero, invio messaggio di errore.")
        error_message = "*Nessun cabinet con spazio libero.*"
        
        c = create_message_with_attachment(
            incoming_msg["roomId"], msgtxt=error_message, attachment=None
        )
    
        return ""

    else:

        print("Errore interno del server, invio messaggio di errore.")
        error_message = "*Errore interno del server. Riprovare più tardi.*"
        
        c = create_message_with_attachment(
            incoming_msg["roomId"], msgtxt=error_message, attachment=None
        )
    
        return ""





"""

SHOW_ADD_CARD: Permette di aggiungere il dispositivo.

Vengono chiesti:
- Tipologia
- Posizione (tra quelle immediatamente disponibili)
- JSON per le caratteristiche del dispositivo.

"""


def show_add_card(incoming_msg, pos, ipaddress, dimension): 


    global devices 


    dimensione = incoming_msg["inputs"]["selectOption"]

    #ora a seconda di questa dimensione, 
    #ci ricaviamo dalla query quelli che hanno una dimensione disponibile >= di quella inserita precedentemente. 
    #facciamo un controllo se quello che torna la query è vuoto non c'è spazio e quindi messaggio di errore!

    url = 'http://' +ipaddress + ':4000/cabinet/'+pos+'/'+dimensione

    response = requests.get(url)

    if response.status_code==200:

        cabinets = response.json()

        #slot_free è una lista contenuta in una lista di liste fatta in questo modo [idDevice, inizioRangePosizione, fineRangePosizione, dimensioneDispositivo]

        positions = [{"title":"Cabinet: " + slot_free[i][0] + " / Posizione disponibile: " + str(slot_free[i][1]) + " - " + str(slot_free[i][2]) ,  "value": slot_free[i]} for slot_free in cabinets if len((slot_free)) > 0 for i in range(len(slot_free))]

        print(positions)

        attachment = """
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": "INSERIMENTO",
                        "weight": "bolder",
                        "size": "large",
                        "color": "Good"
                    },
                    {
                        "type": "TextBlock",
                        "text": "Dimensione scelta: """ + f'{dimensione}' +  """ slot ",
                        "weight": "bolder",
                        "size": "medium",
                        "color": "Warning"
                    },
                    {
                        "type": "TextBlock",
                        "text": "Seleziona tutti i campi per aggiungere il dispositivo.",
                        "weight": "bolder",
                        "size": "medium",
                        "wrap": true
                    },
                    {
                        "type": "TextBlock",
                        "text": "Tipologia dispositivo:"
                    },
                    {
                        "type": "Input.ChoiceSet",
                        "id": "Tipologia dispositivo",
                        "choices": [""" + ','.join([f'{{"title": "{opt["title"]}", "value": "{opt["value"]}"}}' for opt in devices]) + """],
                        "style": "compact",
                        "isMultiSelect": false
                    },
                    {
                        "type": "TextBlock",
                        "text": "Armadietto"
                    },
                    {
                        "type": "Input.ChoiceSet",
                        "id": "Armadietto",
                        "choices": [""" + ','.join([f'{{"title": "{opt["title"]}", "value": "{opt["value"]}"}}' for opt in positions]) + """],
                        "style": "compact",
                        "isMultiSelect": false
                    },
                    {
                        "type": "TextBlock",
                        "text": "Scannerizza il QR del dispositivo e incolla il file JSON qui sotto:",
                        "weight": "bolder",
                        "wrap": true
                    },
                    {
                        "type": "Input.Text",
                        "id": "Immagine",
                        "placeholder": "JSON",
                        "isMultiline": true,
                        "height": "stretch"
                    }
                ],
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Conferma",
                        "data": {
                            "action": "Inserimento"
                        }
                    }
                ],
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.0"
                    }
                }
                """

        backupmessage = "This is an example using Adaptive Cards."

        c = create_message_with_attachment(
            incoming_msg["roomId"], msgtxt=backupmessage, attachment=json.loads(attachment)
        )
        print(c)
        return ""

    elif response.status_code==419:

        print("Sessione scaduta, invio messaggio di errore.")
        error_message = "*Sessione scaduta, effettuare l'accesso.*"
        
        c = create_message_with_attachment(
            incoming_msg["roomId"], msgtxt=error_message, attachment=None
        )

        return ""    

    else:

        print("Errore interno del server, invio messaggio di errore.")
        error_message = "*Errore interno del server. Riprovare più tardi.*"
        
        c = create_message_with_attachment(
            incoming_msg["roomId"], msgtxt=error_message, attachment=None
        )
    
        return ""





"""

getJson: Funzione che trasforma quello inviato tramite adaptive card in formato JSON da mandare con POST al backend.

"""

def getJson(data, cabinet, deviceType, dimension, updatedDevice=None):

    asDictionary = ast.literal_eval(data) #questo trasforma il json inviato tramite Adaptive Card in dizionario. 

    producer, year_of_prod, serial = foundFields(asDictionary)

    asList = ast.literal_eval(cabinet) #informazioni in lista: idArmadietto scelto, spazio occupato, spazio libero.

    idCabinet = asList[0]
    primo_posto = asList[1]
    ultimo_posto = asList[2]



    statusDevice = "Active"

    usedSlot = idCabinet + " - " + str(primo_posto) + " / " + str(ultimo_posto)

    json_data =  {
        "producer": producer[0],
        "yearOfProduction": year_of_prod[0], 
        "serial": serial[0], 
        "idCabinet": idCabinet, 
        "primo_posto": primo_posto,
        "ultimo_posto": ultimo_posto,
        "usedSlot": usedSlot,
        "statusDevice": statusDevice,
        "deviceType": deviceType,
        "dimension": dimension,
        "updatedDevice": updatedDevice
    }
    

    return json_data
