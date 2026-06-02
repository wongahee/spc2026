from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_tavily import TavilySearch
# pip install langchain-tavily

load_dotenv()

# 구글 검색은 원래 구글 API 키로 하면 됨
# 쉽게 만들어주는 사이트: Serf, Serper, Tavily

# pip install langchain-tavily
# .env 파일에 tavily api key 넣기

web_search = TavilySearch(max_results=3)
llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(llm, [web_search])

result = agent.invoke({"messages": [("user", "LangChain의 최신 버전은?")]})
print(result["messages"][-1].content)