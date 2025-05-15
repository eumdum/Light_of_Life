from django.urls import path
from .views import DiaryListCreateView

urlpatterns = [
    path('diaries/', DiaryListCreateView.as_view(), name='diary-list-create'),
]

# 목적 : api경로 설정