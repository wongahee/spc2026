# ollama pull exaone3.5:2.4b
# ollama pull qwen2.5:1.5b

import requests

MODEL_NAME = "exaone3.4:latest"
# MODEL_NAME = "qwen2.5:1.5b"
# MODEL_NAME = "exaone3.4:2.4b"

def ask_qwen(question):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": question,
            "stream": False
        }
    )

    data = response.json()
    return data['response']

# print(ask_qwen("당신을 소개해주세요."))
# print(ask_qwen("인공지능이란 무엇인가요?"))

# 무한 질문 가능한 챗봇
while True:
    user_input = input("나: ")
    if user_input == "exit":
        print("종료합니다.")
        break

    print("응답: ", ask_qwen(user_input))