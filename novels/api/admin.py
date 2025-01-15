from django.contrib import admin
from .models import CustomUser, Novels, Chapters
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Novels)
admin.site.register(Chapters)