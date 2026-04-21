from rest_framework import serializers
from .models import Diary

class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = [
            'id', 
            'title', 
            'content', 
            'date', 
            'created_at', 
            'updated_at', 
            'emotion',

            # top1, top2, 전체감정
            "emotion_label",
            "emotion_score",
            "sub_emotion_label",
            "sub_emotion_score",
            "emotion_raw",

            # [다음 단계 LLM용]
            "keywords",
            "emotion_summary",
            "recommendation_reason",
            "music_query",
            ]

        read_only_fields = [
            'date', 
            'created_at', 
            'updated_at', 
            'emotion',
            "emotion_label",
            "emotion_score",
            "sub_emotion_label",
            "sub_emotion_score",
            "emotion_raw",
            "keywords",
            "emotion_summary",
            "recommendation_reason",
            "music_query",
            
            ]
