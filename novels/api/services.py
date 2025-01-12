from .models import Novels

class NovelFilterService:
    @staticmethod
    def filter_by_genre(genre: str):
        """
        This function filters the novels based on the provided genre.
        Returns a queryset of filtered novels.
        """
        return Novels.objects.filter(genre__icontains=genre)
    
    @staticmethod
    def filter_by_multiple_genre(genre: list):
        """
        This function filters novels based on multiple genre.
        Returns a queryset of filtered novels.
        """
        return Novels.objects.filter(genre__overlap=genre)
