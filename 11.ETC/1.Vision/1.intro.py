# Vision 방법
# 1. 사진 올리기 (base64 인코딩)
# 2. 이미지 URL을 주고 읽도록 함

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()   # OpenAI: 1회성, 단발성 요구 시 사용

image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/MilkManCrop.JPG/960px-MilkManCrop.JPG'

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            'role': 'user',
            'content': [
                {'type': 'text', 'text': '이 이미지를 한국어로 설명해줘.'},
                {'type': 'image_url', 'image_url': {'url': image_url}}   # 핵심
            ]
        }
    ]
)

print(response.choices[0].message.content)