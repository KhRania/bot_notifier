#!/usr/bin/env python3

import discord
import configuration as cfg
import requests
from requests.exceptions import HTTPError
import schedule
import time
import datetime
from keep_alive import keep_alive

client = discord.Client()


#Test if the connection to /state is available
#urls contains the url of state from REST Server
url=cfg.urls["stateurl"]
#The result of this test will be stored in scheduleRequest & state_request to do the treatment afterwards
def getUrl():
    robot_status_list=[]
    notification_msg=''
    color_msg=''
    state_request=False
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
                    # extracting state data in json format
        list_state=requests.get(url).json()

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
          battery_state='⚠️'
          color_msg=0xFF8800
          battery_msg=' below  '+str(round(cfg.config['Settings']['battery']*100))+'%'

                    # Warning case if free_disk_percentage < 20 % msg for battery status switch to warning
        if free_disk_percentage < round(cfg.config['Settings']['disk']*100,1):
          free_disk_percentage_state='⚠️'
          color_msg=0xFF8800
          free_disk_msg=' below '+str(round(cfg.config['Settings']['disk']*100))+'%'

                    #Warning Temperature 
        if temperature_value <= cfg.config['Settings']['temperature']['min']:
          temperature_state='⚠️'
          color_msg=0xFF8800
          temperature_msg='below '+str(int(cfg.config['Settings']['temperature']['min']))+'°C'
                      
        elif temperature_value >= cfg.config['Settings']['temperature']['max']:
          temperature_state='⚠️'
          color_msg=0xFF8800
          temperature_msg='above '+str(int(cfg.config['Settings']['temperature']['max']))+'°C'
                        
                    #Warning Humidity
        if humidity_value <= cfg.config['Settings']['humidity']['min']:
          humidity_state='⚠️'
          color_msg=0xFF8800
          humidity_msg='below '+str(int(cfg.config['Settings']['humidity']['min']))+'%'
        elif humidity_value >= cfg.config['Settings']['humidity']['max']:
          humidity_state='⚠️'
          color_msg=0xFF8800
          humidity_msg='above '+str(int(cfg.config['Settings']['humidity']['max']))+'%'

                    #Get the date and time from local to check with event in get request of schedule
                    #startDateNow= datetime.datetime.today().strftime('%Y-%m-%d')
                    #startTimeNow= datetime.datetime.now().time().strftime("%H:%M")
                  
                    # Test the Status if it FAILED or EMERGENCY the msg of th robot state is failed and the color is red 
        if list_state['state'].lower() == 'failure' or list_state['state'].lower() == 'emergency':
          robot_state='⚠️'
          color_msg=0xF04747

                    #test the length of the array to send the first notification     
        if (len(robot_status_list)==1):
            if(len(list_state['current_events'])==1):
                            
                            # utc = datetime.utcnow()
              end_time_event_utc = datetime.datetime.strptime(list_state['current_events'][0]['stop'], '%Y-%m-%d %H:%M:%S')
              local_time= end_time_event_utc.time()
              now_timestamp = time.time()
              offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
              end_time_event_local =str((datetime.datetime.combine(datetime.date(1,1,1),local_time) + offset).time())
              notification_msg=robot_state+' : Next start '+'**'+robot_status+'**'+' now end '+end_time_event_local[:5]+'\n'+'\n'+battery_state+' : Battery state :battery: '+str(battery_percentage)+'% '+battery_msg+'\n'+'\n'+free_disk_percentage_state+' : Free storage :cd: '+str(free_disk_percentage)+'% '+free_disk_msg+'\n'+'\n'+temperature_state+' : Temperature :thermometer: '+str(temperature_value)+'°C '+temperature_msg+'\n'+'\n'+humidity_state+' : Humidity :droplet: '+str(humidity_value)+'% '+humidity_msg

                          
            else:
              notification_msg=robot_state+' : Robot state '+'**'+robot_status+'**'+'\n'+'\n'+battery_state+' : Battery state :battery: '+str(battery_percentage)+'% '+battery_msg+'\n'+'\n'+free_disk_percentage_state+' : Free storage :cd: '+str(free_disk_percentage)+'% '+free_disk_msg+'\n'+'\n'+temperature_state+' : Temperature :thermometer: '+str(temperature_value)+'°C '+temperature_msg+'\n'+'\n'+humidity_state+' : Humidity :droplet: '+str(humidity_value)+'% '+humidity_msg

                            

                    #test if the old status is different to the new one in this case the length of the array must be greater than 1    
        elif ((len(robot_status_list)>1) and (robot_status!=robot_status_list[-2]))  :
            if(len(list_state['current_events'])==1):
                            
                            # utc = datetime.utcnow()
              end_time_event_utc = datetime.datetime.strptime(list_state['current_events'][0]['stop'], '%Y-%m-%d %H:%M:%S')
              local_time= end_time_event_utc.time()
              now_timestamp = time.time()
              offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
              end_time_event_local =str((datetime.datetime.combine(datetime.date(1,1,1),local_time) + offset).time())
                            #Prepare notification content to send with Webhook 
              notification_msg=robot_state+' : Next start '+'**'+robot_status+'**'+' now end '+end_time_event_local[:5]+'\n'+'\n'+battery_state+' : Battery state :battery: '+str(battery_percentage)+'% '+battery_msg+'\n'+'\n'+free_disk_percentage_state+' : Free storage :cd: '+str(free_disk_percentage)+'% '+free_disk_msg+'\n'+'\n'+temperature_state+' : Temperature :thermometer: '+str(temperature_value)+'°C '+temperature_msg+'\n'+'\n'+humidity_state+' : Humidity :droplet: '+str(humidity_value)+'% '+humidity_msg

            else:
              notification_msg=robot_state+' : Robot state '+'**'+robot_status+'**'+'\n'+'\n'+battery_state+' : Battery state :battery: '+str(battery_percentage)+'% '+battery_msg+'\n'+'\n'+free_disk_percentage_state+' : Free storage :cd: '+str(free_disk_percentage)+'% '+free_disk_msg+'\n'+'\n'+temperature_state+' : Temperature :thermometer: '+str(temperature_value)+'°C '+temperature_msg+'\n'+'\n'+humidity_state+' : Humidity :droplet: '+str(humidity_value)+'% '+humidity_msg
                            
                      
                        #to get only the last 2 elements of robot_status_list to avoid having an array with unlimited content
        robot_status_list=robot_status_list[-2:]
    
    return notification_msg,color_msg,state_request



