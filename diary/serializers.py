# 번역기/응답부서
# 장고 객체(content, title 등등)를 프론트와 주고받기 위해 JSON형태로 변환해주는 도구


from rest_framework import serializers      #serializers안에 modelserializer이 있는거임.
from .models import Diary                   #번역할 원본 데이터를 가져옴.

# models에서 정의한 테이블구조와 일치하는지 검증
class DiarySerializer(serializers.ModelSerializer):     # ModelSerializer: 자동으로 모델 필드를 JSON으로 변환해줌.
    class Meta:
        model = Diary
        fields = ['id', 'title', 'content', 'date', 'created_at', 'updated_at', 'emotion']
        read_only_fields = ['date', 'created_at', 'updated_at', 'emotion']
        