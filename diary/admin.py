from django.contrib import admin
from .models import Diary

# 관리자 페이지에 Diary 모델 등록
admin.site.register(Diary)