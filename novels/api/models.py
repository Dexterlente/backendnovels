from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass

class Chapters(models.Model):
    chapter_id = models.AutoField(primary_key=True)
    novel = models.ForeignKey('Novels', on_delete=models.CASCADE)
    title = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)
    subchapter= models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chapters'


class Novels(models.Model):
    novel_id = models.AutoField(primary_key=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    image_cover_url = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    genre = models.TextField(blank=True, null=True)  # This field type is a guess.
    synopsis = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)  # This field type is a guess.
    author = models.CharField(max_length=255, blank=True, null=True)
    last_chapter = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'novels'
