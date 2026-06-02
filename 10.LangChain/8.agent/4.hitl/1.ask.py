from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

checkpoint = MemorySaver()

@tool
def send_payment(recipient: str, amount: int) -> str:
    """ 수신자에게 지정 금액을 송금한다."""
    return f"{recipient}에게 {amount}원 송금 완료"

llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(llm, [send_payment], checkpointer=checkpoint, interrupt_before=["tools"])  
            # checkpoint: 에이전트 저장, interrupt_before[]: [] 실행 전 멈추기
            # checkpoint, MemorySaver를 통해 보안에 위험한 요소를 실행 전 멈추거나 동의를 받아 실행함
config = {"configurable": {"thread_id": "t001"}}

question = "홍길동에게 10000원 송금해줘"

print(f"[유저] {question}")
result = agent.invoke({"messages": [("user", question)]}, config=config)

call = result["messages"][-1].tool_calls[0]     # 정지시점 (도구를 부르기 직전)

print(f"[일시정지] {call['name']} ({call['args']})")

human_result = input("\n이대로 실행할까요? (y/n)").strip().lower()
if human_result == 'y':
    result = agent.invoke(None, config=config)  # 할 일 이어서 하기
    print(f"[최종결론] {result['messages'][-1].content}")
else:
    print(f"\n[중단] 사용자 요청에 의해 중단되었습니다.")