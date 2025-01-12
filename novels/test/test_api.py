import requests
from proto.novels_pb2 import NovelList  # Ensure to import the generated Protobuf classes

# Make the GET request
response = requests.get("http://localhost:8000/api/novels/?page=1", headers={"Accept": "application/x-protobuf"})

# Ensure the response is Protobuf
if response.headers['Content-Type'] == 'application/x-protobuf':
    # Deserialize the Protobuf data
    novel_list = NovelList()
    novel_list.ParseFromString(response.content)

    # Print the contents of the Protobuf message
    print(f"Total pages: {novel_list.total_pages}")
    print(f"Current page: {novel_list.current_page}")
    for novel in novel_list.novels:
        print(f"Title: {novel.title}, Image URL: {novel.image_url}")
else:
    print("Response is not in Protobuf format.")
