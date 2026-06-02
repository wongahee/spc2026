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

@tool
def get_balance(account: str) -> str:
    """ 계좌 잔액 조회 """
    return {"alice": 1_000_000, "bob": 500_000}.get(account, 0)

llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(llm, [send_payment, get_balance], checkpointer=checkpoint, interrupt_before=["tools"])  
            # checkpoint: 에이전트 저장, interrupt_before[]: [] 실행 전 멈추기
            # checkpoint, MemorySaver를 통해 보안에 위험한 요소를 실행 전 멈추거나 동의를 받아 실행함
config = {"configurable": {"thread_id": "t001"}}

question = "alice의 잔액을 조회한 후, bob에게 10,000원 송금해줘"
# question = "alice와 bob의 잔액을 조회해서, 돈이 많은 사람에게 몰빵해줘"

print(f"[유저] {question}")
result = agent.invoke({"messages": [("user", question)]}, config=config)

# 하나의 질문에서 여러 개의 도구를 호출해야하는 경우
while result['messages'][-1].tool_calls:
    last_msg = result['messages'][-1]
    for call in last_msg.tool_calls:
        print(f"[일시정지] {call['name']} ({call['args']})")

    if last_msg.tool_calls[0]['name'] != 'send_payment':
        # 송금이 아닐 시 중요한 것이 아니니 계획 진행하게 하여 번거롭지 않게 함
        result = agent.invoke(None, config=config)
        continue

    human_result = input("\n이대로 실행할까요? (y/n) ").strip().lower()
    if human_result == 'y':
        result = agent.invoke(None, config=config)  # 할 일 이어서 하기
        print(f"[최종결론] {result['messages'][-1].content}")
    else:
        print(f"\n[중단] 사용자 요청에 의해 중단되었습니다.")
        break