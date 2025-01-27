import requests
import base64
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from proto.chapterdetail_pb2 import  ChapterDetails

url = 'http://127.0.0.1:8000/api/chapters-details/134/138/2'

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
        chapter_details = ChapterDetails()
        chapter_details.ParseFromString(serialized_data)  # Parse the Protobuf data

        # Print out the decoded novel details
        print(f"Novel ID: {chapter_details.novel_id}")
        print(f"Title: {chapter_details.title}")
        print(f"Content: {chapter_details.content}")
        print(f"Timestamp: {chapter_details.timestamp}")
        print(f"Index: {chapter_details.index}")
        print(f"Subchapter: {chapter_details.subchapter}")
        print(f"index_before: {chapter_details.index_before}")
        print(f"index_after: {chapter_details.index_after}")


    except Exception as e:
        print(f"Failed to decode and deserialize the Protobuf data: {e}")
else:
    print(f"Failed to fetch data from API, status code: {response.status_code}")
