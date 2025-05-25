import logging
logging.basicConfig(level=logging.INFO)

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import traceback

# --- 사용할 모델 (pengsu/MLB-care-for-mind-kor) ---
model_name = "pengsu/MLB-care-for-mind-kor"
# -------------------------------------------------

# --- 감정 레이블 정의 (pengsu/MLB-care-for-mind-kor 모델 카드 및 config.json 기준) ---
ACTUAL_ID2LABEL = {
    0: "무감정",
    1: "슬픔",
    2: "기쁨",
    3: "분노"
}
# ------------------------------------

print(f"--- 모델: {model_name} 테스트 (모델 카드 참고) ---")

try:
    print(f"토크나이저 로드 중: {model_name}")
    # 모델 저장소 이름으로 토크나이저 로드 (Gemma 토크나이저 로드 예상)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        logging.info(f"Tokenizer pad_token이 없어 eos_token으로 설정: {tokenizer.pad_token}")
    print("토크나이저 로드 성공.")

    print(f"모델 로드 중: {model_name}")
    # trust_remote_code=True는 모델 저장소의 커스텀 코드 실행을 허용
    # 4-bit 양자화 모델 로드를 위해 bitsandbytes 필요
    # device_map="auto"는 accelerate 라이브러리가 장치 자동 배정
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        trust_remote_code=True, # Gemma + PEFT Sequence Classification에 필요할 수 있음
        num_labels=4,
        # device_map="auto" # GPU 사용 가능 시 자동으로 할당, CPU만 사용 시 이 줄 주석 처리 또는 device="cpu"
        # torch_dtype=torch.bfloat16 # Gemma 모델에 권장, 호환성 문제 시 float32 (기본값) 사용
    )
    # 만약 device_map="auto"를 사용하지 않고 CPU에서만 실행하려면, 위 라인 주석 처리하고 아래 사용:
    # model = AutoModelForSequenceClassification.from_pretrained(model_name, trust_remote_code=True)
    # model.to("cpu") # 명시적으로 CPU로 이동

    model.eval() # 추론 모드로 설정
    print("모델 로드 성공.")
    
    # 모델 config의 id2label과 우리가 정의한 ACTUAL_ID2LABEL 비교 (디버깅용)
    print(f"모델 config 원본 id2label: {model.config.id2label}")
    # 모델 config의 id2label이 이미 한국어 감정으로 되어 있다면, ACTUAL_ID2LABEL 대신 model.config.id2label 직접 사용 가능

    texts_to_analyze = [
        "저번에 본 영화 너무 재밌더라.",
        "오늘 정말 행복해서 날아갈 것 같아!",
        "너무 슬퍼서 눈물밖에 안나.",
        "그냥 아무렇지도 않은 평범한 날이야.",
        "화가 머리 끝까지 났어!"
    ]

    for text in texts_to_analyze:
        print(f"\n분석할 텍스트: \"{text}\"")
        
        inputs = tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=128 # 모델 카드에 명시된 최대 시퀀스 길이
        )
        
        # Gemma 모델은 일반적으로 token_type_ids를 사용하지 않음
        if 'token_type_ids' in inputs:
            # inputs.pop('token_type_ids', None) # 명시적으로 제거하거나
            pass # 모델이 알아서 무시하도록 둠

        # 입력을 모델과 동일한 장치로 이동 (device_map="auto" 사용 안 할 경우)
        # model_device = next(model.parameters()).device
        # inputs = {k: v.to(model_device) for k, v in inputs.items()}
            
        with torch.no_grad():
            outputs = model(**inputs)
        
        logits = outputs.logits
        predicted_class_id = torch.argmax(logits, dim=-1).item()

        predicted_emotion_name = ACTUAL_ID2LABEL.get(predicted_class_id, f"알 수 없는 ID ({predicted_class_id})")
        
        print(f"예측된 클래스 ID: {predicted_class_id} -> 예측된 감정: {predicted_emotion_name}")

except Exception as e:
    print(f"오류 발생: 테스트 실패.")
    print(f"오류 메시지: {e}")
    traceback.print_exc()

print(f"\n--- 테스트 종료 ---")