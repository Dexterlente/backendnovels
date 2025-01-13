from django.urls import path
from . import views

urlpatterns = [
     path('novels/', views.PaginatedNovelsProtobufView.as_view()),
     path('novel-details/<int:novel_id>/', views.NovelDetailsView.as_view()),
     path('novels/single/', views.FilterNovelsBySingleGenreView.as_view()),
     path('chapters/<int:novel_id>', views.PaginatedChaptersListView.as_view()),
     path('chapters-details/<int:novel_id>/<int:index>', views.ChapterDetailsView.as_view()),
]
