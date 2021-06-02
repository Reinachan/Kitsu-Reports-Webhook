import requests
import json

def authentication(username, password):
  auth = requests.post(
    "https://kitsu.io/api/oauth/token",
    headers={
      'Accept': 'application/vnd.api+json',
      'Content-Type': 'application/vnd.api+json',
    },
    json={
      "grant_type": 'password',
      "username": username,
      "password": password, # RFC3986 URl encoded string
    },
  )
  auth = json.loads(auth.text)
  
  return auth["access_token"]