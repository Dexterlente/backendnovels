from django.urls import path, re_path
from . import views

urlpatterns = [
     path('novels/', views.PaginatedNovelsProtobufView.as_view()),
     path('novel-details/<int:novel_id>/', views.NovelDetailsView.as_view()),
     path('novels/single/', views.FilterNovelsBySingleGenreView.as_view()),
     path('chapters/<int:novel_id>', views.PaginatedChaptersListView.as_view()),
     re_path(r'^chapters-details/(?P<novel_id>\d+)/(?P<index>\d+)(?:/(?P<subchapter>\d+))?/$', views.ChapterDetailsView.as_view()),
     path('novel/random/', views.NovelSingleRandom.as_view()),
     path('novel/list-random/', views.SevenRandomNovel.as_view()),
     path('novel/list-latest/', views.GetLatestChaptersList.as_view()),
     path('novels/search', views.SearchNovels.as_view())
]
