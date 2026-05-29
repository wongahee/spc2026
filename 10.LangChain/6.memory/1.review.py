from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_core.messages import HumanMessage, AIMessage

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 챗봇입니다."),    # 역할 지정 (system)
    ("user", "{input}")                     # 나의 질문 (user, human)
    # ("ai", "챗봇 답변")                    # 챗봇 답변 (assistant) - 잘 사용하지 않음
])

chain = prompt | llm | StrOutputParser()

# 이전 대화 내용을 모르는 코드
print(chain.invoke({"input": "안녕하세요, 나는 홍길동 입니다."}))
print(chain.invoke({"input": "내가 누구게"}))
print(chain.invoke({"input": "방금 말했잖아. 그것도 몰라?"}))       # 명시했음에도 모름

print("-" * 60)

# 이전 대화 내용 불러오기
prompt_with_history = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 챗봇입니다."),
    MessagesPlaceholder("history"),     # 
    ("user", "{input}")
])

chain2 = prompt_with_history | llm | StrOutputParser()

history_example = [
    HumanMessage(content="안녕하세요, 저는 홍길동입니다."),
    AIMessage(content="네, 홍길동님 반갑습니다.")
]

answer = chain2.invoke({
    "history": history_example,
    "input": "제 이름이 뭐였죠?"
})

print(answer)