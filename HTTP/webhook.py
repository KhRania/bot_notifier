import requests
from requests.exceptions import HTTPError
from dhooks import Webhook, Embed
import datetime
import time
#schedule the run of the function 
from schedule import every, repeat, run_pending
#This array will save the different status of robot this will help to compare between the new status and the old one
robot_status_list=[]
#@repeat is a decorator provide from schedule. In our case notificationsHook will be ran every 30 seconds
@repeat(every(30).seconds)
def notificationsHook():
    #WebHokk URL Provided By Discord (this url serve to communicate with Discord App)
    #hook = Webhook("https://discord.com/api/webhooks/805752499293650945/yhXlvBIRuZufc4qKcalDzj-WzgWeLkaOxsqgWhNLKtv2KUOgKBwz6yHbFglkIgzZLzW0")
    hook= Webhook("https://discord.com/api/webhooks/836258879519195166/o4HsziR7ZQ1tZD7aopXkn-VFp68aUsY91Lijl1QhnAJNh0rdMIp_6xOtaTBAYXr6Gzx6")
    #urls contains the url of state from REST Server
    url= 'http://127.0.0.1:40054/state'
    #The result of this test will be stored in scheduleRequest & stateRequest to do the treatment afterwards
    stateRequest=False
    
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
            stateRequest=True

    if (stateRequest) :     
        
        # extracting state data in json format
        list_state=requests.get(url).json()
        #State MSG
        robot_state='**OK**'
        humidity_state='**OK**'
        temperature_state='**OK**'
        battery_state='**OK**'
        free_percentage_state='**OK**'
        #normal color msg
        color_msg=0x5CDBF0
        #Robot status
        robot_status=list_state['robot_state']
        robot_status_list.append(robot_status)
        # battery percentage
        battery_percentage=int(list_state['battery']['percentage']*100)
        #Free Storage percentage
        free_percentage=round((float(list_state['storage_free'])/float(list_state['storage_total']))*100,1)
        #Total Storage percentage
        total_percentage=round(float(list_state['storage_total']),1)
        print(robot_status_list)
       
        # Warning case if battery value < 0.4 msg for battery status switch to warning
        if list_state['battery']['percentage']<0.4:
            battery_state='**WARNING**'
            color_msg=0xF04747
         # Warning case if free_percentage < 20% msg for battery status switch to warning
        if free_percentage < 0.2:
            free_percentage_state='**WARNING**'
            color_msg=0xF04747
        #Get the date and time from local to check with event in get request of schedule
        startDateNow= datetime.datetime.today().strftime('%Y-%m-%d')
        startTimeNow= datetime.datetime.now().time().strftime("%H:%M")
      
        # Test the Status if it FAILED the msg of th robot state is failed and the color is red 
        if list_state['robot_state'].lower() == 'failed':
                robot_state='**Failed**'
                color_msg=0xF04747
        
        #test the length of the array to send the first notification     
        if (len(robot_status_list)==1):
            #Prepare the content to send with Webhook                
            notification = Embed(

                                    description=robot_state+' : ROBOT STATUS '+robot_status+'\n'+
                                    battery_state+' : Battery status '+str(battery_percentage)+' % minimum 40%'+'\n'+
                                    free_percentage_state+' : Free Disk Storage '+str(free_percentage)+' % minimum 20%'+'\n'+
                                    'Temperature '+str(list_state['sensors']['temperature'])+' °C'+'\n'+
                                    'Hydrometry '+str(list_state['sensors']['humidity'])+' %',
                                    color=color_msg
                                    
                                    )

            notification.set_author(name='Date : '+startDateNow+' Time : '+startTimeNow)
            #Send the Autopilot Notification to Discord
            hook.send(embed=notification)
        #test if the old status is different to the new one in this case the length of the array must be greater than 1    
        elif ((len(robot_status_list)>1) and (robot_status!=robot_status_list[-2]))  :              
            #Prepare the content to send with Webhook                
            notification = Embed(

                                    description=robot_state+' : ROBOT STATUS '+robot_status+'\n'+
                                    battery_state+' : Battery status '+str(battery_percentage)+' % minimum 40%'+'\n'+
                                    free_percentage_state+' : Free Disk Storage '+str(free_percentage)+' % minimum 20%'+'\n'+
                                    'Temperature '+str(list_state['sensors']['temperature'])+' °C'+'\n'+
                                    'Hydrometry '+str(list_state['sensors']['humidity'])+' %',
                                    color=color_msg
                                    
                                    )

            notification.set_author(name='Date : '+startDateNow+' Time : '+startTimeNow)
            #Send the Autopilot Notification to Discord
            hook.send(embed=notification)
        

#While true repeat the execution of the function notificationsHook
while True:

    run_pending()
    time.sleep(1)       

                

