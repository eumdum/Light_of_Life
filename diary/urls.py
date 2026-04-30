from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import DiaryViewSet, analyze_emotion_api, analyze_diary, signup

router = DefaultRouter()
router.register(r"diaries", DiaryViewSet, basename="diary")

urlpatterns = [
    path("", include(router.urls)),
    path('analyze/', analyze_diary, name='analyze_diary'),
    path("analyze-emotion/", analyze_emotion_api, name="analyze-emotion"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/signup/', signup),
]