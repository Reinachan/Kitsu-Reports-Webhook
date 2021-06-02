import requests
import json
import lib.constants as constants

def get_user(rel):
  user = requests.get(rel["user"]["links"]["related"], headers=constants.headers)
  user = json.loads(user.text)
  user = user["data"]["attributes"]
  return user