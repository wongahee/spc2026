from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 상품명을 지어주는 기획자 입니다."),
    ("user", "{company} 회사에서 {product}을 만드는데, 이 제품명을 만들어주세요.")
])

# LCEL
chain = prompt | llm | parser

inputs = {"company": "AI 첨단 기술 회사", "product":"화장품"}

result = chain.invoke(inputs)

print("최종 결과: ", result)