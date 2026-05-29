# 파일/메모리/DB에 직접 대화내용을 저장

from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# pip install langchain_community
from langchain_community.chat_message_histories import FileChatMessageHistory

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 챗봇입니다."),
    MessagesPlaceholder("history"),
    ("user", "{input}") 
])

chain = prompt | llm | StrOutputParser()

history = FileChatMessageHistory("history.json")    # 파일에 저장

def chat(message):
    print(f"질문: {message}")

    answer = chain.invoke({
        "input": message,
        "history": history.messages
    })
    print(f"답변: {answer}")

    history.add_user_message(message)
    history.add_ai_message(answer)

chat("안녕하세용?")
chat("제 이름은 고부철입니다.")
chat("저는 겨울에 바닷가에 가서 서핑하는 것을 좋아합니다.")
chat("제 이름과 취미가 뭐라고 했지요?")

# chat() 내용을 삭제하고 재실행해도, 이전 대화내용을 기억함 (history.json)