#!/usr/bin/env python3

import discord
from discord.ext import commands
import configuration as cfg
import requests
from requests.exceptions import HTTPError
import schedule
import time
import datetime
from keep_alive import keep_alive
from modules import Notification
import aiohttp
from io import BytesIO

bot = commands.Bot(command_prefix='!', description="This is a Helper Bot")
quad1_url=cfg.urls["quad1"]
quad2_url=cfg.urls["quad2"]
bot.session = aiohttp.ClientSession(loop=bot.loop)

#register an event 
#discrod.py is an async library to manage thinks it will be by callbacks 
#this func will be called when the bot it will be used
@bot.event
async def on_ready():
  print('We have logged in Discord Server as '+ str(bot.user))
  
           

@bot.command()
async def ping(ctx):
  #channel= bot.get_channel(804657187611344942)
  await ctx.send('hello !!!')



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


  # embedVar =''
  # words=[]
  # special_chars=["$", "!", "?", "-", "*", "`", "~", "+", "/", ";", "=", "&", ">"]

  # we do not want the bot to reply to itself
  if message.author == bot.user:
    print('Bot sends a msg')
  else:
    print('User sends a msg')  
  if message.content.lower()==state_notif or message.content.lower()==notify_notif or message.content.lower()==screenshot_notif or  message.content.lower()==battery_notif  or message.content.lower()==hum_notif or message.content.lower()==temp_notif or message.content.lower()== storage_notif or message.content.lower()==help_notif:
    #state notif
    if state_msg and message.content.lower()==state_notif :
        embedVar = discord.Embed(description=state_msg ,color=color_state_msg)   
        await message.channel.send(embed=embedVar)

    #general notif
    elif notification_msg and message.content.lower()==notify_notif :
        embedVar = discord.Embed(description=notification_msg ,color=color_msg)
        await message.channel.send(embed=embedVar)
        async with aiohttp.ClientSession() as session:
            # note that it is often preferable to create a single session to use multiple times later - see below for this.
            async with session.get(quad1_url) as resp:
                buffer = BytesIO(await resp.read())

            await message.channel.send(file=discord.File(buffer, 'quad1.png'))
        
    #battery msg  
    elif battery_msg and message.content.lower()==battery_notif:
        embedVar = discord.Embed(description=battery_msg ,color=color_battery_msg)   
        await message.channel.send(embed=embedVar)

    #storage notif
    elif free_disk_msg and message.content.lower()== storage_notif:
        embedVar = discord.Embed(description=free_disk_msg ,color=color_free_disk_msg)   
        await message.channel.send(embed=embedVar)

    # temperature notif
    elif temperature_msg and message.content.lower()==temp_notif:
        embedVar = discord.Embed(description=temperature_msg ,color=color_temperature_msg)   
        await message.channel.send(embed=embedVar)
    
    #humidity notif
    elif humidity_msg and message.content.lower()==hum_notif:
        embedVar = discord.Embed(description=humidity_msg ,color=color_humidity_msg)   
        await message.channel.send(embed=embedVar)
    
    #screenshot notif   (2 quad)   
    elif message.content.lower()==screenshot_notif :
      async with aiohttp.ClientSession() as session:
            # note that it is often preferable to create a single session to use multiple times later - see below for this.
            async with session.get(quad1_url) as resp:
                buffer = BytesIO(await resp.read())

            await message.channel.send(file=discord.File(buffer, 'quad1.png'))

            async with session.get(quad2_url) as resp:
                buffer = BytesIO(await resp.read())

            await message.channel.send(file=discord.File(buffer, 'quad2.png'))            
    
    
    #help notif
    elif message.content.lower()==help_notif : 
        embedVar = discord.Embed(description=' :speech_balloon: Robot state/sensors/battery/free storage notification : **!notify**'+'\n'+'\n'+' :bell: Robot state notification : **!notify state**'+'\n'+'\n'+' :battery: Robot battery notification : **!notify battery**'+'\n'+'\n'+' :thermometer: Robot temperature sensor notification: **!notify temperature**'+'\n'+'\n'+' :droplet: Robot humidity sensor notification : **!notify humidity**'+'\n'+'\n'+' :cd: Robot disk free storage notification : **!notify storage**'+'\n'+'\n'+' :camera_with_flash: Screenshots notification (quad1 / quad2) : **!notify screenshot**' ,color=0xE6E6FA)  
        await message.channel.send(embed=embedVar)  

    else:
      embedVar = discord.Embed(description="🔕   ** REST Server not available No notification to send **" ,color=0xc0c6c8 )   
      await message.channel.send(embed=embedVar)
  #speech file contain words that they are allow to be sent in discord server
  # with open("speech.txt") as f:
  #     for lines in f:
  #           words.append(lines.strip("\n"))
  # char_found=False
  # for char in words :
  #   if char in message.content:
  #     print(char)
  #     char_found=True
  
  # print(char_found)
  # if char_found==False or message.content == embedVar or (message.content.startswith(("$", "!", "?", "-", "*", "`", "~", "+", "/", ";", "=", "&", ">")) and len(message.content)>=3): 
  #   pass  
  # else:  
  #   try:
  #     #print(message.content)
  #     await message.delete() 
  #   except Exception as err:
  #     print(f'Other error occurred: {err}')  # Python 3.6
                  

 
keep_alive()
bot.run(cfg.urls["token"])
