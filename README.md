# Kitsu Reports to Webhook

Fetch reports from Kitsu and send them to a Discord webhook

Reports look something like this

<img width="400px" src="https://i.imgur.com/ZXho4t0.png" alt="preview"></img>

## Setup Requirements

Fill in the `.env` file with the appropriate information.

Run `pip install pipenv` to install pipenv<br>
Run `pipenv sync` to download dependencies<br>
Run `pipenv run python main.py` to start the program<br>

## Notes

Currently it won't remove old reports, so the reports.json will just get larger and larger. Eventually I'll strip it of older and unecessary report logs.
