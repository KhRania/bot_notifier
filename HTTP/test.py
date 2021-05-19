#!/usr/bin/env python3

from errno import ENETUNREACH
import requests
from requests.exceptions import HTTPError
#dhooks is a library enables interact with discord webhooks  
from dhooks import Webhook, Embed
import datetime
import time
from dateutil import tz
import configuration as cfg
#schedule the run of the function 
import schedule 


class stateInformations:

    #set robot_status_list as a global array
    robot_status_list=[]
    #json content of state url
    list_state='{}'
    #WebHokk URL Provided By Discord (this url serve to communicate with Discord App)
    discord_channel=cfg.urls["webhookurl"]
    #urls contains the url of state from REST Server
    state_url=cfg.urls["stateurl"]
    #icons 
    robot_icon=''
    humidity_icon=''
    temperature_icon=''
    battery_icon=''
    free_disk_percentage_icon=''
        
    #Get the date and time from local to check with event in get request of schedule
    startDateNow= datetime.datetime.today().strftime('%Y-%m-%d')
    startTimeNow= datetime.datetime.now().time().strftime("%H:%M")

    
    def getStateURL(self):
      
        hook= Webhook(self.discord_channel)
        #The result of this test will be stored in scheduleRequest & state_request to do the treatment afterwards
        state_request=False
        
        #Test if the connection to /state is available
        if self.state_url :
            try:
                response = requests.get(self.state_url)

                # If the response was successful, no Exception will be raised
                response.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')  # Python 3.6
            except Exception as err:
                print(f'Other error occurred: {err}')  # Python 3.6
            #No Exception raised => Connection to the Rest Server with success    
            else:
                
                print('Success Connection To Rest Server!')
                state_request=True
                # extracting state data in json format
                self.list_state=requests.get(self.state_url).json()
                print (self.list_state)
                send_data=self.list_state
        return state_request
        
  

if __name__ == "__main__":    
    notif= stateInformations()
   
    schedule.every(30).seconds.do(notif.getStateURL)
    #While true repeat the execution of the function notificationsHook
    while True:

        schedule.run_pending()
        time.sleep(1) 
    


