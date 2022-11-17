import requests

URL = "http://140.238.28.123/dest_result"
response = requests.get(URL)

print(response.status_code)
print(response.text)
