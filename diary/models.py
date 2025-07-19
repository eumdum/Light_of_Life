from django.db import models
# from django.contrib.auth.models import User
from datetime import date

class Diary(models.Model):
    title = models.CharField(max_length=200, default="기본제목")
    content = models.TextField(default="")
    date = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    emotion = models.CharField(max_length=20, blank=True, null=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diary_entries', null=True)
    
    class Meta:
        ordering = ['-date'] # 최신 날짜순으로 정렬
        
    def __str__(self):
        return f"{self.title} ({self.date})"

# class Diary(models.Model):
#     content = models.TextField()  # 사용자가 작성한 일기
#     emotion = models.CharField(max_length=20)  # 감정 분석 결과 (ex. '슬픔')
#     created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

#     def __str__(self):
#         return f"{self.created_at} - {self.emotion}"

# 목적 : 데이터베이스에 저장할 일기 테이블 구조를 정의

# TextField : 긴 텍스트를 저장하기 적합 (일기 내용)
# CharField : 감정 결과 저장 (ex. 행복, 슬픔 등)
# auto_now_add=True : 저장 시 자동으로 현재 시간 저장