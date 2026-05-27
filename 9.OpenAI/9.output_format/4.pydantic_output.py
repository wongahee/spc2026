import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from pydantic import BaseModel

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# 타입 지정 - 파이썬 객체 형태
class CityInfo(BaseModel):
    name: str
    population: int
    area_km2: float

# response = client.chat.completions.create(
response = client.chat.completions.parse(   # 파이썬 객체 형태는 parse로 받아야함
    model='gpt-4o-mini',
    messages=[
        {'role':'system', 'content':'질문에 대해 JSON으로만 답변하시오.'},
        {'role':'user', 'content':'서울의 인구와 면적을 알려주시오.'}
    ],
    response_format=CityInfo
)

# answer = response.choices[0].message.content  # create로 물어본 것은 content
answer = response.choices[0].message.parsed     # parse로 물어본 것은 parsed

print(answer)
data = answer
print(f"도시의 이름: {data.name} - 인구: {data.population:,}명, 면적 {data.area_km2}km2")
