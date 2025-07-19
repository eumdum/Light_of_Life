from rest_framework import viewsets #, permissions, generics
# from django.contrib.auth.models import User
from .models import Diary
from .serializers import DiarySerializer #, UserSerializer
from .emotion_analyzer import analyze_emotion

class DiaryViewSet(viewsets.ModelViewSet):
    queryset = Diary.objects.all().order_by('-created_at')
    serializer_class = DiarySerializer
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_queryset(self):
#         # 현재 로그인한 사용자의 일기만 반환
#         return Diary.objects.filter(user=self.request.user)

    # post 요청(새 일기 저장)을 처리할 때 특별한 작업을 추가하기 위해
    # perform_create 메소드를 오버라이딩(재정의)함.
    def perform_create(self, serializer):
        # 사용자가 입력한 '내용'을 가져옴.
        # serializer.validated_data는 유효성검사를 통과한 데이터임.
        content = serializer.validated_data.get('content', '')

        # 감정 분석 실행
        emotion_result = analyze_emotion(content)

        # 분석 결과를 'emotion' 필드에 담아서 함께 저장
        serializer.save(emotion=emotion_result)

# class UserRegistrationView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.AllowAny]