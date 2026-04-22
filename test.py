import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# 최신 라이브러리 방식
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

print("--- 🔍 내 계정에서 사용 가능한 모델 리스트 ---")

try:
    # 굳이 필터링하지 않고 일단 다 뽑아보자!
    for model in client.models.list():
        print(f"모델명: {model.name}")
except Exception as e:
    print(f"리스트를 가져오는 중 오류 발생: {e}")