from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DiaryViewSet, analyze_emotion_api

router = DefaultRouter()
router.register(r"diaries", DiaryViewSet)

urlpatterns = [
    path("", include(router.urls)),

    # [추가] 감정분석 결과만 테스트하는 API
    path("analyze-emotion/", analyze_emotion_api, name="analyze-emotion"),
]