# Vision 방법
# 1. 사진 올리기 (base64 인코딩)
# 2. 이미지 URL을 주고 읽도록 함

import os
import base64

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()   # OpenAI: 1회성, 단발성 요구 시 사용

image_url = 'poster.jpg'

def encode_image(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def ask_about_image(question, b64):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': question},
                    {'type': 'image_url', 'image_url': {'url': f'data:image/jpg;base64,{b64}'}}   # 이미지 유형에 따라 인코딩된 포맷 바꿔서 설정
                    # {'type': 'image_url', 'image_url': {'url': f'data:image/webp;base64,{b64}'}}   # 이미지 유형에 따라 인코딩된 포맷 바꿔서 설정
                ]
            }
        ]
    )
    return response.choices[0].message.content

questions = [
    '이미지에 있는 한글 글자를 다 읽어줘. 해설 빼고 OCR 기반으로 글자만 읽어줘',
    '해당 이미지에 사용된 주요 색상을 알려줘',
    '이미지의 전체 분위기를 한 문장으로 표현한다면?'
]

b64 = encode_image(image_url)

for q in questions:
    print('-' * 60)
    print(f"질문: {q}")
    print(f"답변: {ask_about_image(q, b64)}")
