from rest_framework import serializers
from .models import Diary

class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['id', 'title', 'content', 'date', 'created_at', 'updated_at', 'emotion']
        read_only_fields = ['date', 'created_at', 'updated_at', 'emotion']
