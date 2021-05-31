#!/usr/bin/env python3
from errno import ENETUNREACH
import requests
from requests.exceptions import HTTPError
#dhooks is a library enables interact with discord webhooks  
from dhooks import Webhook, Embed, File
import datetime
import time
from dateutil import tz
import configuration as cfg



class Notification:

    #set robot_status_list as a global array
    robot_status_list=[]
    #WebHokk URL Provided By Discord (this url serve to communicate with Discord App)
    discord_channel=Webhook(cfg.urls["webhookurl"])
    #urls contains the url of state from REST Server
    state_url=cfg.urls["stateurl"]
    #urls contains the url of state from REST Server
    screenshot_url=cfg.urls["screenshoturl"]



    def getRequestURL(self):
        list_state='{}'
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
                
                state_request=True
                # extracting state data in json format
                list_state=requests.get(self.state_url).json()
        return state_request,list_state

    def batteryMessage(self):
        battery_msg=''
        #normal color msg blue
        color_msg=0x5CDBF0
        state_request,list_state=self.getRequestURL()
        if(state_request):
            # battery percentage
            battery_percentage=round(float(list_state['battery']['percentage']*100),1)
            #icon if value normal
            battery_state=':ballot_box_with_check:'
            #battery Message send with the notification is empty when battery_percentage is normal
            battery_msg=battery_state+' : Battery state :battery: '+str(battery_percentage)+'% '
         
            # Warning case if battery value < 0.2 msg for battery status switch to warning
            if list_state['battery']['percentage']< cfg.config['Settings']['battery']:
                battery_state='⚠️'
                color_msg=0xFF8800
                battery_msg=battery_state+' : Battery state :battery: '+str(battery_percentage)+'% '+'below  '+str(round(cfg.config['Settings']['battery']*100))+'%'
        
        return battery_msg,color_msg
    
    def storageMessage(self):
        free_disk_msg=''
        #normal color msg blue
        color_msg=0x5CDBF0
        state_request,list_state=self.getRequestURL()
        if(state_request):
            #icon if value normal
            free_disk_percentage_state=':ballot_box_with_check:'
            #Free Disk Storage percentage
            free_disk_percentage=round((float(list_state['storage']['free'])/float(list_state['storage']['total']))*100,1)
            #free_disk Message send with the notification is empty when free_disk_percentage is normal
            free_disk_msg=free_disk_percentage_state+' : Free storage :cd: '+str(free_disk_percentage)+'% '
            # Warning case if free_disk_percentage < 20 % msg for battery status switch to warning
            if free_disk_percentage < round(cfg.config['Settings']['disk']*100,1):
                free_disk_percentage_state='⚠️'
                color_msg=0xFF8800
                free_disk_msg=free_disk_percentage_state+' : Free storage :cd: '+str(free_disk_percentage)+'% '+'below '+str(round(cfg.config['Settings']['disk']*100))+'%'
        return free_disk_msg,color_msg

    def temperatureMessage(self):
        temperature_msg=''
        #normal color msg blue
        color_msg=0x5CDBF0
        state_request,list_state=self.getRequestURL()
        if(state_request):
            #icon if value normal
            temperature_state=':ballot_box_with_check:'
            #Temperature Value
            temperature_value=list_state['sensors']['temperature']
            #Temperature Message send with the notification is empty when temperature_value is normal
            temperature_msg=temperature_state+' : Temperature :thermometer: '+str(temperature_value)+'°C '
             #Warning Temperature 
            if temperature_value <= cfg.config['Settings']['temperature']['min']:
                temperature_state='⚠️'
                color_msg=0xFF8800
                temperature_msg=temperature_state+' : Temperature :thermometer: '+str(temperature_value)+'°C below '+str(int(cfg.config['Settings']['temperature']['min']))+'°C'
            elif temperature_value >= cfg.config['Settings']['temperature']['max']:
                temperature_state='⚠️'
                color_msg=0xFF8800
                temperature_msg=temperature_state+' : Temperature :thermometer: '+str(temperature_value)+'°C above '+str(int(cfg.config['Settings']['temperature']['max']))+'°C'
        
        return temperature_msg,color_msg


    def humidityMessage(self):
        humidity_msg=''
        #normal color msg blue
        color_msg=0x5CDBF0
        state_request,list_state=self.getRequestURL()
        if(state_request):
            #icon if value normal
            humidity_state=':ballot_box_with_check:'
            #humidity Value
            humidity_value=list_state['sensors']['humidity']
            #humidity Message send with the notification is empty when humidity_value is normal
            humidity_msg=humidity_state+' : Humidity :droplet: '+str(humidity_value)+'% '
            #Warning Humidity
            if humidity_value <= cfg.config['Settings']['humidity']['min']:
                humidity_state='⚠️'
                color_msg=0xFF8800
                humidity_msg=humidity_state+' : Humidity :droplet: '+str(humidity_value)+'%'+' below '+str(int(cfg.config['Settings']['humidity']['min']))+'%'
            elif humidity_value >= cfg.config['Settings']['humidity']['max']:
                humidity_state='⚠️'
                color_msg=0xFF8800
                humidity_msg=humidity_state+' : Humidity :droplet: '+str(humidity_value)+'%'+' above '+str(int(cfg.config['Settings']['humidity']['max']))+'%'
        return humidity_msg,color_msg

    #Get the date and time from local to check with event in get request of schedule
    def getNow(self):
        #Get the date and time from local to check with event in get request of schedule
        startDateNow= datetime.datetime.today().strftime('%Y-%m-%d')
        startTimeNow= datetime.datetime.now().time().strftime("%H:%M")
        return startDateNow,startTimeNow

    #convert time of event in /state
    def getEventTime(self):

        start_time_event_local = ''
        end_time_event_local = ''
        state_request,list_state=self.getRequestURL()
        if(state_request):
            if(len(list_state['current_events'])==1):

                now_timestamp = time.time()
                offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
                #time start event
                start_time_event_utc = datetime.datetime.strptime(list_state['current_events'][0]['start'], '%Y-%m-%d %H:%M:%S')
                start_local_time = start_time_event_utc.time()
                start_time_event_local = str((datetime.datetime.combine(datetime.date(1,1,1),start_local_time) + offset).time())
                start_time_event_local = start_time_event_local[:5]
                #time end event
                end_time_event_utc = datetime.datetime.strptime(list_state['current_events'][0]['stop'], '%Y-%m-%d %H:%M:%S')
                end_local_time = end_time_event_utc.time()
                end_time_event_local = str((datetime.datetime.combine(datetime.date(1,1,1),end_local_time) + offset).time())
                end_time_event_local = end_time_event_local[:5]
            
            else:
                pass
        return start_time_event_local,end_time_event_local

    #convert time of event in /state
    def getEventDate(self):
        
        start_date_event_local  = ''
        end_date_event_local    = ''

        state_request,list_state=self.getRequestURL()
        if(state_request):
            if(len(list_state['current_events'])==1):
                start_date_event_local  = list_state['current_events'][0]['start'][:11]
                end_date_event_local    = list_state['current_events'][0]['stop'][:11]
            else:
                pass
        return start_date_event_local,end_date_event_local
            


    def msgWebhook(self):
        #normal color msg blue
        color_msg=0x5CDBF0
        notification_msg=''
        try:
            battery_msg,colorB=self.batteryMessage()
            free_disk_msg,colorS=self.storageMessage()
            temperature_msg,colorT=self.temperatureMessage()
            humidity_msg,colorH=self.humidityMessage()
            color_warning=0xFF8800
            #list color to choose the color of the notification to send
            for color_warning in [colorB,colorS,colorT,colorH]:
                color_msg= color_warning
            #icon calendar to be added in the notification to send
            calendar=':calendar_spiral:'
            dateNow,timeNow=self.getNow()
            startTime,endTime=self.getEventTime()
            startDate,endDate=self.getEventDate()
            #State icon for normal state ( ex: AUTOPILOT)
            robot_state=':ballot_box_with_check:'
            state_request,list_state=self.getRequestURL()
            if(state_request):
                print('Success Connection To Rest Server!')
                #Robot status
                robot_status=list_state['state']
                self.robot_status_list.append(robot_status)
                # Test the Status if it FAILED or EMERGENCY the msg of th robot state is failed and the color is red 
                if list_state['state'].lower() == 'failure' or list_state['state'].lower() == 'emergency':
                        robot_state='⚠️'
                        color_msg=0xF04747
                #test the length of the array to send the first notification     
                if (len(self.robot_status_list)==1):
                    if(startTime and endTime and startDate and endDate):
                        #Prepare notification content to send with Webhook
                        notification_msg=calendar+' : Start Event '+'**'+startDate+'**'+' Time '+'**'+startTime+'**'+'\n'+'\n'+calendar+' : End Event '+'**'+endDate+'**'+' Time '+'**'+endTime+'**'+'\n'+'\n'+robot_state+' : Robot state '+'**'+robot_status+'**'+'\n'+'\n'+battery_msg+'\n'+'\n'+free_disk_msg+'\n'+'\n'+temperature_msg+'\n'+'\n'+humidity_msg
                    else:
                        notification_msg=calendar+' ** Date :** '+'**'+dateNow+'**'+' **Time ** '+'**'+timeNow+'**'+'\n'+'\n'+robot_state+' : Robot state '+'**'+robot_status+'**'+'\n'+'\n'+battery_msg+'\n'+'\n'+free_disk_msg+'\n'+'\n'+temperature_msg+'\n'+'\n'+humidity_msg

                #test if the old status is different to the new one in this case the length of the array must be greater than 1    
                elif ((len(self.robot_status_list)>1) and (robot_status!=self.robot_status_list[-2]))  :
                    if(startTime and endTime and startDate and endDate):
                        #Prepare notification content to send with Webhook 
                        notification_msg=calendar+' : Start Event '+'**'+startDate+'**'+' Time '+'**'+startTime+'**'+'\n'+'\n'+calendar+' : End Event '+'**'+endDate+'**'+' Time '+'**'+endTime+'**'+'\n'+'\n'+robot_state+' : Robot state '+'**'+robot_status+'**'+'\n'+'\n'+battery_msg+'\n'+'\n'+free_disk_msg+'\n'+'\n'+temperature_msg+'\n'+'\n'+humidity_msg
                    else:
                        notification_msg=calendar+' ** Date :** '+'**'+dateNow+'**'+' **Time ** '+'**'+timeNow+'**'+'\n'+'\n'+robot_state+' : Robot state '+'**'+robot_status+'**'+'\n'+'\n'+battery_msg+'\n'+'\n'+free_disk_msg+'\n'+'\n'+temperature_msg+'\n'+'\n'+humidity_msg
                #to get only the last 2 elements of robot_status_list to avoid having an array with unlimited content
                self.robot_status_list=self.robot_status_list[-2:]
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        return notification_msg,color_msg         
    

    def stateMessage(self):
        #normal color msg blue
        color_msg=0x5CDBF0
        state_msg=''
        try:
           
            #icon calendar to be added in the notification to send
            calendar=':calendar_spiral:'
            dateNow,timeNow=self.getNow()
            startTime,endTime=self.getEventTime()
            startDate,endDate=self.getEventDate()
            #State icon for normal state ( ex: AUTOPILOT)
            robot_state=':ballot_box_with_check:'
            state_request,list_state=self.getRequestURL()
            if(state_request):
                
                #Robot status
                robot_status=list_state['state']
                # Test the Status if it FAILED or EMERGENCY the msg of th robot state is failed and the color is red 
                if list_state['state'].lower() == 'failure' or list_state['state'].lower() == 'emergency':
                        robot_state='⚠️'
                        color_msg=0xF04747
               
                if(startTime and endTime and startDate and endDate):
                        #Prepare notification content to send with Webhook
                        state_msg=calendar+' : Start Event '+'**'+startDate+'**'+' Time '+'**'+startTime+'**'+'\n'+'\n'+calendar+' : End Event '+'**'+endDate+'**'+' Time '+'**'+endTime+'**'+'\n'+'\n'+robot_state+' : Robot state '+'**'+robot_status+'**'
                
                else:
                        state_msg=calendar+' ** Date :** '+'**'+dateNow+'**'+' **Time ** '+'**'+timeNow+'**'+'\n'+'\n'+robot_state+' : Robot state '+'**'+robot_status+'**'

        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        return state_msg,color_msg 


    def msgNotify(self):
        #normal color msg blue
        color_msg=0x5CDBF0
        notification_msg=''
        try:
            
            battery_msg,colorB=self.batteryMessage()
            free_disk_msg,colorS=self.storageMessage()
            temperature_msg,colorT=self.temperatureMessage()
            humidity_msg,colorH=self.humidityMessage()
            color_warning=0xFF8800
            #list color to choose the color of the notification to send
            for color_warning in [colorB,colorS,colorT,colorH]:
                color_msg= color_warning
            #icon calendar to be added in the notification to send
            calendar=':calendar_spiral:'
            dateNow,timeNow=self.getNow()
            startTime,endTime=self.getEventTime()
            startDate,endDate=self.getEventDate()
            #State icon for normal state ( ex: AUTOPILOT)
            robot_state=':ballot_box_with_check:'
            state_request,list_state=self.getRequestURL()
            if(state_request):
                
                #Robot status
                robot_status=list_state['state']
                # Test the Status if it FAILED or EMERGENCY the msg of th robot state is failed and the color is red 
                if list_state['state'].lower() == 'failure' or list_state['state'].lower() == 'emergency':
                        robot_state='⚠️'
                        color_msg=0xF04747
               
                if(startTime and endTime and startDate and endDate):
                        #Prepare notification content to send with Webhook
                        notification_msg=calendar+' : Start Event '+'**'+startDate+'**'+' Time '+'**'+startTime+'**'+'\n'+'\n'+calendar+' : End Event '+'**'+endDate+'**'+' Time '+'**'+endTime+'**'+'\n'+'\n'+robot_state+' : Robot state '+'**'+robot_status+'**'+'\n'+'\n'+battery_msg+'\n'+'\n'+free_disk_msg+'\n'+'\n'+temperature_msg+'\n'+'\n'+humidity_msg
                
                else:
                        notification_msg=calendar+' ** Date :** '+'**'+dateNow+'**'+' **Time ** '+'**'+timeNow+'**'+'\n'+'\n'+robot_state+' : Robot state '+'**'+robot_status+'**'+'\n'+'\n'+battery_msg+'\n'+'\n'+free_disk_msg+'\n'+'\n'+temperature_msg+'\n'+'\n'+humidity_msg

        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        return notification_msg,color_msg 


    def postWebhook(self):
      
        body_msg,color_msg=self.msgWebhook()
        screenshot_request,list_screenshot=self.screenshot() 
        screenshot=list_screenshot[-3] 
        file = File('/home/rania/Pictures/Docking_Capture.png', name='quad2.png') 
       
       
        if body_msg:
            #Prepare notification content to send with Webhook                
            notification = Embed(description=body_msg,color=color_msg)
            #notification.set_image(screenshot)
       
            #Send the Notification to Discord
            self.discord_channel.send(embed=notification)
            self.discord_channel.send('Look at this:', file=file)
            print("Webhook sent !")

        else:
            print("Nothing to send !")

    def screenshot(self):
        list_screenshot='{}'

        #The result of this test will be stored in scheduleRequest & state_request to do the treatment afterwards
        screenshot_request=False
        
        #Test if the connection to /state is available
        if self.screenshot_url :
            try:
                response = requests.get(self.screenshot_url)

                # If the response was successful, no Exception will be raised
                response.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')  # Python 3.6
            except Exception as err:
                print(f'Other error occurred: {err}')  # Python 3.6
            #No Exception raised => Connection to the Rest Server with success    
            else:
                
                screenshot_request=True
                # extracting state data in json format
                list_screenshot=requests.get(self.screenshot_url).json()
        return screenshot_request,list_screenshot