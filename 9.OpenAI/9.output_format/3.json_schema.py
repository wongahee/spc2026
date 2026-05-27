import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# 자료구조 정의 - 내가 원하는 출력 형식 (json schema)
city_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'population': {'type': 'integer'},
        'area_km2': {'type': 'number'}
    },
    'required': ['name', 'population', 'area_km2'], # 필수 필드
    'additionalProperties': False,                  # 정의하지 않은 것은 추가하지 않음
}

response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {'role':'system', 'content':'질문에 대해 JSON으로만 답변하시오.'},
        {'role':'user', 'content':'서울의 인구와 면적을 알려주시오.'}
    ],
    # API 단에서 출력 결과 보장
    # output을 원하는 형태에 맞게 강제화함 ("""""" 제거)
    response_format={
        'type': 'json_schema',     # 정의한 스키마로 출력되도록 요청
        'json_schema': {
            'name': 'city_info',   # 정의한 이름 
            'strict': True,
            'schema': city_schema
        }
    }
)

answer = response.choices[0].message.content
# print(answer)

# json 형태로 출력
data = json.loads(answer)
print(f"도시의 이름: {data['name']} - 인구: {data['population']:,}명, 면적 {data['area_km2']}km2")
