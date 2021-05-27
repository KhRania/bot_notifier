from modules import Notification
#schedule the run of the function 
import schedule 
import time


notif= Notification()
schedule.every(30).seconds.do(notif.postWebhook)
    
while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6