from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from .models import Diary
from .serializers import DiarySerializer
from diary.main import get_diary_music_recommendation # 서버 시작 시 로드

class DiaryViewSet(viewsets.ModelViewSet):
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Diary.objects.all().order_by("-created_at")
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 현재 유저를 저자로 저장
        diary_instance = serializer.save(author=self.request.user)
        
        diary_content = request.data.get('content', '')
        
        print(f"--- 분석 시작: {diary_content[:20]}... ---")
        try:
            # 분석 실행
            recommendation_result = get_diary_music_recommendation(diary_content)
            
            # DB 필드 업데이트
            diary_instance.emotion = recommendation_result.get('emotion')
            diary_instance.recommendation_song = recommendation_result.get('recommendation_song')
            diary_instance.recommendation_reason = recommendation_result.get('recommendation_reason')
            diary_instance.youtube_url = recommendation_result.get('youtube_url')
            diary_instance.save()

            # 프론트엔드가 사용할 수 있게 결과 포함해서 응답
            final_data = self.get_serializer(diary_instance).data
            final_data['recommendation'] = recommendation_result
            
            return Response(final_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"분석 중 에러 발생: {e}")
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
# from rest_framework import viewsets, status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, AllowAny
# # from django.http import JsonResponse
# # from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.models import User
# # import json

# from diary.main import get_diary_music_recommendation

# from .models import Diary
# from .serializers import DiarySerializer 
# # from .hf_emotion import analyze_emotion_top2

# class DiaryViewSet(viewsets.ModelViewSet):
#     queryset = Diary.objects.all().order_by("-created_at")
#     serializer_class = DiarySerializer

#     def create(self, request, *args, **kwargs):
#         # 1. 일기 저장 (기존 로직)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # self.perform_create 대신 직접 객체를 받아서 나중에 업데이트할 준비를 해!
#         diary_instance = serializer.save()
        
#         diary_content = request.data.get('content')
        
#         # 2. 제미나이 분석 실행 (에러 대비 처리 추가)
#         print(f"--- 분석 시작: {diary_content[:20]}... ---")
#         try:

#             # raise Exception("테스트용 에러 발생!")
            
#             recommendation_result = get_diary_music_recommendation(diary_content)
#         except Exception as e:
#             print(f"분석 중 에러 발생: {e}")
#             # 분석 실패 시 기본값 (사용자에게 에러창 대신 부드러운 위로를 줌)
#             recommendation_result = {
#                 "emotion": "당혹(에러)",
#                 "song": "imperfect for you - ariana grande",
#                 "reason": "AI 분석 중 잠시 오류가 발생했지만, 당신의 하루를 진심으로 응원해요.",
#                 "url": "https://www.youtube.com/results?search_query=ariana grande+imperfect for you"
#             }

#         # 3. [핵심] 분석 결과를 DB 모델 필드에 업데이트
#         # (주의: models.py에 emotion, recommendation_song 등의 필드가 있어야 해!)
#         diary_instance.emotion = recommendation_result.get('emotion')
#         diary_instance.recommendation_song = recommendation_result.get('song')
#         diary_instance.recommendation_reason = recommendation_result.get('reason')
#         diary_instance.youtube_url = recommendation_result.get('url')
#         diary_instance.save() # 최종적으로 DB에 저장!

#         final_serializer = self.get_serializer(diary_instance)

#         # 4. 분석 결과를 포함해서 응답
#         response_data = final_serializer.data
#         response_data['recommendation'] = {
#             'emotion': diary_instance.emotion,
#             'recommendation_song': diary_instance.recommendation_song,
#             'recommendation_reason': diary_instance.recommendation_reason,
#             'youtube_url': diary_instance.youtube_url
#         }
        
#         return Response(response_data, status=status.HTTP_201_CREATED)


# class DiaryViewSet(viewsets.ModelViewSet):
#     serializer_class = DiarySerializer
#     permission_classes = [IsAuthenticated] # 로그인한 사람만 접근 가능

#     def get_queryset(self):
#         # 지금 로그인한 유저의 일기만 반환
#         return Diary.objects.filter(author=self.request.user).order_by('-created_at')

#     def perform_create(self, serializer):
#         # 일기 저장 시 현재 유저를 저자로 저장
#         serializer.save(author=self.request.user)


# @api_view(['POST'])
# @permission_classes([AllowAny]) # 가입은 아무나 해야 하니까!
# def signup(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     email = request.data.get('email')
    
#     if User.objects.filter(username=username).exists():
#         return Response({'message': '이미 존재하는 아이디입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
#     user = User.objects.create_user(username=username, password=password, email=email)
#     return Response({'message': '회원가입 성공'}, status=status.HTTP_201_CREATED)


# @api_view(["POST"])
# def analyze_emotion_api(request):
#     """
#     [왜 필요?]
#     DB 저장 전에 감정분석 결과만 먼저 확인하는 테스트용 API
#     """
#     text = request.data.get("content", "")

#     if not text.strip():
#         return Response(
#             {"detail": "content를 입력하세요."},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     result = analyze_emotion_top2(text)
#     return Response(result, status=status.HTTP_200_OK)


# @csrf_exempt
# def analyze_diary(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         diary_content = data.get('content')
        
#         # 우리가 성공했던 그 함수 호출!
#         result = get_diary_music_recommendation(diary_content)
        
#         if result:
#             return JsonResponse(result) # 결과가 이미 JSON 형태라면 바로 반환
#         else:
#             return JsonResponse({"error": "분석 실패"}, status=500)