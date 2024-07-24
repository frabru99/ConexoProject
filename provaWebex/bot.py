
from webexteamsbot import TeamsBot
import os
import requests
from webexteamsbot import TeamsBot
from webexteamsbot.models import Response
import sys
import json
import geocoder
from geopy.geocoders import Nominatim
import sys
from urllib.parse import quote
import ast 
import re
import time


from message_functions import create_message_with_attachment, get_attachment_actions, ret_message
from add_card import show_add_card, show_add_card_dimension, getJson
from delete_card import show_remove_card_cabinet, show_remove_card_device
from update_card import show_remove_card_cabinetup,show_remove_update_card, show_insert_update_card, show_update_card_dimension



def get_ngork_url():
    while True:
        try:
            response = requests.get('http://127.0.0.1:4040/api/tunnels')
            data = response.json()
            tunnel_url = data['tunnels'][0]['public_url']
            return tunnel_url
        except(requests.exceptions.ConnectionError, IndexError, KeyError):
            time.sleep(1)

""" -------------------- CREAZIONE DEL BOPT E DEFINIZIONE VARIABILI -------------------- """
# Retrieve required details from environment variables

bot_email = "conexo@webex.bot"
teams_token = "NDkxMGIyNDAtNjgwZS00ZGM1LTkyMjAtY2ZmYTYwMDE3Zjc4NTUzZDU1MTEtOGRk_P0A1_9db452ae-a8fa-4c45-ad97-a9c6809f2db1"
bot_app_name = "Conexo"
bot_url = str(get_ngork_url())


cabinet = None #variabile globale cabinet per aggiornamento
posizione = None #variabile globale per la posizione
ipaddress = sys.argv[1]
dimension = None
idDeviceUp = None



if not bot_email or not teams_token or not bot_url or not bot_app_name:
    print(
        "sample.py - Missing Environment Variable. Please see the 'Usage'"
        " section in the README."
    )
    if not bot_email:
        print("TEAMS_BOT_EMAIL")
    if not teams_token:
        print("TEAMS_BOT_TOKEN")
    if not bot_url:
        print("TEAMS_BOT_URL")
    if not bot_app_name:
        print("TEAMS_BOT_APP_NAME")
    sys.exit()


# Create a Bot Object
#   Note: debug mode prints out more details about processing to terminal
#   Note: the `approved_users=approved_users` line commented out and shown as reference
bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    debug=True,
    # approved_users=approved_users,
    webhook_resource_event=[
        {"resource": "messages", "event": "created"},
        {"resource": "attachmentActions", "event": "created"},
    ],
)



""" ------------- FUNZIONE PER LA POSIZIONE-------------- """
def get_current_gps_coordinates():
    g = geocoder.ip('me')
    if g.latlng is not None: 
        return g.latlng
    else:
        return None




""" --------------------- FUNZIONE SHOW_CARD INIZIALE E di HANDLE ----------------------- """

"""
SHOW_CARD: Questa adaptive card viene mostrata alla pressione del comando "/gestisci", e permette di 
Inserire undispositivo, Eliminare un dispositivo, Sostituire un dispositivo. 
"""
def show_card(incoming_msg):
    attachment = """
    {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": {
            "type": "AdaptiveCard",
            "body": [{
                "type": "Container",
                "items": [{
                    "type": "TextBlock",
                    "text": "Gestisci i dispositivi",
                    "size": "large"
                }]
                }, 
                {
                    "type": "TextBlock",
                    "text": "Sede di """ + f'{posizione}' +  """ ",
                    "weight": "bolder",
                    "size": "medium",
                    "color": "Good"
                }],
            "actions": [{
                    "type": "Action.Submit",
                    "title": "Inserisci",
                    "data": "add",
                    "style": "positive",
                    "id": "button1"
                },
                {
                    "type": "Action.Submit",
                    "title": "Rimuovi",
                    "data": "remove",
                    "style": "destructive",
                    "id": "button2"
                },
                {
                    "type": "Action.Submit",
                    "title": "Sostituisci",
                    "data": "update",
                    "style": "default",
                    "id": "button3"
                }
            ],
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.0"
        }
    }
    """
    backupmessage = "This is an example using Adaptive Cards."

    c = create_message_with_attachment(
        incoming_msg.roomId, msgtxt=backupmessage, attachment=json.loads(attachment)
    )
 
    return ""




