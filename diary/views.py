from rest_framework import generics
from .models import Diary
from .serializers import DiarySerializer
from .emotion import analyze_emotion

class DiaryListCreateView(generics.ListCreateAPIView):
    queryset = Diary.objects.all().order_by('-created_at')
    serializer_class = DiarySerializer

    def perform_create(self, serializer):
        content = self.request.data.get('content', '')
        emotion = analyze_emotion(content)
        serializer.save(emotion=emotion)

# 목적 : 프론트에서 들어온 요청을 처리하고, 감정 분석해서 응답

# ListCreateAPIView : GET(목록) + POST(저장) 둘 다 처리해주는 클래스
# perform_create : POST 요청 시 실행됨 → 감정 분석 결과를 함께 저장