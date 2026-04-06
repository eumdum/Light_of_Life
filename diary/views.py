from rest_framework import viewsets 
from .models import Diary
from .serializers import DiarySerializer 
from .emotion_analyzer import analyze_emotion

class DiaryViewSet(viewsets.ModelViewSet):
    queryset = Diary.objects.all().order_by('-created_at')
    serializer_class = DiarySerializer

    def perform_create(self, serializer):
        content = serializer.validated_data.get('content', '')
        emotion_result = analyze_emotion(content)
        serializer.save(emotion=emotion_result)
