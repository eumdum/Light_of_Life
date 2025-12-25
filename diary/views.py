#일기 저장, 감정 분석, db저장


from rest_framework import viewsets 
from .models import Diary
from .serializers import DiarySerializer
from .emotion_analyzer import analyze_emotion
    #ㄴ> 얘가 특허의 ai로직을 담은 파일임.(감정을 views.py에서 분석하는게 아니라 analyze_emotion함수에서 구현)

class DiaryViewSet(viewsets.ModelViewSet):
    queryset = Diary.objects.all().order_by('-created_at') # 최신순으로 정렬.
    serializer_class = DiarySerializer

    # 특허로직!
    # post 요청(새 일기 저장)을 처리할 때 특별한 작업을 추가하기 위해
    # perform_create 메소드를 오버라이딩(재정의)함.
    def perform_create(self, serializer):
        # 사용자가 입력한 '내용'을 가져옴.
        # serializer.validated_data는 유효성검사를 통과한 데이터임.
        content = serializer.validated_data.get('content', '')

        # 감정 분석 실행
        emotion_result = analyze_emotion(content)

        # 분석 결과를 'emotion' 필드에 담아 함께 저장
        serializer.save(emotion=emotion_result)
        