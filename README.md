# Kitsu Reports to Webhook

Fetch Reports From Kitsu and Send Them to a Discord Webhook

## Setup Requirements

Create a file called `env.py` in root. Add this to it and replace the strings with relevant details.

~~~python
webhook = "Discord webhook link"
token = "Kitsu accesstoken"
~~~

Run script by calling `python reports-fetch.py` in root directory. Requires an account with moderator or admin priviledges on Kitsu.

## Missing/Planned functionality

- Fetch token and refresh regularly.
- Display content of offense
