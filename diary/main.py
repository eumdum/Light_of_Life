import os
import json
from google import genai
# from diary.hf_emotion import analyze_emotion_top2  # 실험을 위해 잠시 주석 처리

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_diary_music_recommendation(diary_text):
    # --- [실험용] 허깅페이스 로직 주석 처리 ---
    # emotion_data = analyze_emotion_top2(diary_text)
    # top1 = emotion_data['top1_label']
    # top2 = emotion_data['top2_label']
    
    # --- 제미나이 단독 분석 프롬프트 ---
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
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
            }
        )
        
        raw_text = response.text
        start_idx = raw_text.find('{')
        end_idx = raw_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx != 0:
            clean_json = raw_text[start_idx:end_idx]
        else:
            clean_json = raw_text.strip()

        # JSON 응답 파싱
        result = json.loads(clean_json) # 변수명 주의: clean_json을 파싱해야 해!
        
        # [체크!] 터미널에 이 내용이 찍히는지 확인해봐
        print("--- 제미나이 최종 결과물 ---")
        print(result)

        return {
            'emotion': result.get('emotion'),
            'recommendation_song': result.get('recommendation_song'), 
            'recommendation_reason': result.get('recommendation_reason'),
            'youtube_url': result.get('youtube_url')
        }

    except Exception as e:
        print(f"API 호출 중 오류 발생: {e}")
        return {
            'emotion': "분석 실패",
            'recommendation_song': "추천 실패",
            'recommendation_reason': "API 응답 오류가 발생했습니다.",
            'youtube_url': "#"
        }

# import os
# import json
# from google import genai
# from diary.hf_emotion import analyze_emotion_top2


# client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_diary_music_recommendation(diary_text):
#     emotion_data = analyze_emotion_top2(diary_text)
#     top1 = emotion_data['top1_label']
#     top2 = emotion_data['top2_label']
    
#     prompt = f"""
#     사용자의 일기: {diary_text}
#     주요 감정: {top1}, 보조 감정: {top2}

#     위의 두 감정이 섞인 사용자의 상태를 분석하고, 실제로 존재하는 노래 1곡을 추천해줘.
#     절대로 없는 노래를 지어내지 마.

#     반드시 아래 JSON 형식을 엄격히 지켜서 응답해:
#     1. emotion: "{top1}와 {top2} 사이" 처럼 10자 이내의 짧은 요약문으로만 작성 (문장 금지)
#     2. song: "곡 제목 - 가수명" (실존하는 곡)
#     3. reason: 사용자의 복합적인 감정에 대한 깊이 있는 분석과 이 곡을 추천하는 이유를 상세히 설명 (길어도 됨)
#     4. url: "https://www.youtube.com/results?search_query=가수명+곡제목"

#     형식 예시: 
#     {{
#     "emotion": "{top1}와 {top2}의 혼란",
#     "song": "노래제목 - 가수",
#     "reason": "당신은 현재 ...해서 이런 감정을 느끼고 있군요. 이 곡은 ...한 분위기라 당신에게 위로가 될 거예요.",
#     "url": "유튜브링크"
#     }}
#     """

#     print(f"--- 분석 감정: {top1}, {top2} / 제미나이 가동 ---")

#     try:
#         # [수정] 리스트에 있었던 구체적인 모델명을 사용하자
#         response = client.models.generate_content(
#             model="models/gemini-2.5-flash", 
#             contents=prompt
#         )
        
#         # 마크다운 기호 제거 후 JSON 파싱
#         clean_text = response.text.replace('```json', '').replace('```', '').strip()
#         result = json.loads(clean_text)
#         return result

#     except Exception as e:
#         print(f"오류 발생: {e}")
#         return None

# if __name__ == "__main__":
#     user_input = "점심으로 버거킹 쉬림프 와퍼를 먹었는데 생각보다 너무 매웠고 새우를 세번 추가한거에 비해서 너무 작았다..."
#     res = get_diary_music_recommendation(user_input)
#     if res:
#         print(f"\n🎵 추천곡: {res['song']}")
#         print(f"💡 이유: {res['reason']}")
#         print(f"🔗 링크: {res['url']}")