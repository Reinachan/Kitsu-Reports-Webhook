import requests
import env

def discord(message):
  disc_response = requests.post(
    env.webhook,
    headers = {'Content-Type': 'application/json'},
    json = message,
  )
  return disc_response