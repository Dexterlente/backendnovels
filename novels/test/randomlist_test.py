import requests
import base64
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from proto.novels_pb2 import NovelList

url = 'http://127.0.0.1:8000/api/novel/list-random/?genre=fantasy'

headers = {
    'Accept': 'application/x-protobuf',
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    try:
        print("Raw response content (Base64 encoded):", response.text)

        encoded_data = response.text
        serialized_data = base64.b64decode(encoded_data)

        novel_list = NovelList()
        novel_list.ParseFromString(serialized_data)

        print(f'Total Pages: {novel_list.total_pages}')
        print(f'Current Page: {novel_list.current_page}')

        for novel in novel_list.novels:
            print(f'novel id: {novel.novel_id}')
            print(f'Title: {novel.title}')
            print(f'Image URL: {novel.image_url}')
            print('---')

    except Exception as e:
        print(f'Failed to decode and deserialize the Protobuf data: {e}')
else:
    print(f"Failed to fetch data from API, status code: {response.status_code}")