#!/bin/bash
PATH=/home/ubecome/Documents/bot_notifier/app/state

if [ -e "$PATH" ]; then
	/usr/bin/python3 $PATH/webhook.py
fi
