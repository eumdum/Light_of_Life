# 목적 : views.py와 외부주소를 연결하는 역할.
# 라우터는 a,b 두줄만 사용해서 장고가 자동으로 조회, 생성, 수정, 삭제등과 관련된 코드를 자동으로 짜줌.

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DiaryViewSet 

# 라우터를 사용하여 /diaries/ 경로를 설정
router = DefaultRouter()                    # a, 자동 주소생성기 가동.
router.register(r'diaries', DiaryViewSet)   # b, diaries라는 루트주소를 주고, 이 주소에 대한 모든 처리는 DiaryViewSet에게 맡김.

# diary 앱과 관련된 URL만 남겨두고 하나로 합침
urlpatterns = [
    path('', include(router.urls)),         # back/urls.py에서 /api/를 전달받았고 바로 위 라우터에서 넘겨진 것과 더해 /api/diaries/라는 최종 주소가 완성됨.
]
