import json
import os
from konlpy.tag import Okt
from .emotion_d import BOOSTER_DICT, NEGATION_LIST, REPLACE_DICT, CUSTOM_SCORE_DICT

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    knu_senti_dict_path = os.path.join(BASE_DIR, "SentiWord_info.json")
    knu_senti_dict = {}

    with open(knu_senti_dict_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data:
            knu_senti_dict[item["word_root"]] = int(item["polarity"])
except FileNotFoundError:
    print("Error: SentiWord_info.json 파일을 diary 폴더에 넣어주세요.")
    knu_senti_dict = {}

okt = Okt()

# 조사/대명사/의미 약한 일반어 제거
STOPWORDS = {
    "이", "가", "은", "는", "을", "를", "에", "의", "와", "과", "도", "로", "으로",
    "나", "너", "저", "그", "것", "수", "등", "좀", "더", "또", "진짜", "약간",
    "오늘", "어제", "내일", "사람"
}

# 감정 분석에 쓸 품사만 제한
ALLOWED_POS = {"Noun", "Verb", "Adjective", "Adverb"}

# 감정과 거의 무관한 일반 명사 제외
BLOCKED_NOUNS = {
    "사람", "생각", "상황", "문제", "때", "것", "수", "오늘", "어제", "내일"
}


def analyze_emotion(text: str) -> str:
    print(f'\n===== "{text}" 분석 시작 =====')

    for old_word, new_word in REPLACE_DICT.items():
        text = text.replace(old_word, new_word)

    morphs = okt.pos(text, stem=True)
    print(f"2. 형태소 분석 결과: {morphs}")

    total_score = 0
    negation_flag = False
    detected_words = []

    for i, (word, pos) in enumerate(morphs):
        if word in NEGATION_LIST:
            negation_flag = True
            continue

        if pos not in ALLOWED_POS:
            if negation_flag:
                negation_flag = False
            continue

        if word in STOPWORDS:
            if negation_flag:
                negation_flag = False
            continue

        if len(word) < 2 and word not in CUSTOM_SCORE_DICT:
            if negation_flag:
                negation_flag = False
            continue

        if pos == "Noun" and word in BLOCKED_NOUNS:
            if negation_flag:
                negation_flag = False
            continue

        # 커스텀 사전 우선
        if word in CUSTOM_SCORE_DICT:
            score = CUSTOM_SCORE_DICT[word]
            original_score = score

            if i > 0:
                prev_word = morphs[i - 1][0]
                if prev_word in BOOSTER_DICT:
                    score *= BOOSTER_DICT[prev_word]

            if negation_flag:
                score *= -1
                negation_flag = False

            total_score += score
            detected_words.append(
                f" - [커스텀] '{word}', 기본점수: {original_score}, 최종점수: {score:.2f}"
            )
            continue
        
        # 일반 감성 사전
        score = knu_senti_dict.get(word, 0)

        if score == 0:
            if negation_flag:
                negation_flag = False
            continue

        original_score = score

        if i > 0:
            prev_word = morphs[i - 1][0]
            if prev_word in BOOSTER_DICT:
                score *= BOOSTER_DICT[prev_word]

        if negation_flag:
            score *= -1
            negation_flag = False

        total_score += score
        detected_words.append(
            f" - [일반] '{word}', 기본점수: {original_score}, 최종점수: {score:.2f}"
        )

    print("3. 감지된 단어 및 점수 계산:")
    if not detected_words:
        print(" - 감지된 감정 단어 없음")
    else:
        for line in detected_words:
            print(line)

    print(f"4. 최종 점수: {total_score}")

    if total_score >= 3:
        result = "행복"
    elif total_score >= 1:
        result = "평온"
    elif total_score <= -3:
        result = "분노"
    elif total_score <= -1:
        result = "슬픔"
    else:
        result = "중립"

    print(f"5. 최종 감정: {result}")
    print("=" * 30)
    return result