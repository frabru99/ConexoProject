import requests
import json



from message_functions import create_message_with_attachment, get_attachment_actions, ret_message





""" ------------------------------- SOSTITUISCI ------------------------------------------- 

Le Adaptive Card per l'operazione di sostituzione sono del tutto uguali a quelle per Eliminazione e Inserimento. 
Sono state modificate al fine di diversificare la sostituzione dalle due singole operazioni

"""

def show_remove_card_cabinetup(incoming_msg, pos, ipaddress):


    try:

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
                        "text": "SOSTITUZIONE",
                        "weight": "bolder",
                        "size": "large",
                        "color": "Default"
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
                                "action": "cabinet_remove_update"
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



    except (Exception): #poi specializziamo le eccezioni...
        return "Qualcosa è andato storto, riprova."



def show_remove_update_card(incoming_msg, ipaddress):


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
                        "text": "SOSTITUZIONE",
                        "weight": "bolder",
                        "size": "large",
                        "color": "Default"
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
                        "text": "Seleziona un device:",
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
                            "action": "remove_update"
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




def show_update_card_dimension(incoming_msg, pos, ipaddress):

    #possiamo effettuare una query dove ci prendiamo la dimensione massima rimanente tra tutti i cabinet 

    url = 'http://' +ipaddress + ':4000/cabinet/1/'+pos

    response = requests.get(url)


    if response.status_code == 200:

        maxvalue = response.json()

        options = [
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
                        "text": "SOSTITUZIONE",
                        "weight": "bolder",
                        "size": "large",
                        "color": "Default"
                    },
                    {
                        "type": "TextBlock",
                        "text": "Inserisci la dimensione del nuovo dispositivo: ",
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
                            "action": "update_dimension"
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


def show_insert_update_card(incoming_msg, pos, ipaddress, dimension): 


    options2 = [
        {"title": "Router", "value": "Router"},
        {"title": "Firewall", "value": "Firewall"},
        {"title": "Switch", "value": "Switch"},
        {"title": "PowerSupply", "value": "PowerSupply"}
    ]


    dimensione = incoming_msg["inputs"]["selectOption"]

    #ora a seconda di questa dimensione, 
    #ci ricaviamo dalla query quelli che hanno una dimensione disponibile >= di quella inserita precedentemente. 
    #facciamo un controllo se quello che torna la query è vuoto non c'è spazio e quindi messaggio di errore!

    url = 'http://' +ipaddress + ':4000/cabinet/'+pos+'/'+dimensione

    response = requests.get(url)

    if response.status_code==200:

        cabinets = response.json()
  
        options3 = [{"title":"Cabinet: " + slot_free[i][0] + " / Posizione disponibile: " + str(slot_free[i][1]) + " - " + str(slot_free[i][2]) ,  "value": slot_free[i]} for slot_free in cabinets if len((slot_free)) > 0 for i in range(len(slot_free))]

        print(options3)

        attachment = """
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": "SOSTITUZIONE",
                        "weight": "bolder",
                        "size": "large",
                        "color": "Default"
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
                        "choices": [""" + ','.join([f'{{"title": "{opt["title"]}", "value": "{opt["value"]}"}}' for opt in options2]) + """],
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
                        "choices": [""" + ','.join([f'{{"title": "{opt["title"]}", "value": "{opt["value"]}"}}' for opt in options3]) + """],
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
                            "action": "termina_update"
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