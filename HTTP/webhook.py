import requests
from requests.exceptions import HTTPError
from dhooks import Webhook, Embed
import datetime
import time
#schedule the run of the function 
from schedule import every, repeat, run_pending


#@repeat is a decorator provide from schedule. In our case notificationsHook will be ran every 1 minute
@repeat(every(1).minutes)
def notificationsHook():
    #WebHokk URL Provided By Discord (this url serve to communicate with Discord App)
    hook = Webhook("https://discord.com/api/webhooks/805752499293650945/yhXlvBIRuZufc4qKcalDzj-WzgWeLkaOxsqgWhNLKtv2KUOgKBwz6yHbFglkIgzZLzW0")
    #hook= Webhook("https://discord.com/api/webhooks/836258879519195166/o4HsziR7ZQ1tZD7aopXkn-VFp68aUsY91Lijl1QhnAJNh0rdMIp_6xOtaTBAYXr6Gzx6")
    #urlsRest contains the urls of schedule and state from REST Server
    urlsRest=['http://127.0.0.1:40054/schedule', 'http://127.0.0.1:40054/state']
    #The result of this test will be stored in scheduleRequest & stateRequest to do the treatment afterwards
    scheduleRequest=False
    stateRequest=False
    #Test if the connection to those urls is available
    for url in urlsRest:
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
            print('Success!')
            scheduleRequest=True
            stateRequest=True


    if (scheduleRequest and stateRequest)   :     
        # extracting schedule data in json format
        list_schedule = requests.get(urlsRest[0]).json()
        # extracting state data in json format
        list_state=requests.get(urlsRest[1]).json()
        #State MSG
        robot_state='**OK**'
        humidity_state='**OK**'
        temperature_state='**OK**'
        battery_state='**OK**'
        # battery percentage
        battery_percentage=int(list_state['battery']['percentage']*100)
        #Free Storage percentage
        free_percentage=round((float(list_state['storage_free'])/float(list_state['storage_total']))*100,1)
        #Total Storage percentage
        total_percentage=round(float(list_state['storage_total']),1)
        print(free_percentage)
        print(total_percentage)
        # Warning case if battery value < 0.4 msg for battery status switch to warning
        if list_state['battery']['percentage']<0.4:
            battery_state='**WARNING**'

    

        for event in list_schedule['scheduleData']:
                
                #Get the date and time from local to check with event in get request of schedule
                startDateNow= datetime.datetime.today().strftime('%Y-%m-%d')
                startTimeNow= datetime.datetime.now().time().strftime("%H:%M")
                print(startTimeNow)  
                # AUTOPILOT MSG
                #Check the start time and date pof the event with date and time now
                if(startDateNow == event['StartTime'][0:10] and startTimeNow == event['StartTime'][11:16]):

                        # Test the State if it is different for autopilot when start event then the msg is failed and the color is red 
                        if list_state['robot_state'].lower() == 'autopilot':
                            robot_state='**OK**'
                            color_msg=0x5CDBF0
                        else :
                            robot_state='**Failed**'
                            color_msg=0xF04747
                        
                        #Prepare the content to send with Webhook                
                        notification = Embed(

                            description=robot_state+' : Next start AUTOPILOT NOW END '+event['EndTime'][11:16]+'\n'+
                            robot_state+' : ROBOT STATUS switched to '+list_state['robot_state']+'\n'+
                            battery_state+' : Battery status '+str(battery_percentage)+' % minimum 40%'+'\n'+
                            'Temperature '+str(list_state['sensors']['temperature'])+' °C'+'\n'+
                            'Hydrometry '+str(list_state['sensors']['humidity'])+' %'+'\n'+
                            'Free Disk Storage '+str(free_percentage)+' %',
                            color=color_msg
                            
                            )

                        notification.set_author(name='Start Event Date : '+startDateNow+' Time : '+startTimeNow)
                        #Send the Autopilot Notification to Discord
                        hook.send(embed=notification)
                    
                #DOCKING MSG      
                if (startDateNow == event['StartTime'][0:10] and (event['StartTime'][11:16] < startTimeNow == event['EndTime'][11:16]) ):
                        
                         # Test the State if it is different for docking when start event then the msg is failed and the color is red 
                        if(list_state['robot_state'].lower() == 'docking'):
                                
                                robot_state='**OK**'
                                color_msg=0x5CDBF0
                            
                        else :
                                robot_state='**Failed**'
                                color_msg=0xF04747
                        #Prepare the content to send with Webhook  
                        notification = Embed(
                                        description=robot_state+' : Next start AUTOPILOT NOW'+'\n'+
                                        robot_state+' : ROBOT STATUS changed to '+list_state['robot_state']+'\n'+
                                        battery_state+' : Battery status '+str(battery_percentage)+' % minimum 40%'+'\n'+
                                        'Temperature '+str(list_state['sensors']['temperature'])+' °C'+'\n'+
                                        'Hydrometry '+str(list_state['sensors']['humidity'])+' %'+'\n'+
                                        'Free Disk Storage '+str(free_percentage)+' %',
                                        color=color_msg
                                            )

                        notification.set_author(name='End Event Date : '+startDateNow+' Time : '+startTimeNow)
                        #Send the Docking Notification to Discord
                        hook.send(embed=notification)    



#While true repeat the execution of the function notificationsHook
while True:

    run_pending()
    time.sleep(1)       

                

