# Kitsu Reports to Webhook

Fetch Reports From Kitsu and Send Them to a Discord Webhook

## Setup Requirements

Create a file called `env.py` in root. Add this to it and replace the strings with relevant details.

```python
webhook = "Discord webhook link"
token = "Kitsu accesstoken"
```

Run script by calling `python reports-fetch.py` in root directory. Requires an account with moderator or admin priviledges on Kitsu.

## Notes

Writing the SQLite database structure in [DB Browser for SQLite](https://sqlitebrowser.org/)

## Missing/Planned functionality

- REFACTOR!!
- Fetch token and refresh regularly
- Display content of offense
