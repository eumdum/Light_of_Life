from django.db import models
from datetime import date

class Diary(models.Model):
    title = models.CharField(max_length=200, default="기본제목")
    content = models.TextField(default="")
    date = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 사전대조 감정분석 방식
    emotion = models.CharField(max_length=20, blank=True, null=True)

    # 대표 감정(top1)
    emotion_label = models.CharField(max_length=50, blank=True, null=True)
    emotion_score = models.FloatField(blank=True, null=True)

    # 보조 감정(top2)
    sub_emotion_label = models.CharField(max_length=50, blank=True, null=True)
    sub_emotion_score = models.FloatField(blank=True, null=True)

    # 전체 감정 분포 저장
    emotion_raw = models.JSONField(blank=True, null=True)

    # [다음 단계 LLM용]
    keywords = models.JSONField(blank=True, null=True)
    emotion_summary = models.TextField(blank=True, null=True)
    recommendation_reason = models.TextField(blank=True, null=True)
    music_query = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return f"{self.title} ({self.date})"

