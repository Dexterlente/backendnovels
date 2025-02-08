from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

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
    title = models.CharField(max_length=255, blank=True, null=True)
    genre = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    synopsis = models.TextField(blank=True, null=True)
    tags = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    author = models.CharField(max_length=255, blank=True, null=True)
    last_chapter = models.IntegerField(blank=True, null=True)
    images = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'novels'

    def __str__(self):
        return f"Novel_id-{self.novel_id} {self.title}"