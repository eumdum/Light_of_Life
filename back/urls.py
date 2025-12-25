# 목적 : api경로 설정
#       프로젝트의 메인 URL 설정파일, 모든 외부 요청을 어느 앱으로 보낼지 결정.

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),      # /admin/으로 들어오는 요청은 장고 관리자페이지로 보냄.
    path('api/', include('diary.urls')),  # /api/로 시작하는 모든 요청은 diary.urls로 전달
]
