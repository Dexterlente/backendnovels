from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Novels, Chapters
from .services import NovelFilterService
from django.core.paginator import Paginator
from proto.novels_pb2 import NovelList, Novel
from proto.noveldetails_pb2 import NovelDetails
from proto.chapterlist_pb2 import ChaptersList
from proto.chapterdetail_pb2 import ChapterDetails
from rest_framework import status
import random

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

class ChapterDetailsView(APIView):
    def get(self, request, novel_id, index, subchapter=None):
        try:
            if subchapter is None:
                chapter = Chapters.objects.get(novel_id=novel_id, index=index)
                if chapter is None:
                    error_response = {'error': 'Chapter not found'}
                    return Response(error_response, status=status.HTTP_404_NOT_FOUND)
            else:
                 chapter = Chapters.objects.get(novel_id=novel_id, index=index, subchapter=subchapter)

            chapter_detail = ChapterDetails()

            chapter_detail.novel_id = chapter.novel_id
            chapter_detail.title = str(chapter.title) or ''
            chapter_detail.timestamp = chapter.timestamp.isoformat() if chapter.timestamp else ''
            chapter_detail.index = chapter.index if chapter.subchapter is not None else -1
            chapter_detail.subchapter = chapter.subchapter if chapter.subchapter is not None else -1
            chapter_detail.content = str(chapter.content) or ''

            return Response(chapter_detail)

        except Chapters.DoesNotExist:
            error_response = {'error': 'Novel not found'}
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)


class NovelSingleRandom(APIView):
    def get(self, request, *args, **kwargs):
        genre_to_filter = request.query_params.get('genre', None)
        
        if not genre_to_filter:
            return Response({'error': 'No genre specified'}, status=status.HTTP_400_BAD_REQUEST)

        filtered_novels = NovelFilterService.filter_by_genre(genre_to_filter)
        if not filtered_novels.exists():
            return Response({'error': 'No novels found for the specified genre'}, status=status.HTTP_404_NOT_FOUND)

        novel = random.choice(filtered_novels)

        NovelBook = Novel()

        NovelBook.novel_id = novel.novel_id
        NovelBook.title = str(novel.title)
        NovelBook.image_url = str(novel.image_url)

        return Response(NovelBook)

class SevenRandomNovel(APIView):
    def get(self, request, *args, **kwargs):
        genre_to_filter = request.query_params.get('genre', None)
            
        if not genre_to_filter:
            return Response({'error': 'No genre specified'}, status=status.HTTP_400_BAD_REQUEST)

        filtered_novels = NovelFilterService.filter_by_genre(genre_to_filter)
        random_novels = random.sample(list(filtered_novels), min(7, len(filtered_novels)))

        response = NovelList()
        response.total_pages = len(filtered_novels)
        response.current_page = len(random_novels)

        for novel in random_novels:
            novel_msg = response.novels.add()
            novel_msg.novel_id = novel.novel_id  
            novel_msg.title = str(novel.title)
            novel_msg.image_url = str(novel.image_url)

        return Response(response)

class GetLatestChaptersList(APIView):
    def get(self, novel_id):
        try:
            chapters = Chapters.objects.all().order_by('-timestamp')

            paginator = Paginator(chapters, 14)
            page_number = 1
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

                novel = Novels.objects.filter(novel_id=chapter.novel_id).first()
                chapter_msg.novel_title = novel.title if novel else 'Unknown'

            return Response(response)

        except Exception as e:
            error_response = {'error': str(e)}
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
                
class SearchNovels(APIView):
    def get(self, request, *args, **kwargs):
        try:
            title_query = request.query_params.get('title', None)

            novels = Novels.objects.all()
            if title_query == '':
                return Response(NovelList())
                
            if title_query:
                novels = novels.filter(title__icontains=title_query)
                
            paginator = Paginator(novels, 10)
            page_number = request.query_params.get('page', 1)  # Default to page 1
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

        except Exception as e:
            error_response = {'error': str(e)}
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)