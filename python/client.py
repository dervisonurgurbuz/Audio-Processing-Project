import requests

emotion = 'happy'
energy = 0.6
dancebility = 0.5
loudness = -0.4

url = f'http://localhost:3004?emotion=${emotion}&energy=${energy}&loudness=${loudness}&dancebility=${dancebility}'

try:
  response = requests.get(url)
  response.raise_for_status()
except Exception as e:
  print("OOps: Something wrong", e)
