from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DiaryViewSet, signup # analyze_emotion_api 등 삭제

router = DefaultRouter()
router.register(r"diaries", DiaryViewSet, basename="diary")

urlpatterns = [
    path("", include(router.urls)),
    path("signup/", signup, name="signup"),
]
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from .views import DiaryViewSet, analyze_emotion_api, analyze_diary, signup

# router = DefaultRouter()
# router.register(r"diaries", DiaryViewSet, basename="diary")

# urlpatterns = [
#     path("", include(router.urls)),
#     path('analyze/', analyze_diary, name='analyze_diary'),

#     # [추가] 감정분석 결과만 테스트하는 API
#     path("analyze-emotion/", analyze_emotion_api, name="analyze-emotion"),
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('api/signup/', signup),

# ]