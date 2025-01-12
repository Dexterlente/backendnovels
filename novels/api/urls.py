# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
     path('novels/', views.PaginatedNovelsProtobufView.as_view(), name='paginated_novels_protobuf'),
]
