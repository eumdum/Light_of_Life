import os
import json
# from dotenv import load_dotenv
from google import genai
<<<<<<< Updated upstream
from diary.hf_emotion import analyze_emotion_top2

# load_dotenv()
=======
from django.conf import settings
>>>>>>> Stashed changes

client = genai.Client(api_key=settings.GOOGLE_API_KEY)

def get_diary_music_recommendation(diary_text):
<<<<<<< Updated upstream
    emotion_data = analyze_emotion_top2(diary_text)
    top1 = emotion_data['top1_label']
    
    # main.py 프롬프트 수정
=======
>>>>>>> Stashed changes
    prompt = f"""
    사용자의 일기: {diary_text}
    감정 분석 결과: {top1}

    이 상황에 어울리는 노래 1곡을 추천하고 이유와 유튜브 검색 링크를 JSON으로 줘.
    유튜브 링크는 반드시 아래 형식을 지켜줘:
    "url": "https://www.youtube.com/results?search_query=가수명+곡제목"

    형식: {{"song": "제목-가수", "reason": "이유", "url": "유튜브링크"}}
    """

    print(f"--- 분석 감정: {top1} / 제미나이 가동 ---")

    try:
<<<<<<< Updated upstream
        # [수정] 리스트에 있었던 구체적인 모델명을 사용하자
        response = client.models.generate_content(
            model="models/gemini-2.5-flash", 
            contents=prompt
        )
        
        # 마크다운 기호 제거 후 JSON 파싱
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        result = json.loads(clean_text)
        return result

    except Exception as e:
        print(f"오류 발생: {e}")
        return None

if __name__ == "__main__":
    user_input = "점심으로 버거킹 쉬림프 와퍼를 먹었는데 생각보다 너무 매웠고 새우를 세번 추가한거에 비해서 너무 작았다..."
    res = get_diary_music_recommendation(user_input)
    if res:
        print(f"\n🎵 추천곡: {res['song']}")
        print(f"💡 이유: {res['reason']}")
        print(f"🔗 링크: {res['url']}")
=======
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
>>>>>>> Stashed changes
