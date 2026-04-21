import requests
import json

url = "http://127.0.0.1:8000/api/analyze-emotion/"
data = {
    "content": "요즘 너무 지치고 슬프다."
}

res = requests.post(url, json=data)
print(res.status_code)
print(json.dumps(res.json(), ensure_ascii=False, indent=2))