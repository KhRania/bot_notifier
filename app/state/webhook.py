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
discord_channel=Webhook(cfg.urls["webhookurl"])
screenshot_url=cfg.urls["quad1"]
notif= Notification()

def postWebhook():
      
        body_msg,color_msg=notif.msgWebhook()
        
       
       
        #print(resp)
        if body_msg:
            #Prepare notification content to send with Webhook                
            notification = Embed(description=body_msg,color=color_msg)
            response = requests.get(screenshot_url)
            screenshot = File(BytesIO(response.content), name='quad1.png')
            #Send the Notification to Discord
           
            discord_channel.send(embed=notification)
            discord_channel.send(file=screenshot)
            logging.info("Webhook sent !")
            discord_channel.close()
            screenshot.close()
            
        else:
            logging.info("Nothing to send !")
       
schedule.every(30).seconds.do(postWebhook)
    
while True:
    try:
      
        schedule.run_pending()
        time.sleep(1)
    except Exception as err:
        logging.error(f'Other error occurred: {err}')  # Python 3.6