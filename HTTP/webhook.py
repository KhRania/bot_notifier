from modules import Notification
#schedule the run of the function 
import schedule 
import time
from dhooks import Webhook, Embed, File
import configuration as cfg
import requests
from io import BytesIO,StringIO
from PIL import Image

discord_channel=Webhook(cfg.urls["webhookurl"])
screenshot_url=cfg.urls["takescreenshot"]
notif= Notification()

def postWebhook():
      
        body_msg,color_msg=notif.msgWebhook()
        
       
        resp = notif.screenshot()
        #print(resp)
        if body_msg:
            #Prepare notification content to send with Webhook                
            notification = Embed(description=body_msg,color=color_msg)
            response = requests.get(screenshot_url)
            screenshot = File(BytesIO(response.content), name='quad.png')
            #Send the Notification to Discord
           
            discord_channel.send(embed=notification)
            discord_channel.send(file=screenshot)
            print("Webhook sent !")
            discord_channel.close()
            screenshot.close()
            
        else:
            print("Nothing to send !")
       
schedule.every(30).seconds.do(postWebhook)
    
while True:
    try:
      
        schedule.run_pending()
        time.sleep(1)
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6