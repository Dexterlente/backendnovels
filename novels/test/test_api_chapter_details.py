import requests
import base64
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from proto.noveldetails_pb2 import  NovelDetails

url = 'http://localhost:8000/api/novel-details/12'

headers = {
    'Accept': 'application/x-protobuf',
}

# Send the request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    try:
        # Print the raw response content (Base64-encoded or raw Protobuf binary data)
        print("Raw response content (Base64 or Protobuf binary):", response.text)

        # Decode Base64 (if the response is Base64-encoded)

        encoded_data = response.text
        serialized_data = base64.b64decode(encoded_data)  # Decode the Base64 string into bytes


        # Deserialize the Protobuf data into a NovelDetails object
        novel_details = NovelDetails()
        novel_details.ParseFromString(serialized_data)  # Parse the Protobuf data

        # Print out the decoded novel details
        print(f"Novel ID: {novel_details.novel_id}")
        print(f"Title: {novel_details.title}")
        print(f"Image URL: {novel_details.image_url}")
        print(f"Genre: {novel_details.genre}")
        print(f"Synopsis: {novel_details.synopsis}")
        print(f"Tags: {novel_details.tags}")
        print(f"Author: {novel_details.author}")
        print(f"Last Chapter: {novel_details.last_chapter}")

    except Exception as e:
        print(f"Failed to decode and deserialize the Protobuf data: {e}")
else:
    print(f"Failed to fetch data from API, status code: {response.status_code}")
