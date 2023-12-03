import requests

# Sending request to Java Script Backend Server
emotion = "Calm" # Important: This needs to be Calm, Happy, Energetic or Sad
tempo =  98

url = f"http://localhost:3004?emotion={emotion}&tempo={tempo}"
headers = {}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for non-2xx status codes
    print(response.json())
except requests.exceptions.RequestException as e:
    print(e)
