from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DiaryViewSet, analyze_emotion_api, analyze_diary

router = DefaultRouter()
router.register(r"diaries", DiaryViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('analyze/', analyze_diary, name='analyze_diary'),

    # [추가] 감정분석 결과만 테스트하는 API
    path("analyze-emotion/", analyze_emotion_api, name="analyze-emotion"),
]