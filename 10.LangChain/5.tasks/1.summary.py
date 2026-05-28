# 목적: 긴 문장을 받아서 짧게 요약한다.

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate, 
    HumanMessagePromptTemplate, 
    SystemMessagePromptTemplate, 
    AIMessagePromptTemplate
)

from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda

load_dotenv()

template = "다음의 긴 내용을 3개의 문장으로 요약하시오: \n\n{article}"
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("당신은 전문 문장 요약가입니다."),
    HumanMessagePromptTemplate.from_template(template)
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)   # 0.3~0.5 사용. 높아질 수록 창의적인 이야기가 많이 생김

chain = chat_prompt | llm | RunnableLambda(lambda x: {"summary": x.content.strip()})

input_text = {
    "article": "행안부가 운영하는 통합행정 서비스 포털인 정부24에서는 2024년 4월 교육부 NEIS(나이스) 연계 민원서류와 국세청 납세증명서 관련 소스코드 개발 오류로 1233명의 개인정보가 타인에게 공개되는 사고가 발생했다. 또한 지난해 5월 정부24 홈페이지에서 제공하는 주민등록증 발급상황 조회 서비스에 존재하는 인증 취약점 때문에 주민등록증 발급상황 4건이 타인에게 조회됐다."
}

result = chain.invoke(input_text)
print("요약 결과: ", result['summary'])