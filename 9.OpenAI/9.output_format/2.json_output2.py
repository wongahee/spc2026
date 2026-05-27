import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {'role':'system', 'content':'질문에 대해 JSON으로만 답변하시오.'},
        {'role':'user', 'content':'서울의 인구와 면적을 알려주시오.'}
    ],
    # API 단에서 출력 결과 보장
    # output을 원하는 형태에 맞게 강제화함 ("""""" 제거)
    response_format={'type': 'json_object'}
)

answer = response.choices[0].message.content
print(answer)