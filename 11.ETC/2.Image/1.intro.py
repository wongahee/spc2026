# 텍스트 기반 이미지 생성 (GAN) 
# Generative Adversarial Network, 생성적 적대 신경망

# 구버전 모델 dall-e => dall-e-2 => ??
# gpt-image-1.5 또는 gpt-image-2

import os
import base64

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

# prompt = "노을 지는 해변, 잔잔한 파도, 수채화 스타일"
prompt = "노을 지는 해변, 잔잔한 파도, 파스텔톤의 수채화 스타일. 돌고래 동상을 만들어줘"

result = client.images.generate(
    model="gpt-image-1",
    prompt=prompt,
    size='1024x1024',   # 정사각형, 세로(1024x1536), 가로(1536x1024)
    quality='high'
)

# image-2
# 4k 지원(4096), 16:9 비율 생성 가능
# 투명 배경 못 만듦

b64 = result.data[0].b64_json
with open('output.png', 'wb') as f:
    f.write(base64.b64decode(b64))

print('저장 완료')