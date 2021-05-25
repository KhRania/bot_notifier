from flask import Flask
from threading import Thread


app = Flask('')


@app.route('/')
def home():
    return "Your server is alive => Your Bot is alive"

def run():
  app.run(host='0.0.0.0',port=40044)

def keep_alive():
    t = Thread(target=run)
    t.start()