"""
HANDLE_CARDS: Funzione che permette di gestire tutte le pressioni dei botton di tutte le adaptive card. 
"""
def handle_cards(api, incoming_msg):
    
    global cabinet #variabile globale utile per l'aggiornamento. 
    global dimension #utile per la dimensione scelta nell'inserimento
    global idDeviceUp #variabile globale idDevice rimosso

    m = get_attachment_actions(incoming_msg["data"]["id"]) #messaggio in arrivo, utile per icavare le info scelte 
   
    #SE VOGLIAMO GESTIRE LA POSIZIONE CHIESTA ALL'UTENTE, MEETTERE QUI l'IF
   
    
    print("STAMPA MESSAGGIO")
    print(m)

    

    if isinstance(m["inputs"], dict) and m["inputs"]["action"] == "auth":


        if m["inputs"]["Matricola"] == "" or m["inputs"]["Email"] == "":
            return "*Si prega di compilare tutti i campi.*"


         #LOGIN
        if m["inputs"]["action"] == "auth" and m["inputs"]["Matricola"] != "" and m["inputs"]["Email"] != "":
            
            url = "http://"+ipaddress+":4000/employee"

            data = {"matricola": m["inputs"]["Matricola"], "email": m["inputs"]["Email"]}
        
            headers = {
                'Content-Type': 'application/json'
            }


            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                return "*Accesso avvenuto correttamente.*"
            elif response.status_code == 404:
                return "*L'utente indicato non esiste. Riprovare.*"

        

    url = "http://"+ipaddress+":4000/employee"

    response = requests.get(url)

    if response.status_code == 200:

        #GESTIONE_PULSANTI_SINGOLI

        #Gestione della pressione di "Inserisci", "Elimina" o "Sostituisci" 
        if m["inputs"]== "add":
            show_add_card_dimension(m, posizione, ipaddress)

        if  m["inputs"]== "remove":
            show_remove_card_cabinet(m, posizione, ipaddress)

        if m["inputs"]== "update":
            show_remove_card_cabinetup(m, posizione, ipaddress) 


         

        #ELIMINAZIONE
        if m["inputs"]["action"] == "cabinet" and m["inputs"]["selectOption"] != "": #Dopo aver scelto l'armadietto

            show_remove_card_device(m, ipaddress) #Card per scegliere il device da eliminare 

            return ""

        if m["inputs"]["action"] == "elimina" and m["inputs"]["selectOption"] != "":


            url = 'http://' +ipaddress+ ':4000/device'

            data = {"idDevice": m["inputs"]["selectOption"], "type": "delete"}

            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.delete(url, json=data, headers=headers)


            if response.status_code == 200:

                return "*Eliminato correttamete device con ID: **{}***".format(m["inputs"]["selectOption"])

            elif response.status_code ==419:
                return "*Sessione scaduta, effettuare l'accesso.*"

            else:

                return "*Errore, elemento non eliminato o non presente.**{}***".format(m["inputs"]["selectOption"])

        



        #INSERIMENTO
        if m["inputs"]["action"] == "dimension" and m["inputs"]["selectOption"] != "":


            dimension=int(m["inputs"]["selectOption"]) 

            show_add_card(m, posizione, ipaddress, dimension) #mostriamo la card di aggiunta con i campi da compilare

            return ""

        if m["inputs"]["action"] == "Inserimento" and (m["inputs"]["Armadietto"] != "" and m["inputs"]["Immagine"] != "" and m["inputs"]["Tipologia dispositivo"] != ""):

            

            try:
                data = str(m["inputs"]["Immagine"]) #dati json inviati per il dispositivo

                data_to_send = getJson(data, m["inputs"]["Armadietto"], m["inputs"]["Tipologia dispositivo"], dimension)

                print(data_to_send)


                headers = {
                    'Content-Type': 'application/json'
                }

                url = "http://"+ipaddress+":4000/device"

                response = requests.post(url, json=data_to_send, headers=headers)


                if response.status_code==200:
                    return "*Dispositivo inserito correttamente.*"

                elif response.status_code==404:

                    return "*Non è stato possibile inserire l'elemento perché già presente o per altri errori.*"
                    
                elif response.status_code==419:

                    return "*Sessione scaduta, effettuare l'accesso.*"

                elif response.status_code==500:
                    return "*Errore, riprovare più tardi.*"
            
           

            
            except (Exception, SyntaxError) as error:
                print(error)
                return "*Errore. Si prega di ricontrollare i campi e riprovare l'inserimento.*"
            

            
                

            return ""



        #SOSTITUZIONE
        if m["inputs"]["action"] == "cabinet_remove_update" and m["inputs"]["selectOption"] != "": 

            cabinet = m["inputs"]["selectOption"]

            show_remove_update_card(m, ipaddress) #mostro la card di rimozione del dispositivo NEL CABINET

            return "" 

        if m["inputs"]["action"] == "remove_update" and m["inputs"]["selectOption"] != "": #dopo questo, devo aggiungere un nuovo dispositivo


            idDeviceUp = m["inputs"]["selectOption"]

            url = 'http://' +ipaddress+ ':4000/device'

            data = {"idDevice": m["inputs"]["selectOption"], "type": "update"}

            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.delete(url, json=data, headers=headers)



            if response.status_code==200:

                show_update_card_dimension(m, posizione, ipaddress) #carta di aggiunta dispositivo, entro la lunghezza del dispositivo precedente
                return "*Elemento eliminato con ID: **{}***".format(m["inputs"]["selectOption"])

            elif response.status_code==404:

                return "*Non è stato possibile eliminare l'elemento, perché non esiste.*"
                
            elif response.status_code==419:

                return "*Sessione scaduta, effettuare l'accesso.*"

            elif response.status_code==500:
                return "*Errore, riprovare più tardi.*"


            
        if m["inputs"]["action"] == "update_dimension" and m["inputs"]["selectOption"] != "": #ho scelto la dimensione

                dimension = int(m["inputs"]["selectOption"])
                show_insert_update_card(m, posizione, ipaddress, m["inputs"]["selectOption"])

        
        if m["inputs"]["action"] == "termina_update" and (m["inputs"]["Armadietto"] != "" and m["inputs"]["Immagine"] != "" and m["inputs"]["Tipologia dispositivo"] != ""):
            

            try:
                data = str(m["inputs"]["Immagine"]) #dati json inviati per il dispositivo

                data_to_send = getJson(data, m["inputs"]["Armadietto"], m["inputs"]["Tipologia dispositivo"], dimension, idDeviceUp)

                print(data_to_send)


                headers = {
                    'Content-Type': 'application/json'
                }

                url = "http://"+ipaddress+":4000/device"

                response = requests.post(url, json=data_to_send, headers=headers)


                if response.status_code==200:
                    return "*Dispositivo inserito correttamente.*"

                elif response.status_code==404:

                    return "*Non è stato possibile inserire l'elemento perché già presente o per altri errori.*"
                    
                elif response.status_code==419:

                    return "*Sessione scaduta, effettuare l'accesso.*"

                elif response.status_code==500:
                    return "*Errore, riprovare più tardi.*"
            
           

            
            except (Exception, SyntaxError) as error:
                print(error)
                return "*Errore. Si prega di ricontrollare i campi e riprovare l'inserimento.*"
            

        
        return "*Si prega di compilare tutti i campi.*"

    
    elif response.status_code == 419:

        return "*Sessione scaduta, effettuare l'accesso.*"
    elif response.status_code == 500:

        return "*Errore del Server. Riprovare più tardi.*"

    



