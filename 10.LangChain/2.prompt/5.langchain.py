import os
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import (
    SystemMessagePromptTemplate, HumanMessagePromptTemplate, 
    AIMessagePromptTemplate
)

from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("당신은 브랜딩 컨텐츠 기획자 입니다."),
    HumanMessagePromptTemplate.from_template("회사를 홍보하기 위한 {company} 회사의 {product} 상품을 기반으로 캐치프레이즈를 만들어주세요.")
])

llm = ChatOpenAI(model="gpt-4o-mini")   # 모델 정의
parser = StrOutputParser()              # 후처리 함수 정의

inputs = {"company": "삼성전자", "product": "메모리"}
# inputs = {"company": "하이닉스", "product": "HBM"}
messages = prompt.format_messages(**inputs)      # ** : dict 형태로 풀어서 넣기
                                                 # company="삼성전자", product="메모리"

response = llm.invoke(messages)
output = parser.invoke(response)

final_result = {"response": output}

print(final_result)