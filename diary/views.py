from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json

from diary.main import get_diary_music_recommendation

from .models import Diary
from .serializers import DiarySerializer 
from .hf_emotion import analyze_emotion_top2

class DiaryViewSet(viewsets.ModelViewSet):
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Diary.objects.filter(author=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        diary_instance = serializer.save(author=self.request.user)
        
        diary_content = request.data.get('content')
        
        print(f"--- 허깅페이스 + 제미나이 분석 시작 ---")
        try:
            emotion_data = analyze_emotion_top2(diary_content)
            recommendation_result = get_diary_music_recommendation(diary_content)
            
        except Exception as e:
            print(f"하이브리드 분석 중 에러: {e}")
            recommendation_result = {
                "emotion": "분석 중(에러)",
                "song": "imperfect for you - ariana grande",
                "reason": "잠시 연결오류가 발생했어요. 다시 시도해주세요.",
                "url": "https://www.youtube.com/results?search_query=ariana+grande+imperfect+for+you"
            }

        diary_instance.emotion = recommendation_result.get('emotion')
        diary_instance.recommendation_song = recommendation_result.get('song')
        diary_instance.recommendation_reason = recommendation_result.get('reason')
        diary_instance.youtube_url = recommendation_result.get('url')
        diary_instance.save() 

        final_serializer = self.get_serializer(diary_instance)
        response_data = final_serializer.data
        response_data['recommendation'] = {
            'emotion': diary_instance.emotion,
            'recommendation_song': diary_instance.recommendation_song,
            'recommendation_reason': diary_instance.recommendation_reason,
            'youtube_url': diary_instance.youtube_url
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny]) 
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    
    if User.objects.filter(username=username).exists():
        return Response({'message': '이미 존재하는 아이디입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
    user = User.objects.create_user(username=username, password=password, email=email)
    return Response({'message': '회원가입 성공'}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def analyze_emotion_api(request):
    text = request.data.get("content", "")

    if not text.strip():
        return Response(
            {"detail": "content를 입력하세요."},
            status=status.HTTP_400_BAD_REQUEST
        )

    result = analyze_emotion_top2(text)
    return Response(result, status=status.HTTP_200_OK)


@csrf_exempt
def analyze_diary(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        diary_content = data.get('content')
        
        result = get_diary_music_recommendation(diary_content)
        
        if result:
            return JsonResponse(result) 
        else:
            return JsonResponse({"error": "분석 실패"}, status=500)