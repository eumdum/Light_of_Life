from django.db import models

class Diary(models.Model):
    content = models.TextField()  # 사용자가 작성한 일기
    emotion = models.CharField(max_length=20)  # 감정 분석 결과 (ex. '슬픔')
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return f"{self.created_at} - {self.emotion}"

# 목적 : 데이터베이스에 저장할 일기 테이블 구조를 정의

# TextField : 긴 텍스트를 저장하기 적합 (일기 내용)
# CharField : 감정 결과 저장 (ex. 행복, 슬픔 등)
# auto_now_add=True : 저장 시 자동으로 현재 시간 저장