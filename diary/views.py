from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from diary.main import get_diary_music_recommendation

from .models import Diary
from .serializers import DiarySerializer 
from .hf_emotion import analyze_emotion_top2

class DiaryViewSet(viewsets.ModelViewSet):
    queryset = Diary.objects.all().order_by("-created_at")
    serializer_class = DiarySerializer

    def perform_create(self, serializer):
        """
        [왜 필요?]
        일기 저장할 때 Hugging Face 감정분석도 같이 수행해서
        DB에 top1 / top2 / raw 결과 저장
        """
        content = serializer.validated_data.get("content", "")

        emotion_result = analyze_emotion_top2(content)

        serializer.save(
            # [기존 필드 호환용]
            emotion=emotion_result["top1_label"],

            # [새 필드]
            emotion_label=emotion_result["top1_label"],
            emotion_score=emotion_result["top1_score"],
            sub_emotion_label=emotion_result["top2_label"],
            sub_emotion_score=emotion_result["top2_score"],
            emotion_raw=emotion_result["raw"],
        )


@api_view(["POST"])
def analyze_emotion_api(request):
    """
    [왜 필요?]
    DB 저장 전에 감정분석 결과만 먼저 확인하는 테스트용 API
    """
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
        
        # 우리가 성공했던 그 함수 호출!
        result = get_diary_music_recommendation(diary_content)
        
        if result:
            return JsonResponse(result) # 결과가 이미 JSON 형태라면 바로 반환
        else:
            return JsonResponse({"error": "분석 실패"}, status=500)