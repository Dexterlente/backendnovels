import requests
import base64
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from novels_pb2 import NovelList  # Make sure you import your generated Protobuf classes
from proto.novels_pb2 import NovelList

# Endpoint URL
# url = 'http://localhost:8000/api/novels/?page=2'
url = 'http://127.0.0.1:8000/api/novels/single/?genre=Harem&page=1'

# Setting headers to accept Protobuf
headers = {
    'Accept': 'application/x-protobuf',  # Accept protobuf responses
}

# Send GET request to the API with the proper headers
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    try:
        # Print the raw response content to debug
        print("Raw response content (Base64 encoded):", response.text)

        # Get the Base64 encoded response and decode it
        encoded_data = response.text
        serialized_data = base64.b64decode(encoded_data)  # Decode the Base64 string into bytes

        # Deserialize the Protobuf data into a NovelList object
        novel_list = NovelList()
        novel_list.ParseFromString(serialized_data)  # Parse the Protobuf data

        # Print out the data
        print(f'Total Pages: {novel_list.total_pages}')
        print(f'Current Page: {novel_list.current_page}')

        # Print all the novels
        for novel in novel_list.novels:
            print(f'novel id: {novel.novel_id}')
            print(f'Title: {novel.title}')
            print(f'Image URL: {novel.image_url}')
            print('---')

    except Exception as e:
        print(f'Failed to decode and deserialize the Protobuf data: {e}')
else:
    print(f"Failed to fetch data from API, status code: {response.status_code}")


# protoc --python_out=. novels.proto