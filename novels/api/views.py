from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Novels
from django.core.paginator import Paginator
from proto.novels_pb2 import NovelList
from proto.noveldetails_pb2 import NovelDetails
from rest_framework import status

class PaginatedNovelsProtobufView(APIView):
    def get(self, request, *args, **kwargs):
        # Query all novels from the database
        novels = Novels.objects.all()

        paginator = Paginator(novels, 10)  # Show 10 novels per page
        page_number = request.query_params.get('page', 1)  # Default to page 1
        page = paginator.get_page(page_number)

        # Create the Protobuf response object
        response = NovelList()

        # Set pagination information
        response.total_pages = paginator.num_pages
        response.current_page = page.number

        # Add each novel to the Protobuf response
        for novel in page.object_list:
            novel_msg = response.novels.add()  # Add a new novel message
            novel_msg.novel_id = novel.novel_id
            novel_msg.title = str(novel.title)  # Ensure it's a string
            novel_msg.image_url = str(novel.image_url)  # Ensure it's a string

        return Response(response) # Let the ProtobufRenderer handle serialization

class NovelDetailsView(APIView):
    def get(self, request, novel_id):
        try:
            # Retrieve the novel details from the database
            novel = Novels.objects.get(novel_id=novel_id)

            # Create a new instance of the ProtoBuf message
            novel_detail = NovelDetails()

            # Populate the ProtoBuf message with the novel details
            novel_detail.novel_id = novel.novel_id
            novel_detail.image_url = novel.image_url or ''
            novel_detail.title = novel.title or ''
            novel_detail.genre = novel.genre or ''
            novel_detail.synopsis = novel.synopsis or ''
            novel_detail.tags = novel.tags or ''
            novel_detail.author = novel.author or ''
            novel_detail.last_chapter = novel.last_chapter if novel.last_chapter is not None else 0

            return Response(novel_detail)

        except Novels.DoesNotExist:
            # Handle the case where the novel is not found
            error_response = {'error': 'Novel not found'}
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)