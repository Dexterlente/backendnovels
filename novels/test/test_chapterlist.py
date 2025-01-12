import base64
import requests
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from proto.chapterlist_pb2 import ChaptersList

url = 'http://127.0.0.1:8000/api/chapters/27?page=1'

headers = {
    'Accept': 'application/x-protobuf',  # Accept protobuf responses
}

response = requests.get(url, headers=headers)


if response.status_code == 200:

    encoded_data = response.text
    serialized_data = base64.b64decode(encoded_data)

    chapter_list = ChaptersList()
    chapter_list.ParseFromString(serialized_data)  

    print(f'Total Pages: {chapter_list.total_pages}')
    print(f'Current Page: {chapter_list.current_page}')

    for chapter in chapter_list.chapters:
        print(f"Novel ID: {chapter.novel_id}, Title: {chapter.title}, Timestamp: {chapter.timestamp}, Index: {chapter.index}")
else:
    print(f"Failed to fetch data, status code: {response.status_code}")
