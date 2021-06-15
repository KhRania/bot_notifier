import discord
from keep_aliveH import keep_alive
import time


client = discord.Client()

sender_list=['user']
msg_list=[]
#register an event 
#discrod.py is an async library to manage thinks it will be by callbacks 
#this func will be called when the bot it will be used
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

 
#when  receive message

@client.event
async def on_message(message):
  global sender_list
  last_msg=False

  user_sender = ''
  bot_sender=''
  notify_msg='!notify'
  embeds = message.embeds
  
  embedNotif = discord.Embed(description=" :loudspeaker: ** Robot Not Available **",color=0xc0c6c8 )
  unavailable_msg={'color': 12633800, 'type': 'rich', 'description': ':loudspeaker: ** Robot Not Available **'}


  try:
    for embed in embeds:
        
        details=embed.to_dict()
        if details == unavailable_msg:
            last_msg=True
        break
  except Exception as err:
        print(f'Other error occurred: {err}')  

#   c_channel = discord.utils.get(message.guild.text_channels, name='development-and-test')
#   msg_list.append(c_channel.last_message.embeds)
#   msg_list.append(c_channel.last_message.content)
#   print(msg_list)  
#   print(embeds)
  if message.author != client.user: #IF 1
    if  message.content.lower()==notify_msg: 
    
      user_sender = 'user'
      sender_list.append(user_sender)
      #print("IF 1 user")
      
      
  else:
    if last_msg==True:

        last_msg=False   
        
    else:
       
        print(" robot dispo ")
    sender_list=sender_list[1:]
    return
  print(sender_list)
  try:

            if sender_list[-1]=='user' and sender_list[0]=='user':

                if len(sender_list)==1:
                  
                    pass

                else:

                    print(" robot non dispo ")
                    
                    await message.channel.send(embed=embedNotif)
                    #sender_list=sender_list[1:]
  except Exception as err:
    print(f'Exception: {err}')  # Python 3.6  
  


    
keep_alive()
client.run("ODQ1MzE0ODUxNTkyMDc3MzEy.YKfKzQ.fUNMmVBzZlLrNPtDQtS8ikugd6M")