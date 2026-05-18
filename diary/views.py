from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from .models import Diary
from .serializers import DiarySerializer
from diary.main import get_diary_music_recommendation

class DiaryViewSet(viewsets.ModelViewSet):
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Diary.objects.all().order_by("-created_at")
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        diary_instance = serializer.save(author=self.request.user)
        
        diary_content = request.data.get('content', '')
        
        print(f"--- 분석 시작: {diary_content[:20]}... ---")
        try:
            recommendation_result = get_diary_music_recommendation(diary_content)
        
            diary_instance.emotion = recommendation_result.get('emotion')
            diary_instance.recommendation_song = recommendation_result.get('recommendation_song')
            diary_instance.recommendation_reason = recommendation_result.get('recommendation_reason')
            diary_instance.youtube_url = recommendation_result.get('youtube_url')
            diary_instance.save()

            final_data = self.get_serializer(diary_instance).data
            final_data['recommendation'] = recommendation_result
            
            return Response(final_data, status=status.HTTP_201_CREATED)

        except Exception as error:
            print(f"분석 중 에러 발생: {error}")
            return Response(self.get_serializer(diary_instance).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if User.objects.filter(username=username).exists():
        return Response({'message': '이미 존재하는 아이디입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
    User.objects.create_user(username=username, password=password)
    return Response({'message': '회원가입 성공'}, status=status.HTTP_201_CREATED)