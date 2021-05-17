#!/usr/bin/env python3

import discord
#from webhook import notificationsHook
import configuration as cfg


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
  # we do not want the bot to reply to itself
  if message.author == client.user:
    print('User sends a msg')
  if message.content.startswith('!notify'):
  
    await message.channel.send('hello!')
#new member join the server    
@client.event
async def on_member_join(member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f'Welcome {member.mention} to {guild.name}!'
            await guild.system_channel.send(to_send)
            print("welcome !")
#notificationsHook()
client.run(cfg.urls["token"])