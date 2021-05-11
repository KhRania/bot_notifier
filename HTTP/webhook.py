#!/usr/bin/env python3

from errno import ENETUNREACH
import requests
from requests.exceptions import HTTPError
#dhooks is a library enables interact with discord webhooks  
from dhooks import Webhook, Embed
import datetime
import time
import configuration as cfg
#schedule the run of the function 
from schedule import every, repeat, run_pending
#This array will save the different status of robot this will help to compare between the new status and the old one
robot_status_list=[]
notification=''

#@repeat is a decorator provide from schedule. In our case notificationsHook will be ran every 30 seconds
@repeat(every(30).seconds)
def notificationsHook():
    #set robot_status_list as a global array
    global robot_status_list
    #WebHokk URL Provided By Discord (this url serve to communicate with Discord App)
    hook= Webhook(cfg.urls["webhookurl"])
    #urls contains the url of state from REST Server
    url=cfg.urls["stateurl"]
    #The result of this test will be stored in scheduleRequest & state_request to do the treatment afterwards
    state_request=False
    
    #Test if the connection to /state is available
    if url :
        try:
            response = requests.get(url)

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
            

    if (state_request) :     
        calendar_image='https://img.icons8.com/color/48/000000/planner.png'
        # extracting state data in json format
        list_state=requests.get(cfg.urls["stateurl"]).json()
        #State MSG
        robot_state=':ballot_box_with_check:'
        humidity_state=':ballot_box_with_check:'
        temperature_state=':ballot_box_with_check:'
        battery_state=':ballot_box_with_check:'
        free_disk_percentage_state=':ballot_box_with_check:'
        #normal color msg blue
        color_msg=0x5CDBF0
        #Robot status
        robot_status=list_state['state']
        robot_status_list.append(robot_status)
        #Temperature Value
        temperature_value=list_state['sensors']['temperature']
        #Temperature Message send with the notification is empty when temperature_value is normal
        temperature_msg=''
        #humidity Value
        humidity_value=list_state['sensors']['humidity']
        #humidity Message send with the notification is empty when humidity_value is normal
        humidity_msg=''
        # battery percentage
        battery_percentage=round(float(list_state['battery']['percentage']*100),1)
        #battery Message send with the notification is empty when battery_percentage is normal
        battery_msg=''
        #Free Disk Storage percentage
        free_disk_percentage=round((float(list_state['storage']['free'])/float(list_state['storage']['total']))*100,1)
        #Total Disk Storage percentage
        total_percentage=round(float(list_state['storage']['total']),1)
        #free_disk Message send with the notification is empty when free_disk_percentage is normal
        free_disk_msg=''
        
       
        # Warning case if battery value < 0.2 msg for battery status switch to warning
        if list_state['battery']['percentage']< cfg.config['Settings']['battery']:
            battery_state=':no_entry_sign:'
            color_msg=0xFF8800
            battery_msg=' below  '+str(round(cfg.config['Settings']['battery']*100))+'%'

        # Warning case if free_disk_percentage < 20 % msg for battery status switch to warning
        if free_disk_percentage < round(cfg.config['Settings']['disk']*100,1):
            free_disk_percentage_state=':no_entry_sign:'
            color_msg=0xFF8800
            free_disk_msg=' below '+str(round(cfg.config['Settings']['disk']*100))+'%'

        #Warning Temperature 
        if temperature_value <= cfg.config['Settings']['temperature']['min']:
            temperature_state=':no_entry_sign:'
            color_msg=0xFF8800
            temperature_msg='below '+str(int(cfg.config['Settings']['temperature']['min']))+'C'
          
        elif temperature_value >= cfg.config['Settings']['temperature']['max']:
            temperature_state=':no_entry_sign:'
            color_msg=0xFF8800
            temperature_msg='above '+str(int(cfg.config['Settings']['temperature']['max']))+'C'
            
        #Warning Humidity
        if humidity_value <= cfg.config['Settings']['humidity']['min']:
            humidity_state=':no_entry_sign:'
            color_msg=0xFF8800
            humidity_msg='below '+str(int(cfg.config['Settings']['humidity']['min']))+'%'
        elif humidity_value >= cfg.config['Settings']['humidity']['max']:
            humidity_state=':no_entry_sign:'
            color_msg=0xFF8800
            humidity_msg='above '+str(int(cfg.config['Settings']['humidity']['max']))+'%'

        #Get the date and time from local to check with event in get request of schedule
        startDateNow= datetime.datetime.today().strftime('%Y-%m-%d')
        startTimeNow= datetime.datetime.now().time().strftime("%H:%M")
      
        # Test the Status if it FAILED the msg of th robot state is failed and the color is red 
        if list_state['state'].lower() == 'failure':
                robot_state=':no_entry_sign:'
                color_msg=0xF04747
        
        #test the length of the array to send the first notification     
        if (len(robot_status_list)==1):
            #Prepare notification content to send with Webhook                
            notification = Embed(

                                    description=robot_state+' : Robot state '+'**'+robot_status+'**'+'\n'+
                                    '\n'+
                                    battery_state+' : Battery state :battery: '+str(battery_percentage)+'% '+battery_msg+'\n'+
                                    '\n'+
                                    free_disk_percentage_state+' : Free storage :cd: '+str(free_disk_percentage)+'% '+free_disk_msg+'\n'+
                                    '\n'+
                                    temperature_state+' : Temperature :thermometer: '+str(temperature_value)+'C '+temperature_msg+'\n'+
                                    '\n'+
                                    humidity_state+' : Hydrometry :droplet: '+str(humidity_value)+'% '+humidity_msg,
                                    color=color_msg
                                    
                                    )

            notification.set_author(name='Date : '+startDateNow+' Time : '+startTimeNow, icon_url=calendar_image)
            #Send the Notification to Discord
            hook.send(embed=notification)
        #test if the old status is different to the new one in this case the length of the array must be greater than 1    
        elif ((len(robot_status_list)>1) and (robot_status!=robot_status_list[-2]))  :              
            #Prepare the notification to send with Webhook                
            notification = Embed(

                                    description=robot_state+' : Robot state '+'**'+robot_status+'**'+'\n'+
                                   '\n'+
                                    battery_state+' : Battery state :battery: '+str(battery_percentage)+'% '+battery_msg+'\n'+
                                    '\n'+
                                    free_disk_percentage_state+' : Free storage :cd: '+str(free_disk_percentage)+'% '+free_disk_msg+'\n'+
                                    '\n'+
                                    temperature_state+' : Temperature :thermometer: '+str(temperature_value)+'C '+temperature_msg+'\n'+
                                    '\n'+
                                    humidity_state+' : Hydrometry :droplet: '+str(humidity_value)+'% '+humidity_msg,
                                    color=color_msg
                                    
                                    )

            notification.set_author(name='Date : '+startDateNow+' Time : '+startTimeNow, icon_url=calendar_image)
            #Send the Notification to Discord
            hook.send(embed=notification)
            #to get only the last 2 elements of robot_status_list to avoid having an array with unlimited content
            robot_status_list=robot_status_list[-2:]
            
#While true repeat the execution of the function notificationsHook
while True:

    run_pending()
    time.sleep(1)       

                

