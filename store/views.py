from rest_framework import viewsets, status, parsers
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Store
from .serializers import StoreSerializer
from .vision_analyzer import analyze_product_image
import traceback

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    # [1] 최종 저장: '등록 확정하기' 버튼을 눌렀을 때 실행
    # 사장님이 모달에서 확인/수정한 최종 데이터가 들어옵니다.
    def perform_create(self, serializer):
        # 저장할 데이터 미리보기
        final_item = serializer.validated_data.get('item', '알 수 없음')
        final_price = serializer.validated_data.get('price', 0)

        # 실제 DB 저장
        serializer.save()

        # [요청하신 부분] 저장 버튼을 눌렀을 때 비로소 결과 로그를 띄웁니다.
        print("\n" + "═" * 50)
        print(f"🤖 [최종 데이터 확정] 상품명: {final_item} | 가격: {final_price}")
        print("✅ [DB 저장 성공] 매대 등록이 완료되었습니다.")
        print("═" * 50 + "\n")

    # [2] 단순 분석: 사진을 선택했을 때 실행 (저장 X)
    @action(detail=False, methods=['post'], url_path='analyze')
    def analyze(self, request):
        # 여기서는 로그를 최소화하여 '아직 저장 안 됨'을 암시합니다.
        print(f"🔍 [미리보기] 사장님이 사진({request.FILES.get('image')})을 확인하고 있습니다...")
        
        image = request.FILES.get('image')
        if not image:
            return Response({"error": "이미지가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # AI 분석 수행
            result = analyze_product_image(image)
            # 결과는 프론트엔드(모달)로만 조용히 보냅니다.
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"❌ [분석 에러] {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            print("\n🔥 [서버 내부 에러 발생] 🔥")
            print(traceback.format_exc())
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)