from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DiaryViewSet, signup

router = DefaultRouter()
router.register(r"diaries", DiaryViewSet, basename="diary")

urlpatterns = [
    path("", include(router.urls)),
    path("signup/", signup, name="signup"),
]