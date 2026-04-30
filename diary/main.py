import os
import json
from google import genai
from diary.hf_emotion import analyze_emotion_top2


client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_diary_music_recommendation(diary_text):
    emotion_data = analyze_emotion_top2(diary_text)
    top1 = emotion_data['top1_label']
    top2 = emotion_data['top2_label']
    
    prompt = f"""
    사용자의 일기: {diary_text}
    주요 감정: {top1}, 보조 감정: {top2}

    위의 두 감정이 섞인 사용자의 상태를 분석하고, 실제로 존재하는 노래 1곡을 추천해줘.
    절대로 없는 노래를 지어내지 마.

    반드시 아래 JSON 형식을 엄격히 지켜서 응답해:
    1. emotion: "{top1}와 {top2} 사이" 처럼 10자 이내의 짧은 요약문으로만 작성 (문장 금지)
    2. song: "곡 제목 - 가수명" (실존하는 곡)
    3. reason: 사용자의 복합적인 감정에 대한 깊이 있는 분석과 이 곡을 추천하는 이유를 상세히 설명 (길어도 됨)
    4. url: "https://www.youtube.com/results?search_query=가수명+곡제목"

    형식 예시: 
    {{
    "emotion": "{top1}와 {top2}의 혼란",
    "song": "노래제목 - 가수",
    "reason": "당신은 현재 ...해서 이런 감정을 느끼고 있군요. 이 곡은 ...한 분위기라 당신에게 위로가 될 거예요.",
    "url": "유튜브링크"
    }}
    """

    print(f"--- 분석 감정: {top1}, {top2} / 제미나이 가동 ---")

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash", 
            contents=prompt
        )
        
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        result = json.loads(clean_text)
        return result

    except Exception as e:
        print(f"오류 발생: {e}")
        return None

if __name__ == "__main__":
    user_input = "점심으로 버거킹 쉬림프 와퍼를 먹었는데 생각보다 너무 매웠다..."
    res = get_diary_music_recommendation(user_input)
    if res:
        print(f"\n🎵 추천곡: {res['song']}")
        print(f"💡 이유: {res['reason']}")
        print(f"🔗 링크: {res['url']}")