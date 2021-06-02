import requests
import json
import lib.constants as constants

def get_image(link):
    print(link)
    offender_data = ""
    offender_data = requests.get(link, headers=constants.headers)
    offender_data = json.loads(offender_data.text)
    
    if "errors" in offender_data:
      offender_data = None
      
    if "data" in offender_data:
      if "meta" in offender_data:
        if offender_data["meta"]["count"] > 0:    
          if "original" in offender_data["data"][0]["attributes"]["content"]:
            offender_data = offender_data["data"][0]["attributes"]["content"]["original"]
        else:
          offender_data = None
    
    return offender_data