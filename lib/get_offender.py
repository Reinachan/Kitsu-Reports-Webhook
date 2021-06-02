import requests
import json
import lib.constants as constants

def get_offender(post_type, post_id):
    url_offender = "https://kitsu.io/api/edge/" + post_type + "/" + str(post_id) + "?include=user"

    print(url_offender)

    offender_data = ""
    offender_data = requests.get(url_offender, headers=constants.headers)
    offender_data = json.loads(offender_data.text)
    
    if "errors" in offender_data:
      offender_data = None
    
    return offender_data