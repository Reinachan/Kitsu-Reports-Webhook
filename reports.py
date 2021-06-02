# Imports
from typing import Literal
import requests
import json
import time
import os
import env
import lib.constants as constants
import lib.get_user as get_user
import lib.get_url_type as get_url_type
import lib.get_offender as get_offender
import lib.get_image as get_image
import lib.discord

stop_code = False

def fetch_reports():
  # FETCH DATA FROM KITSU
  url = constants.url
  headers = constants.headers
  response = requests.get(url, headers=headers)
  data = json.loads(response.text)


  # FETCH PREVIOUS REQUEST
  latest_report = "0"

  if os.path.exists("reports.json"):
    with open("reports.json", "r") as read_file:
      # Convert JSON file to Python Types
      obj = json.load(read_file) 
    
    if "data" in obj:
      if len(obj["data"]) > 0:
        latest_report = obj["data"][0]["id"]
      else:
        to_discord = {
          "username": "Kitsu Reports",
          "url": "https://kitsu.io/admin/reports/open",
          "avatar_url": "https://avatars.githubusercontent.com/u/7648832?s=200&v=4",
          "content": "There's no data for some reason. Most likely the token needs to be refreshed. Go tell <@374927132327149568> that she has to stop being lazy and make an auto token refresher"
        }
        print("token needs refresh")
        lib.discord.discord(to_discord)
        
        return False
    else:
      to_discord = {
        "username": "Kitsu Reports",
        "url": "https://kitsu.io/admin/reports/open",
        "avatar_url": "https://avatars.githubusercontent.com/u/7648832?s=200&v=4",
        "content": "There's no data for some reason. Most likely the token needs to be refreshed. Go tell <@374927132327149568> that she has to stop being lazy and make an auto token refresher"
      }
      print("token needs refresh")
      lib.discord.discord(to_discord)
      return False


  # SORT OUT TO ONLY NEW REPORTS
  new_reports = []

  if "data" in data:
    for report in data["data"]:
      if report["id"] > latest_report:
        # Structure data for Discord
        attr = report["attributes"]
        rel = report["relationships"]

        reporter = get_user.get_user(rel)

        naughty_type = attr["naughtyType"]
        naughty_url_type = get_url_type.get_url_type(naughty_type)

        post_url = "https://kitsu.io/" + naughty_url_type + "/" + str(attr["naughtyId"])

        offender = get_offender.get_offender(naughty_url_type, attr["naughtyId"])

        offending_image = None
        if offender:
          print(offender)
          offender_name = offender["included"][0]["attributes"]["name"]
          
          if naughty_url_type == "media-reactions":
            offender_text = offender["data"]["attributes"]["reaction"]
          else:
            offender_text = offender["data"]["attributes"]["content"]
            if offender["data"]["relationships"]["uploads"]["links"]["related"]:
              offending_image = get_image.get_image(offender["data"]["relationships"]["uploads"]["links"]["related"])
            else:
              offending_image = None
            
          
        else:
          offender_name = "Missing"
          offender_text = "Missing"

        description = "**Explanation**\n" + str(attr["explanation"]) + "\n\n**Offender**\n" + str(offender_name) + "\n\n**Offense**\n" + str(offender_text)

        description = (description[:1040] + ' …') if len(description) > 1040 else description
        print(description)

        discord = {
          "url": post_url,
          "timestamp": attr["createdAt"],
          "description": description,
          "color": "16208182",
          "image": {
            "url": offending_image,
          },
          "author": {
            "name": reporter["name"],
            "url": "https://kitsu.io/admin/reports/open",
            "icon_url": reporter["avatar"]["small"],
          },
          "footer": {
            "text": "Status: " + attr["status"]
          },
          "fields": [
            {
              "name": "Links",
              "value": "[" + attr["naughtyType"] + "](" + post_url + ")\n" + "[All Reports](https://kitsu.io/admin/reports/open)",
              "inline": "true",
            },
            {
              "name": "Reason",
              "value": attr["reason"],
              "inline": "true",
            },
          ],
        }

        new_reports.append(discord)
  else:
    to_discord = {
      "username": "Kitsu Reports",
      "url": "https://kitsu.io/admin/reports/open",
      "avatar_url": "https://avatars.githubusercontent.com/u/7648832?s=200&v=4",
      "content": "There's no data for some reason. Most likely the token needs to be refreshed. Go tell <@374927132327149568> that she has to stop being lazy and make an auto token refresher"
    }
    print("token needs refresh")
    return False


  for nreport in new_reports[::-1]:
    to_discord = {
      "username": "Kitsu Reports",
      "url": "https://kitsu.io/admin/reports/open",
      "avatar_url": "https://avatars.githubusercontent.com/u/7648832?s=200&v=4",
      "embeds": [nreport]
    }

    # SEND NEW REPORTS TO DISCORD WEBHOOK
    disc_response = requests.post(
      env.webhook,
      headers = {'Content-Type': 'application/json'},
      json = to_discord,
    )
    
    print(disc_response)
    time.sleep(0.5)




  if "data" in data:
    # write json to disk for next comparsion
    with open("reports.json", "w") as write_file:
      json.dump(data, write_file, indent=4)
  else:
    print("probably invalid token or smth. No 'data' in the response")

while not stop_code:
  if type(fetch_reports()) != bool:  
    print("Fetched")
    time.sleep(60)
  else:
    break