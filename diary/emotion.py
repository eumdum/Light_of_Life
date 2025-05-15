from transformers import pipeline

# Hugging Face 감정 분석기 (간단한 사전학습 모델)
classifier = pipeline("sentiment-analysis")

def analyze_emotion(text):
    result = classifier(text)[0]
    label = result['label']
    score = result['score']

    # 예시 매핑 (Hugging Face 모델은 'POSITIVE'/'NEGATIVE'만 있을 수 있음)
    if label == "POSITIVE":
        return "행복"
    elif label == "NEGATIVE":
        return "슬픔"
    else:
        return "중립"

# 목적 : 일기 내용을 감정 분석해서 emotion에 저장할 값 만들기

