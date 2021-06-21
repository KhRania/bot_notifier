from modules import Notification
#schedule the run of the function 
import schedule 
import time
from dhooks import Webhook, Embed, File
import configuration as cfg
import requests
from io import BytesIO,StringIO
import logging

logging.basicConfig(level=logging.INFO)

#set robot_status_list as a global array
robot_status_list=[]
#WebHokk URL Provided By Discord (this url serve to communicate with Discord App)
discord_channel=Webhook(cfg.urls["webhookurl"])
#state_url contains the url of state from REST Server
state_url=cfg.urls["stateurl"]
#settings_url contains the url of state from REST Server
settings_url=cfg.urls["settingsurl"]
notif= Notification()
robot_status_list=[]


def StartEndEvent():
    global robot_status_list
    #get responses from /state 
    state_request,list_state=notif.getResponseState()
    #get date of event
    start_date_event,end_date_event=notif.getEventDate()
    #get time of event
    start_time_event,end_time_event=notif.getEventTime()
    startDateNow,startTimeNow=notif.getNow()
    robot_status=''
    if(state_request):
        #get last two states
        robot_status=list_state['state']
        robot_status_list.append(robot_status)
        #to get only the last 2 elements of robot_status_list to avoid having an array with unlimited content
        robot_status_list=robot_status_list[-2:]  
        #for start event normal case last state = docked switched to autopilot and current events are available
        if robot_status_list[0].lower() == 'docked':
            if robot_status_list[1].lower() != 'autopilot' and start_date_event and start_time_event:
                notification = Embed(description='**Start of event failed, robot state is '+robot_status_list[1]+'**',color=0xF04747)
                discord_channel.send(embed=notification)

        #for end event normal case last state = autopilot switched to docking 
        if robot_status_list[0].lower() == 'autopilot':
            if  robot_status_list[1].lower() != 'docking' and len(list_state['current_events'])==0:
                notification = Embed(description='**End of event failed, robot state is '+robot_status_list[1]+'**',color=0xF04747)
                discord_channel.send(embed=notification) 

       
schedule.every(30).seconds.do(StartEndEvent)
    
while True:
    try:
      
        schedule.run_pending()
        time.sleep(1)
    except Exception as err:
        logging.warning(f'Other error occurred: {err}')  # Python 3.6