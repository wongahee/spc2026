# 외부에 ollama 서버가 있는 경우
# 나의 request를 api에 요청하듯이 설정

import requests

OLLAMA_HOST = "http://127.0.0.1:11434"
OLLAMA_ENDPOINT = f"{OLLAMA_HOST}/api/generate"

payload = {
    "model": "exaone3.5",
    "prompt": "파이썬으로 구현하는 헬로우 월드 코드를 보여줘.",
    "stream": False
}

response = requests.post(OLLAMA_ENDPOINT, json=payload)
data = response.json()

print("모델 응답: ", data.get("response"))