from functools import lru_cache
from transformers import pipeline

MODEL_NAME = "LimYeri/HowRU-KoELECTRA-Emotion-Classifier"


@lru_cache(maxsize=1)
def get_emotion_classifier():
    classifier = pipeline(
        "text-classification",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME,
        top_k=None,   
    )
    return classifier


def analyze_emotion_top2(text: str) -> dict:
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

    if results and isinstance(results[0], list):
        results = results[0]

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