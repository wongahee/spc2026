# -- 시간이 지난 코드로 실행 불가

# agent를 통해, 본연의 LLM(대화 기능 등등) 사용 가능

# pip install wikipedia
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent, AgentType

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

tools = load_tools(["wikipedia"])

# 에이전트 초기화
agent = initialize_agent(
    tools=tools,                                    # 에이전트 사용 가능 도구목록
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,    # 에이전트 전략 (zero_shot: 예시 없이 도구 설명만 보고 판단)
                                                    # ReAct: Thought → Action → Observation 사이클을 반복하며 추론
    verbose=True    # 추론 과정을 콘솔에 출력 (기본값 False)
)

result = agent.invoke({"input": "인공지능의 역사에 대해 간략히 설명해줘."})
print(result["output"])