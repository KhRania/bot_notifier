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
docked_state_list=[]
autopilot_state_list=[]
dateEvent=[]


def StartEndEventLog():

    global robot_status_list,dateEvent
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
        robot_status=list_state['state'].lower()
        robot_status_list.append(robot_status)
        #get the end of event (time/date) cause after each get the data will be deleted and we need those values in end event treatement
        if len(list_state['current_events'])==1 and len(dateEvent)==0 :
            dateEvent.append(end_date_event)
            dateEvent.append(end_time_event)

        #for start event normal case last state = docked switched to autopilot and current events are available
        if robot_status_list[-2] == 'docked':
            #anomalie
            if robot_status_list[-1] != 'autopilot' and start_date_event and end_date_event  and len(list_state['current_events'])==1:
                notification = Embed(description='** Failed Start Event '+start_date_event+' '+start_time_event+' , Robot state is '+robot_status_list[-1]+'**',color=0xF04747)
                discord_channel.send(embed=notification)
            #normal    
            if robot_status_list[-1] == 'autopilot' and start_date_event and end_date_event and len(list_state['current_events'])==1:
                notification = Embed(description='** Success Start Event '+start_date_event+' '+start_time_event+' the robot starts its patrol**',color=0x5CDBF0)
                discord_channel.send(embed=notification)

        #for end event normal case last state = autopilot switched to docking 
        if robot_status_list[-2] == 'autopilot' and len(dateEvent)==2:
            #anomalie
            if  robot_status_list[-1] != 'docking' and len(list_state['current_events'])==0:
              
                notification = Embed(description='** Failed End Event '+dateEvent[0] +' '+dateEvent[1]+' . Robot state is '+robot_status_list[-1]+'**',color=0xF04747)
                discord_channel.send(embed=notification) 
                dateEvent=[]
            #normal
            if  robot_status_list[-1] == 'docking' and list_state['patrol']['active']== False:
                notification = Embed(description='** Success End Event '+dateEvent[0] +' '+dateEvent[1]+' . Returning to the charging base. **',color=0x5CDBF0)
                discord_channel.send(embed=notification) 
                dateEvent=[]
        #to get only the last 2 elements of robot_status_list to avoid having an array with unlimited content
        robot_status_list=robot_status_list[-2:] 
    

#log start from docking status
def baseLog():

    global docked_state_list
    #get responses from /state 
    state_request,list_state=notif.getResponseState()
    robot_status=''
    status=False
    if(state_request):
        #get last status
        robot_status=list_state['state'].lower()
       
        #set docking state as the first element in the array
        if (robot_status== 'docking' or robot_status== 'starting') and list_state['patrol']['active']==False:
            if len(docked_state_list)== 0 :
                docked_state_list.append(robot_status)
            else:
                docked_state_list=[]
                docked_state_list.append(robot_status)
        else:
            if robot_status!=docked_state_list[-1]:

                docked_state_list.append(robot_status)
            else:
                status=True

        #Treatement after docking/starting state starting is taken the first element in the array case the robot will reboot and all variables will reset
        if (docked_state_list[0]=='docking' or docked_state_list[0]=='starting') and len(docked_state_list)> 0:
            print(docked_state_list)
            #Manual return to base
            if docked_state_list[-1]=='manual' and status==False:

                notification = Embed(description='** Problem returning to the charging base. MANUAL RETURN.**',color=0xF04747)
            #Failure return to base    
            elif docked_state_list[-1]=='failure' and status==False:
                notification = Embed(description='** Problem returning to the charging base.**',color=0xF04747)
             
            #sur la base    
            elif docked_state_list[-1]=='docked' and status==False:
                if list_state['sensors']['docking']== True:
                    notification = Embed(description='** Success returning to the charging base.**',color=0x5CDBF0)
                else:
                    notification = Embed(description='** The robot is not well placed on the charging base**',color=0xF04747)


        discord_channel.send(embed=notification)             

#log au cours de l'event
def eventLog():

    global autopilot_state_list
    #get responses from /state 
    state_request,list_state=notif.getResponseState()
    robot_status=''
    status=False
    if(state_request):
        #get last status
        robot_status=list_state['state'].lower()
        #set autopilot state as the first element in the array when the patrol is active and there is a current event
        if robot_status== 'autopilot' and list_state['patrol']['active']==True and len(list_state['current_events'])==1:
            if len(docked_state_list)== 0 :
                docked_state_list.append(robot_status)
            else:
                docked_state_list=[]
                docked_state_list.append(robot_status)
        else:
            if robot_status!=docked_state_list[-1]:

                docked_state_list.append(robot_status)
            else:
                status=True







       










schedule.every(30).seconds.do(StartEndEventLog)
schedule.every(30).seconds.do(baseLog)
    
while True:
    try:
      
        schedule.run_pending()
        time.sleep(1)
    except Exception as err:
        logging.warning(f'Other error occurred: {err}')  # Python 3.6