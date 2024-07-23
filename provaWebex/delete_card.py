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
Card per eliminazione del dispositivo: Possiamo chiedere posizione (o prenderla) e poi l'armadietto in base a dove mi trovo. 
Poi mostra un selettore che fa vedere le posizioni uniche dei dispositivi con accanto seriale del dispositivo, per decidere quale eliminare. 
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
Scelta dell'elemento da eliminare 
"""
def show_remove_card_device(incoming_msg, ipaddress):

    chosenCabinet = incoming_msg["inputs"]["selectOption"]

    print("CABINET:" + chosenCabinet)

    url = 'http://' +ipaddress + ':4000/device/'+chosenCabinet


    response = requests.get(url)
    
    if response.status_code == 200:

        data = response.json()

        options = [{"title": elem[0] + " / " + elem[1] + " / " + elem[2] + " / " +  elem[3] + " / "+ str(elem[4]),  "value": elem[4]} for elem in data]
        

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
                        "style": "compact",
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