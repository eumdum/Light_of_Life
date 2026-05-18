from django.urls import path, include
from rest_framework.routers import DefaultRouter
<<<<<<< Updated upstream
from .views import DiaryViewSet, analyze_emotion_api, analyze_diary
=======
from .views import DiaryViewSet, signup
>>>>>>> Stashed changes

router = DefaultRouter()
router.register(r"diaries", DiaryViewSet)

urlpatterns = [
    path("", include(router.urls)),
<<<<<<< Updated upstream
    path('analyze/', analyze_diary, name='analyze_diary'),

    # [추가] 감정분석 결과만 테스트하는 API
    path("analyze-emotion/", analyze_emotion_api, name="analyze-emotion"),
=======
    path("signup/", signup, name="signup"),
>>>>>>> Stashed changes
]