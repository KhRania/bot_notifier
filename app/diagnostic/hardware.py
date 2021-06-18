#!/usr/bin/env python3
import os,sys
from ..state import modules

class Anomalies:

    #WebHokk URL Provided By Discord (this url serve to communicate with Discord App)
    discord_channel=Webhook(cfg.urls["webhookurl"])
    #state_url contains the url of state from REST Server
    state_url=cfg.urls["stateurl"]
    #settings_url contains the url of state from REST Server
    settings_url=cfg.urls["settingsurl"]

    def startEvent(self):

        start_date_event,end_date_event=modules.Notification.getEventDate()
        #if(start_date_event):
        print(start_date_event)
        print(modules.Notification.robot_status_list)




if __name__ == "__main__":
 log= Anomalies()
 log.startEvent