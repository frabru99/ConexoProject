# Inventory di rete & BI in collaborazione con Cisco System Inc. e Conexo S.R.L.

## Idea
Il progetto consiste nella creazione di un sistema che permette di gestire un inventory di ret di cui è possibile visualizzare indformazioni e stato dei dispositivi in una interfaccia di Business Intelligence, da integrare in una Control Room. 


## Sviluppo e Tecnologie
La suddivisione del progetto avviene in tre parti principali:
 - **Data Acquisition:** Gestione dei dispositivi di rete, tramite un bot appositamente sviluppato su Webex Teams by Cisco.
 - **Data Storage:** Storage dei dati in un database relazionale.
 - **Data Visualization:** Visualizzazione dei dati e monitoring dei dispositivi tramite un interfaccia di Business Intelligence.

Tecnologie Utilizzate:
 - **Data Acquisition:** Python, Webex, ngrok, flask
 - **Data Storage:** PostGreSQL, Python, flask
 - **Data Visualization:** Microsoft PowerBI, flask
 
## Avvio del Sistema

Assicurarsi di aver creato il DataBase con gli inserimenti base e che PostGre sia attivo e in ascolto sulla porta 5432. E' possibile farlo con il comando `netstat -a -b`

![image](https://github.com/user-attachments/assets/8f8e1852-1ca4-46c7-83d9-4418be2af664)

**Avvio del Bot Webex.**
 - Avviare il backend (in cartella backendWebex): backendWebex.py
 - Avviare ngrok con il comando `ngrok http 5000`
 - Avviare il bot con il primo argomento l'indirizzo IP su cui il backend è in ascolto: bot.py



