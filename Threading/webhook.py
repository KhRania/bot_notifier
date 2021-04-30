from dhooks import Webhook, Embed, File
import json
import os,sys
import datetime
import time
import threading
import re
import logging

#hook = Webhook("https://discord.com/api/webhooks/805752499293650945/yhXlvBIRuZufc4qKcalDzj-WzgWeLkaOxsqgWhNLKtv2KUOgKBwz6yHbFglkIgzZLzW0")
hook= Webhook("https://discord.com/api/webhooks/836258879519195166/o4HsziR7ZQ1tZD7aopXkn-VFp68aUsY91Lijl1QhnAJNh0rdMIp_6xOtaTBAYXr6Gzx6")
#image= os.path.join(os.path.expanduser('~'), 'tmp/image', '03-02-2021_09_00_00_quad2_screenshot.jpg')
schedule_json_file = os.path.join(os.path.expanduser('~'), 'tmp', 'schedule.json')
state_json_file =os.path.join(os.path.expanduser('~'), 'tmp', 'state.json')
sensors_config_file=os.path.join(os.path.expanduser('~'), 'tmp', 'config.js')


def notifications():
    data_now=[]
    data_next=[]
    #Time for the next event
    event_nextTime=''
    #Date for the next event
    event_nextDate=''
    #Threading Log
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
   
    #State MSG
    robot_state='**OK**'
    humidity_state='**OK**'
    temperature_state='**OK**'
    battery_state='**OK**'
    
    # battery percentage
    battery_percentage=int(list_state['battery']['percentage']*100)
    # Color for autopilot NORMAL MSG State
    color_msg=0x5CDBF0
    
    # Warning case if battery value < 0.4 msg for battery status switch to warning
    if list_state['battery']['percentage']<0.4:
        battery_state='**WARNING**'

    # Test the State if it is different for autopilot when start event then the msg is failed and the color is red 
    if list_state['robot_state'].upper()!= 'AUTOPILOT':
        robot_state='**Failed**'
        color_msg=0xF04747
    
    #this variable is for checking the state switched to Docking or not
    docking_state=False
    
    for event in list_schedule['scheduleData']:
            while (list_state['robot_state'].lower() == 'docking'):
                docking_state=True 
            #Get the dtae and time from local to check with event in schedule.json file
            startDateNow= datetime.datetime.today().strftime('%Y-%m-%d')
            startTimeNow= datetime.datetime.now().time().strftime("%H:%M")
            
            if(startDateNow == event['StartTime'][0:10]):
                # take all time values that have the same date and sort them to get a list
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

            #print(event_nextDate)
            #print(event_nextTime) 
            print(docking_state)       
            # AUTOPILOT MSG
            if(startDateNow == event['StartTime'][0:10] and startTimeNow == event['StartTime'][11:16]):

                if event['Subject'].upper() == 'AUTOPILOT':
                    
                    
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
                    logging.info('AUTOPILOT Notification Sent !')
                    
            #DOCKING MSG      
            if (startDateNow == event['StartTime'][0:10] and (event['StartTime'][11:16] < startTimeNow == event['EndTime'][11:16]) ):
                if(list_state['robot_state'].lower() == 'docking'):
                        
                        robot_state='**OK**'
                        color_msg=0x5CDBF0
                        docking_state=True 
                else :
                        robot_state='**Failed**'
                        color_msg=0xF04747
                notification = Embed(
                                description=robot_state+' : Next start AUTOPILOT NOW'+'\n'+
                                robot_state+' : ROBOT STATUS changed to '+list_state['robot_state']+'\n'+
                                battery_state+' : Battery status '+str(battery_percentage)+' % minimum 40%'+'\n'+
                                'Temperature '+str(list_state['sensors']['temperature'])+' °C'+'\n'+
                                'Hydrometry '+str(list_state['sensors']['humidity'])+' %',
                                color=color_msg
                                    )

                notification.set_author(name='Date : '+startDateNow+' Time : '+startTimeNow)

                hook.send(embed=notification)
                logging.info('DOCKING Notification Sent !')
               
           
                       
             
            #DOCKED MSG
            #To verify if the date and time for an event ae in the same date or for the case of midnight to take the state docked 
            if (docking_state and list_state['robot_state'].lower() == 'docked'): #and ((startDateNow==event_nextDate and startTimeNow < event_nextTime) or (startDateNow < event_nextDate))) :
                    
                notification = Embed(
                                    description='Next start AUTOPILOT '+event_nextDate+' '+event_nextTime+'\n'+
                                    '**OK**'+' : ROBOT STATUS switched to '+list_state['robot_state']+'\n'+
                                    battery_state+' : Battery status '+str(battery_percentage)+' % minimum 40%'+'\n'+
                                    'Temperature '+str(list_state['sensors']['temperature'])+' °C'+'\n'+
                                    'Hydrometry '+str(list_state['sensors']['humidity'])+' %',
                                    color=0x5CDBF0
                                    )
                notification.set_author(name='Date : '+startDateNow+' Time : '+startTimeNow)
                hook.send(embed=notification)
                docking_state=False
                logging.info('DOCKED Notification Sent !')
                       
                
                    
            
             
                     
                  


notifications()   


    
                
        