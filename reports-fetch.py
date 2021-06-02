# Imports
import requests
import json
import time
import os
import env

def fetch_reports():
  # FETCH DATA FROM KITSU
  url = "https://kitsu.io/api/edge/reports?sort=-id"
  headers = {
    'Accept': 'application/vnd.api+json',
    'Content-Type': 'application/vnd.api+json',
    'Authorization': 'Bearer ' + env.token
  }
  response = requests.get(url, headers=headers)
  data = json.loads(response.text)


  # FETCH PREVIOUS REQUEST
  latest_report = "0"

  if os.path.exists("reports.json"):
    with open("reports.json", "r") as read_file:
      # Convert JSON file to Python Types
      obj = json.load(read_file) 
    latest_report = obj["data"][0]["id"]


  # SORT OUT TO ONLY NEW REPORTS
  def get_user(rel):
    user = requests.get(rel["user"]["links"]["related"], headers=headers)
    user = json.loads(user.text)
    user = user["data"]["attributes"]
    return user

  def get_url_type(ntype):
    if ntype == "Post":
      return "posts"
    elif ntype == "Comment":
      return "comments"
    elif ntype == "Reaction":
      return "media-reactions"
    elif ntype == "Review":
      return "reviews"

  def get_offender(post_type, post_id):
    url_offender = "https://kitsu.io/api/edge/" + post_type + "/" + str(post_id) + "?include=user"

    print(url_offender)

    offender_data = ""
    try: 
      offender_data = requests.get(url_offender, headers=headers)
      offender_data = json.loads(offender_data.text)
      print(offender_data["included"][0]["attributes"]["name"])
    except: 
      offender_data = None
    finally: return offender_data






  new_reports = []

  for report in data["data"]:
    if report["id"] > latest_report:
      # Structure data for Discord
      attr = report["attributes"]
      rel = report["relationships"]

      reporter = get_user(rel)

      naughty_type = attr["naughtyType"]
      naughty_url_type = get_url_type(naughty_type)

      post_url = "https://kitsu.io/" + naughty_url_type + "/" + str(attr["naughtyId"])

      offender = get_offender(naughty_url_type, attr["naughtyId"])

      offender_name = ""
      if offender:
        print(offender)
        offender_name = offender["included"][0]["attributes"]["name"]
        offender_text = offender["included"][0]["attributes"]["name"]
      else:
        offender_name = "Missing"

      description = "**Explanation**\n" + str(attr["explanation"]) + "\n\n**Offender**\n" + str(offender_name) + "\n\n**Offence**\n" + str()

      print(description)

      discord = {
        "url": post_url,
        "timestamp": attr["createdAt"],
        "description": description,
        "color": "16208182",
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




  # write json to disk for next comparsion
  with open("reports.json", "w") as write_file:
    json.dump(data, write_file, indent=4)

while True:
  fetch_reports()
  print("Fetched")
  time.sleep(300)