from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Novels, Chapters
from .services import NovelFilterService
from django.core.paginator import Paginator
from proto.novels_pb2 import NovelList
from proto.noveldetails_pb2 import NovelDetails
from proto.chapterlist_pb2 import ChaptersList
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
            novel = Novels.objects.get(novel_id=novel_id)

            novel_detail = NovelDetails()

            novel_detail.novel_id = novel.novel_id
            novel_detail.image_url = str(novel.image_url) or ''
            novel_detail.title = str(novel.title) or ''
            novel_detail.genre = ', '.join(novel.genre) if novel.genre else ''
            novel_detail.synopsis = str(novel.synopsis) or ''
            novel_detail.tags = ', '.join(novel.tags) or ''
            novel_detail.author = str(novel.author) if novel.author else ''
            novel_detail.last_chapter = novel.last_chapter if novel.last_chapter is not None else 0

            return Response(novel_detail)

        except Novels.DoesNotExist:
            error_response = {'error': 'Novel not found'}
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)


class FilterNovelsBySingleGenreView(APIView):
    """
    This class-based view filters novels based on a single genre passed in the query parameters.
    """
    def get(self, request, *args, **kwargs):
        genre_to_filter = request.query_params.get('genre', None)
        
        if not genre_to_filter:
            return Response({'error': 'No genre specified'}, status=status.HTTP_400_BAD_REQUEST)

        filtered_novels = NovelFilterService.filter_by_genre(genre_to_filter)

        paginator = Paginator(filtered_novels, 10)
        page_number = request.query_params.get('page', 1)
        page = paginator.get_page(page_number)

        response = NovelList()

        response.total_pages = paginator.num_pages
        response.current_page = page.number

        for novel in page.object_list:
            novel_msg = response.novels.add()
            novel_msg.novel_id = novel.novel_id
            novel_msg.title = str(novel.title)
            novel_msg.image_url = str(novel.image_url)

        return Response(response)

class PaginatedChaptersListView(APIView):
    def get(self, request, novel_id):
        try:
            reverse_order = request.query_params.get('reverse', 'false').lower() == 'true'
            chapters = Chapters.objects.filter(novel_id=novel_id)

            if reverse_order:
                chapters = chapters.order_by('-timestamp') 

            paginator = Paginator(chapters, 50)
            page_number = request.query_params.get('page', 1)
            page = paginator.get_page(page_number)

            response = ChaptersList()
            response.total_pages = paginator.num_pages
            response.current_page = page.number

            for chapter in page.object_list:
                chapter_msg = response.chapters.add()
                chapter_msg.novel_id = chapter.novel_id
                chapter_msg.title = chapter.title or ''
                chapter_msg.timestamp = chapter.timestamp.isoformat() if chapter.timestamp else ''
                chapter_msg.index = chapter.index if chapter.index is not None else -1
                chapter_msg.subchapter = chapter.subchapter if chapter.subchapter is not None else -1

            # Return the paginated response
            return Response(response)

        except Chapters.DoesNotExist:
            error_response = {'error': 'No chapters found for this novel_id'}
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)