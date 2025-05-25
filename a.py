from transformers import pipeline
import os

# 심볼릭 링크 경고 비활성화 (선택 사항)
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# 모델 이름 (매우 인기 있는 영문 감정 분석 모델)
model_name = "distilbert-base-uncased-finetuned-sst-2-english"

print(f"테스트 시작: 모델 '{model_name}'을 사용하여 파이프라인을 생성합니다.")

try:
    # 1. 파이프라인을 통해 모델과 토크나이저를 로드하고 파이프라인 생성
    #    가장 간단한 방법입니다. 내부적으로 AutoModel, AutoTokenizer를 사용합니다.
    classifier = pipeline("sentiment-analysis", model=model_name)
    print("파이프라인 생성 성공!")

    # 테스트 문장
    text1 = "I love using Hugging Face transformers! It's so easy."
    text2 = "I really hate it when my code doesn't work."

    print(f"문장 1 분석: \"{text1}\"")
    result1 = classifier(text1)
    print("결과 1:", result1)

    print(f"문장 2 분석: \"{text2}\"")
    result2 = classifier(text2)
    print("결과 2:", result2)

    print("테스트 성공!")

except Exception as e:
    print(f"오류 발생: {e}")
    import traceback
    traceback.print_exc()