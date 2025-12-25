from rest_framework import viewsets #, permissions, generics
# from django.contrib.auth.models import User
from .models import Store
from .serializers import StoreSerializer #, UserSerializer
from .emotion_analyzer import analyze_emotion
from .vision_analyzer import analyze_product_image

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all().order_by('-created_at')
    serializer_class = StoreSerializer
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_queryset(self):
#         # 현재 로그인한 사용자의 일기만 반환
#         return Diary.objects.filter(user=self.request.user)

    # post 요청(새 일기 저장)을 처리할 때 특별한 작업을 추가하기 위해
    # perform_create 메소드를 오버라이딩(재정의)함.
    def perform_create(self, serializer):
        # 사용자가 입력한 '내용'을 가져옴.
        # serializer.validated_data는 유효성검사를 통과한 데이터임.
        content = serializer.validated_data.get('content', '')
        image = serializer.validated_data.get('image', None)  # 이미지 필드가 있다고 가정

        # 감정 분석 실행
        emotion_result = analyze_emotion(content)
        # 상품 이미지 분석 실행
        product_result = analyze_product_image(image)
        item = product_result.get('item')
        price = product_result.get('price')
        confidence = product_result.get('confidence')

        # 분석 결과를 'emotion', 'item', 'price', 'confidence' 필드에 담아서 함께 저장
        serializer.save(emotion=emotion_result, item=item, price=price, confidence=confidence)

# class UserRegistrationView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.AllowAny]