import env

url = "https://kitsu.io/api/edge/reports?sort=-id"
headers = {
  'Accept': 'application/vnd.api+json',
  'Content-Type': 'application/vnd.api+json',
  'Authorization': 'Bearer ' + env.token
}