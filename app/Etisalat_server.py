#!/usr/bin/env python3

import discord
from discord.ext import commands
import configuration as cfg
import schedule
import time
import datetime
from keep_alive import keep_alive
from modules import Notification


bot = commands.Bot(command_prefix='!', description="This is a Helper Bot")

#register an event 
#discrod.py is an async library to manage thinks it will be by callbacks 
#this func will be called when the bot it will be used
@bot.event
async def on_ready():
  print('We have logged in Discord Server as '+ str(bot.user))
  
#when  receive message
@bot.event
async def on_message(message):

  notif= Notification()
  notification_msg,color_msg=notif.msgNotify()
  battery_msg,color_battery_msg=notif.batteryMessage()
  free_disk_msg,color_free_disk_msg=notif.storageMessage()
  temperature_msg,color_temperature_msg=notif.temperatureMessage()
  humidity_msg,color_humidity_msg=notif.humidityMessage()
  state_msg,color_state_msg=notif.stateMessage()

  notify_notif='!notify'
  screenshot_notif='!notify screenshot'
  battery_notif='!notify battery'
  hum_notif='!notify humidity'
  temp_notif='!notify temperature'
  storage_notif='!notify storage'
  state_notif="!notify state"
  help_notif='!notify help'

  # we do not want the bot to reply to itself
  if message.author == bot.user:
    print('Bot sends a msg')
  else:
    print('User sends a msg')  
  if message.content.lower()==state_notif or message.content.lower()==notify_notif or message.content.lower()==battery_notif  or message.content.lower()==hum_notif or message.content.lower()==temp_notif or message.content.lower()== storage_notif or message.content.lower()==help_notif:
 
    if state_msg and message.content.lower()==state_notif :
        embedVar = discord.Embed(description=state_msg ,color=color_state_msg)   
        await message.channel.send(embed=embedVar)

    elif notification_msg and message.content.lower()==notify_notif :
        embedVar = discord.Embed(description=notification_msg ,color=color_msg)
        await message.channel.send(embed=embedVar)
      
    elif battery_msg and message.content.lower()==battery_notif:
        embedVar = discord.Embed(description=battery_msg ,color=color_battery_msg)   
        await message.channel.send(embed=embedVar)

    elif free_disk_msg and message.content.lower()== storage_notif:
        embedVar = discord.Embed(description=free_disk_msg ,color=color_free_disk_msg)   
        await message.channel.send(embed=embedVar)

    elif temperature_msg and message.content.lower()==temp_notif:
        embedVar = discord.Embed(description=temperature_msg ,color=color_temperature_msg)   
        await message.channel.send(embed=embedVar)

    elif humidity_msg and message.content.lower()==hum_notif:
        embedVar = discord.Embed(description=humidity_msg ,color=color_humidity_msg)   
        await message.channel.send(embed=embedVar)  

    elif message.content.lower()==help_notif : 
        embedVar = discord.Embed(description=' :speech_balloon: Robot state/sensors/battery/free storage notification : **!notify**'+'\n'+'\n'+' :bell: Robot state notification : **!notify state**'+'\n'+'\n'+' :battery: Robot battery notification : **!notify battery**'+'\n'+'\n'+' :thermometer: Robot temperature sensor notification: **!notify temperature**'+'\n'+'\n'+' :droplet: Robot humidity sensor notification : **!notify humidity**'+'\n'+'\n'+' :cd: Robot disk free storage notification : **!notify storage**' ,color=0xE6E6FA)  
        await message.channel.send(embed=embedVar)  

    else:
      embedVar = discord.Embed(description="🔕   ** REST Server not available No notification to send **" ,color=0xc0c6c8 )   
      await message.channel.send(embed=embedVar)
 

             

      
     
        

      
    





keep_alive()
bot.run(cfg.urls["token"])


