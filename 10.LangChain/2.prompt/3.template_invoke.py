# 내용 이해를 위해 분리하여 기재
# 실무에서는 역할에 맞게 짜야함

# prompt
from langchain_core.prompts import ChatPromptTemplate   # 많이 사용

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 작명가입니다."),
    ("user", "다음 상품을 만드는 회사의 이름을 지어주세요. 상품명: {product}")
])

filled_prompt = prompt.format_messages(product="스마트폰")
print("완성된 프롬프드: ", filled_prompt)

# invoke, 호출
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
response = llm.invoke(filled_prompt)

print(response.content)