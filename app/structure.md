1. **modules.py** ==> ce fichier comporte les modules nécessaires pour le fichier webhook.py et discord_server.py
structure:
        class Notification:
            #fonction pour faire check sur /state et envoyer son contenu
            def getResponseState(self):
            #fonction pour envoyer un message de batterie
            def batteryMessage(self):
            #fonction pour envoyer un message de disque
            def storageMessage(self):
            #fonction pour envoyer un message de température
            def temperatureMessage(self):
            #fonction pour envoyer un message de humidité
            def humidityMessage(self):
            #récupération de date/heure local
            def getNow(self):
            #convertion de l'heure de l'event 
            def getEventTime(self):
            #convertion de la date de l'event 
            def getEventDate(self):
            #Contenu de message envoyé par webhook : combine les retours des fonctions précédentes pour avoir un message qui sera envoyé par la suite
            def msgWebhook(self):
            #Contenu de message envoyé par bot
            def msgNotify(self):
            #Fonction d'envoi du webhook 
            def postWebhook(self):

2. **discord_server.py** ==> server responsable du fonctionnement du bot ( exemple : Bot_Etisalat)
    structure:
            #fonction permet de vérifier si le bot est bien connecté
            def on_ready()
            #fonction permet l'echange de msg entre utilisateur et bot dans notre cas !notify
            #cette fonction utilise la fonction de msgNotify de modules.py
            async def on_message(message):

3. **webhook.py** ==> fichier responsable d'envoi des messages webhook (post), utilise fonction msgWebhook de  fichier modules.   
