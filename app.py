#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from flask import Flask, request
from tinydb import TinyDB, Query
import argparse
import json
import requests
import os
import aiml
import config

# Carga aplicación Flask
app = Flask(__name__)

# Carga nucleo de AIML
k = aiml.Kernel()

# Carga base de datos de conversaciones
db = TinyDB('conversations.json')
Usuario= Query()

# Función auxiliar que envia el mensaje
def send_message(recipient_id, message_text):
    params = {
        "access_token": config.ACCESS_TOKEN,
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)


# Punto de entrada para verificación
@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == config.VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


# Punto de llegada para mensajes
@app.route('/', methods=['POST'])
def webhook():
    print("hello")
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
		# Nos llegó un mensaje al que hay que responde
                if messaging_event.get("message"):
                    # Se obtiene la información del mensaje
                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    user=db.search(Usuario.user == sender_id)
                    if len(user)==0:
                        user=db.insert({'user':sender_id,'conversations':[[]]})
                        user=db.get(eid=user)
                    else:
                        user=user[0]
                    ans=k.respond(message_text)
                    conv=user['conversations']
                    conv[-1].append({'msg':message_text,'ans':ans})
                    db.update({'conversations':conv},eids=[user.eid])
                    send_message(sender_id, ans)

                # El mensaje llegó
                if messaging_event.get("delivery"): 
                    pass
                # El usuario aceptó chatear
                if messaging_event.get("optin"):
                    pass
                # Que hacer después del mensaje
                if messaging_event.get("postback"):
                    pass

    return "ok", 200

# Función principal (interfaz con línea de comandos)
if __name__ == '__main__':
    p = argparse.ArgumentParser("pyAIML")
    p.add_argument("--host",default="127.0.0.1",
            action="store", dest="host",
            help="Root url [127.0.0.1]")
    p.add_argument("--port",default=5000,type=int,
            action="store", dest="port",
            help="Port url [500]")
    p.add_argument("--aiml",default="aiml/mibot.aiml",type=str,
            action="store", dest="aiml",
            help="AIML file with rules [aiml/mibot.aiml]")
    p.add_argument("--debug",default=False,
            action="store_true", dest="debug",
            help="Use debug deployment [Flase]")
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")

    opts = p.parse_args()

    k.learn(opts.aiml)
    k.respond("load aiml b")

    app.run(debug=opts.debug,
            host=opts.host,
            port=opts.port)