"""------------------ AUTENTICAZIONE ------------------ """


def show_auth_direct(incoming_msg):


    attachment= """
    {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": {
            "type": "AdaptiveCard",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "AUTENTICAZIONE",
                    "weight": "bolder",
                    "size": "large",
                    "color": "Light"
                },
                {
                    "type": "Input.Text",
                    "id": "Email",
                    "placeholder": "Indirizzo email"
                },
                {
                    "type": "Input.Text",
                    "id": "Matricola",
                    "placeholder": "Matricola Identificativa"
                }
            ],
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Login",
                    "data": {
                        "action": "auth"
                    },
                    "style": "positive"
                }
            ],
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.0"
                }
            }

            """

    backupmessage = "This is an example using Adaptive Cards."

    
    c = create_message_with_attachment(
        incoming_msg.roomId, msgtxt=backupmessage, attachment=json.loads(attachment)
    )
    print(c)

    return ""
    
    
    


# Add new commands to the bot.
bot.add_command("attachmentActions", "*", handle_cards)
bot.add_command("/gestisci", "Gestisci i dispositivi.", show_card)
bot.add_command("/login", "Autenticazione dipendenti.", show_auth_direct)



# Every bot includes a default "/echo" command.  You can remove it, or any
# other command with the remove_command(command) method.
bot.remove_command("/echo")

if __name__ == "__main__":
    

    coordinates = get_current_gps_coordinates() #Retreive della posizione

    if coordinates is not None:

        latitude, longitude = coordinates
        print(f"Your current GPS coordinates are:")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")

        # calling the nominatim tool
        geoLoc = Nominatim(user_agent="GetLoc")
    

        pos = str(latitude) + ", " + str(longitude)
        # passing the coordinates
        posizione = str(geoLoc.reverse(pos)).split(',')[3] #Mi prendo la città

        posizione = posizione.strip()

        bot.run(host="0.0.0.0", port=5000)
    else:
        print("Non è stato possibile recuperare la posizione. ")


