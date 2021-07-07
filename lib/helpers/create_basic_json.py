import json


def create_basic_json():
    with open("reports.json", "w") as json_file:
        content = {"reports": [{"id": "0", "discord": "", "status": "RESOLVED"}]}

        json_file.write(json.dumps(content))