#register an event 
#discrod.py is an async library to manage thinks it will be by callbacks 
#this func will be called when the bot it will be used
@client.event
async def on_ready():
  print('We have logged in Discord Server as {0.user}'.format(client))


#when  receive message
@client.event
async def on_message(message):
  
  # we do not want the bot to reply to itself
  if message.author == client.user:
    print('User sends a msg')
  if message.content.startswith('!notify'):
    #Get the date and time from local to check with event in get request of schedule
    startDateNow= datetime.datetime.today().strftime('%Y-%m-%d')
    startTimeNow= datetime.datetime.now().time().strftime("%H:%M")
    notification,color,status_request=getUrl()
    if notification and status_request==True:
      embedVar = discord.Embed(title='Date : '+startDateNow+' Time : '+startTimeNow, description=notification ,color=color)   
      await message.channel.send(embed=embedVar)
    if status_request== False:
      embedVar = discord.Embed(description=":loudspeaker: ** No notification to send problem with REST server**" ,color=0xc0c6c8 )   
      await message.channel.send(embed=embedVar)
     
    



#new member join the server    
@client.event
async def on_member_join(member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f'Welcome {member.mention} to {guild.name}!'
            await guild.system_channel.send(to_send)
            print("hi !")



keep_alive()
client.run(cfg.urls["token"])

    