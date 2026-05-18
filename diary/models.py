from django.db import models
from datetime import date
from django.conf import settings

class Diary(models.Model):
    title = models.CharField(max_length=200, default="기본제목")
    content = models.TextField(default="")
    date = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    emotion = models.CharField(max_length=50, null=True, blank=True)
    
    recommendation_song = models.CharField(max_length=200, null=True, blank=True)
    recommendation_reason = models.TextField(null=True, blank=True)
    youtube_url = models.URLField(max_length=500, null=True, blank=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
