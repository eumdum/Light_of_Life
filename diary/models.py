from django.db import models
from datetime import date

class Diary(models.Model):
    title = models.CharField(max_length=200, default="기본제목")
    content = models.TextField(default="")
    date = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    emotion = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return f"{self.title} ({self.date})"

