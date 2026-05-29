# 목적: 콜센터 답변
# 질문 유형 입력 => 배송조회 / 결제관련 / 기술지원 상담

# RunnableBranch

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

def make_chain(role):
    return (
        ChatPromptTemplate.from_messages([
            ("system", role),
            ("user", "{question}")
        ])
        | llm
        | StrOutputParser()
    )

# 배송 / 결제 / 기술지원
delivery_chain = make_chain("당신은 배송 전문가입니다.")
payment_chain = make_chain("당신은 결제 전문가입니다.")
tech_chain = make_chain("당신은 기술 지원 전문가입니다.")

branch = RunnableBranch(
    (
        lambda x: "배송" in x["question"],
        delivery_chain
    ),
    (
        lambda x: "결제" in x["question"],
        payment_chain
    ),
    (
        lambda x: "기술" in x["question"],
        tech_chain
    ),
    RunnableLambda(lambda x: "죄송합니다. 해당 질문에 대한 답변을 제공할 수 없습니다.")
)

questions = [
    "배송 조회하고 싶어요", "결제 방법을 알고 싶습니다", "기술적인 문제 해결 부탁드립니다"
]

for q in questions:
    print("질문: ", q)
    print("답변: ", branch.invoke({"question": q}))
    print("-" * 60)