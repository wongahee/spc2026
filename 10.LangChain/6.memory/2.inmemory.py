# 파일/메모리/DB에 직접 대화내용을 저장

from dotenv import load_dotenv

# 프롬프트
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# 모델
from langchain_openai import ChatOpenAI
# 파서
from langchain_core.output_parsers import StrOutputParser
# 기타
from langchain_core.chat_history import InMemoryChatMessageHistory

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 챗봇입니다."),
    MessagesPlaceholder("history"),
    ("user", "{input}") 
])

chain = prompt | llm | StrOutputParser()

history = InMemoryChatMessageHistory()  # 메모리상의 공간 생성

def chat(message):
    print(f"질문: {message}")

    answer = chain.invoke({
        "input": message,
        "history": history.messages,     # 저장소의 메시지
        # "history": history.messages[10:],     # 저장소의 메시지 (최근 10개)
    })
    print(f"답변: {answer}")

    history.add_user_message(message)
    history.add_ai_message(answer)

chat("안녕하세용?")
chat("제 이름은 고부철입니다.")
chat("저는 겨울에 바닷가에 가서 서핑하는 것을 좋아합니다.")
chat("제 이름과 취미가 뭐라고 했지요?")

question = [
    "저는 밤에 드라이브하면서 노래 듣는 것을 좋아합니다."
    "저는 좋아하는 사람들과 오래 이야기하는 시간을 소중하게 생각합니다."
    "저는 낯선 도시를 천천히 구경하는 것을 좋아합니다."
    "저는 겨울 새벽에 따뜻한 커피를 마시는 것을 좋아합니다."
    "저는 바닷가를 걸으면서 음악 듣는 시간을 좋아합니다."
    "저는 새로운 취미를 하나씩 배우는 것을 즐깁니다."
    "저는 비 오는 날 집에서 영화 보는 것을 좋아합니다."
]