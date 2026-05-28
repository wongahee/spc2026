# Langchain - 아래의 과정
# 입력 정의(Prompt) => 2. LLM => 3. 결과 파싱

# 1. Prompt 생성
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 브랜드 기획자입니다."),
    ("user", 
        "회사를 홍보하기 위한 캐치프레이즈를 5개 만들어줘. 회사명: {company}, 상품명: {product}."
        "출력 결과는 콤마로 구분된 리스트 (CSV)로 만들어줘."
     )
])

filled_prompt = prompt.format_messages(company="테슬라", product="Model S")
# print("완성된 프롬프드: ", filled_prompt)

# 2. LLM 모델 호출 (invoke)
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
response = llm.invoke(filled_prompt)

print(response.content)

# 3. 출력 파서 (Output Parser)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import CommaSeparatedListOutputParser

parser1 = StrOutputParser()
parser2 = CommaSeparatedListOutputParser()

result_str = parser1.invoke(response)
result_csv = parser2.invoke(response)

print("문자열 결과: ", result_str)
print("CSV 결과: ",result_csv)