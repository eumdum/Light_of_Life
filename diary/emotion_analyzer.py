import json
import os
from konlpy.tag import Okt
from .emotion_d import BOOSTER_DICT, NEGATION_LIST, REPLACE_DICT, CUSTOM_SCORE_DICT

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    knu_senti_dict_path = os.path.join(BASE_DIR, 'SentiWord_info.json')
    knu_senti_dict = {}     # KNU 감정 사전 불러옴.
    with open(knu_senti_dict_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            knu_senti_dict[item['word_root']] = int(item['polarity'])
except FileNotFoundError:   # 만약 감정사전이 없으면 오류출력하도록 설정. 안그러면 프로그램이 멈추기때문.
    print("Error: SentiWord_info.json 파일을 back/diary/ 폴더에 넣어주세요.")
    knu_senti_dict = {}


def analyze_emotion(text: str) -> str:
    print(f"\n===== \"{text}\" 분석 시작 =====")
    
    # 1. '바꿔치기' 로직(비표준어나 따로 정의한 단어를 분석 가능한 표준단어로 바꿈.)
    for old_word, new_word in REPLACE_DICT.items():
        text = text.replace(old_word, new_word)
    
    # 2. 형태소 분석(단어의 원형으로 쪼갬.)
    okt = Okt()
    morphs = okt.pos(text, stem=True)
    print(f"2. 형태소 분석 결과: {morphs}")
    
    total_score = 0
    negation_flag = False
    detected_words = []
    
    for i, (word, pos) in enumerate(morphs):
        
        # 3. 'VIP 통로': 커스텀/암호 단어인지 먼저 확인
        if word in CUSTOM_SCORE_DICT:
            score = CUSTOM_SCORE_DICT[word]
            
            # 커스텀 단어도 부사/부정어 영향을 받도록 수정
            original_score = score
            if i > 0:
                prev_word = morphs[i-1][0]
                if prev_word in BOOSTER_DICT:
                    score *= BOOSTER_DICT[prev_word]
            if negation_flag:
                score *= -1
                
            total_score += score
            detected_words.append(f"  - [커스텀/암호] '{word}', 기본점수: {original_score}, 최종점수: {score:.2f}")
            
            # 부정어 플래그는 여기서도 관리
            if word in NEGATION_LIST:
                negation_flag = True
            else:
                negation_flag = False
            
            continue # VIP 단어는 처리했으니, 아래 로직은 건너뜀

        # 4. 일반 단어 필터링
        if len(word) < 2 or pos in ['Josa', 'Punctuation', 'Suffix', 'Foreign']:
            continue
            
        # 5. KNU 사전에서 점수 가져오기
        score = knu_senti_dict.get(word, 0)
        
        # 6. 점수 계산 (부사/부정어 처리)
        if score != 0:
            original_score = score
            if i > 0:
                prev_word = morphs[i-1][0]
                if prev_word in BOOSTER_DICT:
                    score *= BOOSTER_DICT[prev_word]
            if negation_flag:
                score *= -1

            total_score += score
            detected_words.append(f"  - [일반 단어] '{word}', 기본점수: {original_score}, 최종점수: {score:.2f}")
        
        # 7. 부정어 플래그 관리
        if word in NEGATION_LIST:
            negation_flag = True
        else:
            negation_flag = False
            
    # 8. 최종 감정 분류
    print("3. 감지된 단어 및 점수 계산:")
    if not detected_words:
        print("  - 감지된 감정 단어 없음")
    else:
        for line in detected_words:
            print(line)

    print(f"4. 최종 점수: {total_score}")

    if total_score > 3:
        result = "행복"
    elif total_score > 0:
        result = "평온"
    elif total_score < -3:
        result = "분노"
    elif total_score < 0:
        result = "슬픔"
    else:
        result = "중립"
        
    print(f"5. 최종 감정: {result}")
    print("=" * 30)
    return result
