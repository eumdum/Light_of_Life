from rest_framework import serializers
from .models import Diary

class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['id', 'content', 'emotion', 'created_at']

# 목적 : Django 객체(Diary)를 프론트(Vue)와 주고받기 위해 JSON 형태로 변환해주는 도구

# ModelSerializer를 쓰면 자동으로 모델 필드를 JSON으로 변환해줘
# 프론트에서 보낼 content, Django가 생성할 emotion, created_at을 포함함