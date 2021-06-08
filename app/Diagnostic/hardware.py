#!/usr/bin/env python3
from http import modules

notif= modules.Notification()

class Anomalies:

    #WebHokk URL Provided By Discord (this url serve to communicate with Discord App)
    discord_channel=Webhook(cfg.urls["webhookurl"])
    #state_url contains the url of state from REST Server
    state_url=cfg.urls["stateurl"]
    #settings_url contains the url of state from REST Server
    settings_url=cfg.urls["settingsurl"]

    def startEvent(self):

        start_date_event,end_date_event=notif.getEventDate()
        #if(start_date_event):
        print(start_date_event)
        print(notif.robot_status_list)




if __name__ == "__main__":
 log= Anomalies()
 log.startEvent