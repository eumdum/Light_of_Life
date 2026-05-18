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
            "recommendation_song",
            "recommendation_reason",
            "youtube_url",
            ]

        read_only_fields = [
            'date', 
            'created_at', 
            'updated_at', 
            'emotion',
            "recommendation_song",
            "recommendation_reason",
            "youtube_url",
            ]

        fields = '__all__'
        read_only_fields = ('author',)
