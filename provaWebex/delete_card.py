import requests
import json



from message_functions import create_message_with_attachment, get_attachment_actions, ret_message



""" -------------------- CREAZIONE DEL BOPT E DEFINIZIONE VARIABILI -------------------- """
# Retrieve required details from environment variables

bot_email = "conexo@webex.bot"
teams_token = "NDkxMGIyNDAtNjgwZS00ZGM1LTkyMjAtY2ZmYTYwMDE3Zjc4NTUzZDU1MTEtOGRk_P0A1_9db452ae-a8fa-4c45-ad97-a9c6809f2db1"
bot_app_name = "Conexo"
bot_url = "https://f8ae-93-147-221-46.ngrok-free.app"





""" ------------------------------ ELIMINAZIONE ------------------------------------- 

- Viene chiesto il cabinet interessato (relativo alla sede in cui mi trovo).
- Se il cabinet non risulta vuoto, allora torna la lista dei dispositivi presenti da poter eliminare.

"""






"""

SHOW_REMOVE_CARD_DEVICE: Scelta del cabinet da eliminare. 
- La query permette di prendere tutti i cabinet relativi alla posizione "pos" passata come parametro.
- I cabinet disponibili vengono poi messi una lista e esposti come una Option List.

"""
def show_remove_card_cabinet(incoming_msg, pos, ipaddress):


    
    url = 'http://' +ipaddress + ':4000/cabinet/0/'+pos


    response = requests.get(url)


    if response.status_code == 200:

        data = response.json()

        print(data)

        options = [{"title":str("Cabinet " + cabinet[0]),  "value": cabinet[0]} for cabinet in data]
        

        attachment = """
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "body": [
                    {
                    "type": "TextBlock",
                    "text": "ELIMINAZIONE",
                    "weight": "bolder",
                    "size": "large",
                    "color": "Attention"
                    },
                    {
                        "type": "TextBlock",
                        "text": "Seleziona un cabinet:",
                        "weight": "bolder",
                        "size": "medium"
                    },
                    {
                        "type": "Input.ChoiceSet",
                        "id": "selectOption",
                        "choices": [""" + ','.join([f'{{"title": "{opt["title"]}", "value": "{opt["value"]}"}}' for opt in options]) + """],
                        "style": "compact",
                        "isMultiSelect": false
                    }
                ],
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Conferma",
                        "data": {
                            "action": "cabinet"
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

        print("Cabinet non trovato, invio messaggio di errore.")
        error_message = "*Nessun cabinet trovato nella posizione attuale*"
        
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

SHOW_REMOVE_CARD_DEVICE: Scelta del cabinet da eliminare. 
- La query permette di prendere tutti i dispositivi relativi a quel cabinet.
- I cabinet disponibili vengono poi messi una lista e esposti come una Option List.

"""
def show_remove_card_device(incoming_msg, ipaddress):

    chosenCabinet = incoming_msg["inputs"]["selectOption"]

    print("CABINET:" + chosenCabinet)

    url = 'http://' +ipaddress + ':4000/device/'+chosenCabinet


    response = requests.get(url)
    
    if response.status_code == 200:

        data = response.json()

        #elem è composto in questo modo: [Tipologia, SerialNumber, Produttore, Stato, ID, UsedSlot]
        options = [{"title": elem[0] + " di " + elem[2] + " : " + elem[1] + " : " +  elem[3] + " : "+ str(elem[5]),  "value": elem[4]} for elem in data]
        

        attachment = """
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": "ELIMINAZIONE",
                        "weight": "bolder",
                        "size": "large",
                        "color": "Attention"
                    },
                    {
                        "type": "TextBlock",
                        "text": "Cabinet scelto: """ + f'{chosenCabinet}' +  """ ",
                        "weight": "bolder",
                        "size": "medium",
                        "color": "Warning"
                    },
                    {
                        "type": "TextBlock",
                        "text": "Seleziona un device: ",
                        "weight": "bolder",
                        "size": "medium"
                    },
                    {
                        "type": "Input.ChoiceSet",
                        "id": "selectOption",
                        "choices": [""" + ','.join([f'{{"title": "{opt["title"]}", "value": "{opt["value"]}"}}' for opt in options]) + """],
                        "style": "expanded",
                        "isMultiSelect": false,
                        "wrap": true
                    }
                ],
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Elimina",
                        "data": {
                            "action": "elimina"
                        },
                        "style": "destructive"
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

        print("Device non trovati, invio messaggio di errore.")
        error_message = "*Nessun device trovato nel cabinet attuale*"
        
        c = create_message_with_attachment(
            incoming_msg["roomId"], msgtxt=error_message, attachment=None
        )
    
        return ""
        
    elif response.status_code >= 500:

        print("Errore interno del server, invio messaggio di errore.")
        error_message = "*Errore interno del server. Riprovare più tardi.*"
        
        c = create_message_with_attachment(
            incoming_msg["roomId"], msgtxt=error_message, attachment=None
        )
    
        return ""