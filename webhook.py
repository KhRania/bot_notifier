from dhooks import Webhook, Embed, File
import json
import os,sys
import datetime
import time
import threading
import re
import logging

#hook = Webhook("https://discord.com/api/webhooks/805752499293650945/yhXlvBIRuZufc4qKcalDzj-WzgWeLkaOxsqgWhNLKtv2KUOgKBwz6yHbFglkIgzZLzW0")
hook= Webhook("https://discord.com/api/webhooks/809051950389264394/CbfQ7MB1m1v7JAB68hZJzF0hqmzPOTZxnLqPcJRyt0-mvvrTCgpYA_h8kY_moadkag5X")
#image= os.path.join(os.path.expanduser('~'), 'tmp/image', '03-02-2021_09_00_00_quad2_screenshot.jpg')
schedule_json_file = os.path.join(os.path.expanduser('~'), 'tmp', 'schedule.json')
state_json_file =os.path.join(os.path.expanduser('~'), 'tmp', 'state.json')
sensors_config_file=os.path.join(os.path.expanduser('~'), 'tmp', 'config.js')


def notifications():
    data_now=[]
    data_next=[]
    event_nextTime=''
    event_nextDate=''
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('Webhook Script Started !')
    threading.Timer(60.0, notifications).start()
    #js = open(sensors_config_file, "r").readlines()
    
    
    #with open(sensors_config_file,'r') as f:
        #lines = f.readlines()
        #print(lines)
  

    file_schedule = open(schedule_json_file,)
    list_schedule = json.load(file_schedule) 

    file_state = open(state_json_file,)
    list_state = json.load(file_state)
   
    #State
    robot_state='**OK**'
    humidity_state='**OK**'
    temperature_state='**OK**'
    battery_state='**OK**'
    battery_percentage=int(list_state['battery']['percentage']*100)
    color_msg=0x5CDBF0
    
    
    if list_state['battery']['percentage']<0.4:
        battery_state='**WARNING**'


    if list_state['robot_state']!= 'AUTOPILOT':
        robot_state='**Failed**'
        color_msg=0xF04747
    
    
      
    for event in list_schedule['scheduleData']:
           
            startDateNow= datetime.datetime.today().strftime('%Y-%m-%d')
            startTimeNow= datetime.datetime.now().time().strftime("%H:%M")
            
            if(startDateNow == event['StartTime'][0:10]):
                
                if(startTimeNow < event['StartTime'][11:16]):
                    data_now.append(event['StartTime'][11:16])
                    data_now.sort()
                    event_nextTime=data_now[0]
                    event_nextDate=startDateNow
                    

            elif(startDateNow < event['StartTime'][0:10] and len(data_now)==0):
                    data_next.append(event['StartTime'])
                    data_next.sort()
                    event_nextTime=data_next[0][11:16]
                    event_nextDate=data_next[0][0:10]
                    

            if(startDateNow == event['StartTime'][0:10] and startTimeNow == event['StartTime'][11:16]):

                if event['Subject'] == 'AUTOPILOT':
                    
                    
                    notification = Embed(

                        description=robot_state+' : Next start AUTOPILOT NOW END '+event['EndTime'][11:16]+'\n'+
                        robot_state+' : ROBOT STATUS switched to '+list_state['robot_state']+'\n'+
                        battery_state+' : Battery status '+str(battery_percentage)+' % minimum 40%'+'\n'+
                        'Temperature '+str(list_state['sensors']['temperature'])+' °C'+'\n'+
                        'Hydrometry '+str(list_state['sensors']['humidity'])+' %',
                        color=color_msg
                        
                        )

                    notification.set_author(name='Date : '+startDateNow+' Time : '+startTimeNow)

                    hook.send(embed=notification)
                    logging.info('AUTOPILOT Notification sent !')
                    
                  
            if (startDateNow == event['StartTime'][0:10] and (event['StartTime'][11:16] < startTimeNow == event['EndTime'][11:16]) ):
                if(list_state['robot_state'].lower() == 'docked'):
                        
                        robot_state='**OK**'
                        notification = Embed(

                                description='Next start AUTOPILOT '+event_nextDate+' '+event_nextTime+'\n'+
                                robot_state+' : ROBOT STATUS switched to '+list_state['robot_state']+'\n'+
                                battery_state+' : Battery status '+str(battery_percentage)+' % minimum 40%'+'\n'+
                                'Temperature '+str(list_state['sensors']['temperature'])+' °C'+'\n'+
                                'Hydrometry '+str(list_state['sensors']['humidity'])+' %',
                                color=0x5CDBF0
                                
                                )

                        notification.set_author(name='Date : '+startDateNow+' Time : '+startTimeNow)

                        hook.send(embed=notification)
                        logging.info('DOCKED Notification sent !')

                      
                  
    #print(data_now)
    #print(data_next)

notifications()   


    
                
        