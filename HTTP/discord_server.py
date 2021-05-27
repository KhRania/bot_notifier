#!/usr/bin/env python3

import discord
import configuration as cfg
import requests
from requests.exceptions import HTTPError
import schedule
import time
import datetime
from keep_alive import keep_alive
from modules import Notification



client = discord.Client()

#register an event 
#discrod.py is an async library to manage thinks it will be by callbacks 
#this func will be called when the bot it will be used
@client.event
async def on_ready():
  print('We have logged in Discord Server as {0.user}'.format(client))


#when  receive message
@client.event
async def on_message(message):
  notif= Notification()
  notification_msg,color_msg=notif.msgNotify()
  # we do not want the bot to reply to itself
  if message.author == client.user:
    print('User sends a msg')
  if message.content.startswith('!notify'):
 
    if notification_msg:
        embedVar = discord.Embed(description=notification_msg ,color=color_msg)   
        await message.channel.send(embed=embedVar)
      
    else:
      embedVar = discord.Embed(description="🔕   ** REST Server not available No notification to send **" ,color=0xc0c6c8 )   
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

    