# 목적: 뉴스 분석
# 뉴스 입력 => 요약 / 감정 / 카테고리 분석

# RunnableParallel

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate, 
    HumanMessagePromptTemplate, 
    SystemMessagePromptTemplate, 
)
from langchain_core.runnables import RunnableLambda, RunnableParallel

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("당신은 뉴스 분석가입니다. 다음 뉴스를 {analysis_type} 결과만 출력하시오."),
    HumanMessagePromptTemplate.from_template("{news}")
])

# 요약
chain_summary = (
    chat_prompt.partial(analysis_type="요약")
    | llm
    | RunnableLambda(lambda x: x.content.strip())
)

# 감정
chain_sentiment = (
    chat_prompt.partial(analysis_type="감정")
    | llm
    | RunnableLambda(lambda x: x.content.strip())
)

# 카테고리
chain_category = (
    chat_prompt.partial(analysis_type="카테고리")
    | llm
    | RunnableLambda(lambda x: x.content.strip())
)

parallel_chain = RunnableParallel({
    "summary": chain_summary,
    "sentiment": chain_sentiment,
    "category": chain_category
})

input_text = {
    "news": "최근 영국 매체 데일리메일은 영양학자 소피 가스트만(Sophie Gastman)의 설명을 인용해 타히니의 건강 효능과 섭취 방법에 대해 소개했다. 타히니는 볶은 참깨를 곱게 갈아 만든 베이지색 페이스트로, 중동식 요리인 후무스의 재료로 잘 알려져 있다. 설명에 따르면 타히니는 참깨를 통째로 갈아 만드는 만큼 참깨의 영양 성분을 그대로 담고 있는 식품이다. 식이섬유와 단백질 함량이 높은 편이며 칼슘·마그네슘·철분·아연·구리 등 다양한 미네랄도 풍부하게 포함돼 있다. 특히 칼슘은 뼈와 치아 건강 유지에 도움을 줄 수 있고, 마그네슘은 혈압과 혈당 조절, 신경 기능 등에 관여한다. 철분은 산소 운반과 피로 예방에 필요하며 아연은 면역 기능과 상처 회복 등에 중요한 역할을 한다."
}

result = parallel_chain.invoke(input_text)

print("- 요약: ", result['summary'])
print("- 감정: ", result['sentiment'])
print("- 카테고리: ", result['category'])
