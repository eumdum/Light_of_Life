import os
import json
from google import genai
from django.conf import settings

client = genai.Client(api_key=settings.GOOGLE_API_KEY)

def get_diary_music_recommendation(diary_text):
    prompt = f"""
    다음은 사용자가 쓴 일기 내용이야:
    "{diary_text}"

    이 일기를 읽고 사용자가 느끼는 감정을 깊이 있게 분석해서, 그 상황에 꼭 어울리는 실존하는 노래 1곡을 추천해줘.
    절대로 없는 노래를 지어내지 마.

    반드시 아래 JSON 형식을 엄격히 지켜서 응답해:
    1. emotion: 분석된 주요 감정을 10자 이내의 짧은 단어나 구절로 작성 (예: "지친 하루의 끝", "설레는 시작")
    2. recommendation_song: "곡 제목 - 가수명"
    3. recommendation_reason: 일기 내용에서 파악된 사용자의 구체적인 상황과 감정을 언급하며, 왜 이 곡이 위로가 되거나 공감이 될지 상세히 설명해줘.
    4. youtube_url: "https://www.youtube.com/results?search_query=가수명+곡제목"

    형식 예시: 
    {{
    "emotion": "감정 요약",
    "recommendation_song": "노래제목 - 가수",
    "recommendation_reason": "당신의 일기를 보니 ...한 상황이군요. 이 곡의 가사는 ...해서 당신에게 힘이 될 거예요.",
    "youtube_url": "유튜브링크"
    }}
    """

    print(f"--- [실험] 제미나이 단독 분석 가동 ---")

    try:
        res = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
            }
        )
        
        raw_text = res.text
        start_idx = raw_text.find('{')
        end_idx = raw_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx != 0:
            clean_json = raw_text[start_idx:end_idx]
        else:
            clean_json = raw_text.strip()

        result = json.loads(clean_json) 
        
        print("--- 제미나이 최종 결과물 ---")
        print(result)

        return {
            'emotion': result.get('emotion'),
            'recommendation_song': result.get('recommendation_song'), 
            'recommendation_reason': result.get('recommendation_reason'),
            'youtube_url': result.get('youtube_url')
        }

    except Exception as error:
        print(f"API 호출 중 오류 발생: {error}")
        return {
            'emotion': "분석 실패",
            'recommendation_song': "추천 실패",
            'recommendation_reason': "API 응답 오류가 발생했습니다.",
            'youtube_url': "#"
        }