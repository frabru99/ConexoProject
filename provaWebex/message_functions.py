
from webexteamsbot import TeamsBot
import os
import requests
from webexteamsbot import TeamsBot
from webexteamsbot.models import Response
import sys
import json
from io import BytesIO
from PIL import Image
import geocoder
from geopy.geocoders import Nominatim
import sys
from urllib.parse import quote


"""

Funzioni ausiliarie per l'invio dei messaggi con Attachment (tra cui Adaptive Card):
- create_message_with_attachment: permette di generare un messaggio con attachment e inviarlo al bot.
- get attachment_actions: permette di prendere il JSON di risposta alla pressione di un tasto,
- ret_message: funzione per Debugging.

"""

bot_email = "conexo@webex.bot"
teams_token = "NDkxMGIyNDAtNjgwZS00ZGM1LTkyMjAtY2ZmYTYwMDE3Zjc4NTUzZDU1MTEtOGRk_P0A1_9db452ae-a8fa-4c45-ad97-a9c6809f2db1"
bot_app_name = "Conexo"
bot_url = "https://f8ae-93-147-221-46.ngrok-free.app"




def create_message_with_attachment(rid, msgtxt, attachment):
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + teams_token,
    }

    url = "https://api.ciscospark.com/v1/messages"
    data = {"roomId": rid, "attachments": [attachment], "markdown": msgtxt}
    response = requests.post(url, json=data, headers=headers)
    return response.json()



def get_attachment_actions(attachmentid):
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + teams_token,
    }

    url = "https://api.ciscospark.com/v1/attachment/actions/" + attachmentid
    response = requests.get(url, headers=headers)
    return response.json()



def ret_message(incoming_msg):
    """
    Sample function that uses a Response object for more options.
    :param incoming_msg: The incoming message object from Teams
    :return: A Response object based reply
    """
    # Create a object to create a reply.
    response = Response()

    

   
    return response