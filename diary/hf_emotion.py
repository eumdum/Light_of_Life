from functools import lru_cache
from transformers import pipeline

# [중요] 네가 테스트 완료한 모델
MODEL_NAME = "LimYeri/HowRU-KoELECTRA-Emotion-Classifier"


@lru_cache(maxsize=1)
def get_emotion_classifier():
    """
    [왜 필요?]
    모델 로딩은 무겁기 때문에 서버 실행 중 1번만 로드되게 캐시
    """
    classifier = pipeline(
        "text-classification",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME,
        top_k=None,   # 전체 감정 점수 반환
    )
    return classifier


def analyze_emotion_top2(text: str) -> dict:
    """
    [왜 필요?]
    일기 텍스트에서
    1) 대표 감정(top1)
    2) 보조 감정(top2)
    3) 전체 감정 점수(raw)
    를 한 번에 뽑기 위한 함수
    """
    if not text or not text.strip():
        return {
            "top1_label": "평범함",
            "top1_score": 0.0,
            "top2_label": None,
            "top2_score": 0.0,
            "raw": [],
        }

    classifier = get_emotion_classifier()
    results = classifier(text)

    # [중요] top_k=None이면 [[...]] 형태로 오는 경우가 많음
    if results and isinstance(results[0], list):
        results = results[0]

    # 점수 높은 순 정렬
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    top1 = results[0] if len(results) > 0 else {"label": "평범함", "score": 0.0}
    top2 = results[1] if len(results) > 1 else {"label": None, "score": 0.0}

    return {
        "top1_label": top1["label"],
        "top1_score": round(float(top1["score"]), 4),
        "top2_label": top2["label"],
        "top2_score": round(float(top2["score"]), 4),
        "raw": [
            {
                "label": item["label"],
                "score": round(float(item["score"]), 4),
            }
            for item in results
        ],
    }