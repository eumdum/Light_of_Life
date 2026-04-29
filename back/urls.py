from django.contrib import admin
from django.urls import path, include
from diary.views import signup  
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # 일기 관련 api
    path('api/', include('diary.urls')),  

    # 회원가입 및 토큰 주소들
    path('api/signup/', signup), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]