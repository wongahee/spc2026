# pip install langchain langchain-openai

import os
from dotenv import load_dotenv

# from langchain.llms import OpenAI     # 구버전
from langchain_openai import OpenAI     # 신버전

load_dotenv()

openai_api_key = os.environ.get('OPENAI_API_KEY')

llm = OpenAI(model="gpt-4o-mini")
# llm = OpenAI(model="gpt-4o-mini", temperature=1.5)


print(llm)

prompt = "오늘 저녁은 무엇을 먹을까요?"
result = llm.invoke(prompt)     # 호출/질문 함수: invoke
print(result)