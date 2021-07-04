from dotenv import load_dotenv
from lib.report import fetch_reports
import requests

load_dotenv(".env")

# fetch_reports()

payload = {
    "content": "This is a message with components",
    "components": [
        {
            "type": 1,
            "components": [
                {
                    "type": 2,
                    "label": "Click me!",
                    "style": 5,
                    "url": "https://pressfire.no",
                }
            ],
        }
    ],
}

query = {
    "wait": "true",
    "Authorization": "Bot ODQ5Mzg1ODE5NTYyNTczODc0.YLaaMA.Vzryc72O0OK_dkks87tkQGRTWXY",
}

response = requests.post(
    "https://discord.com/api/webhooks/855958892827246593/sIYuxm30lkHt9Ex0UPfzQ00O6C4WcmG3UIhg6WMQtfTvkxSLl4b_wfRnsBbGnq62tpr_",
    params=query,
    json=payload,
)

print(response.headers)
print(response.text)
