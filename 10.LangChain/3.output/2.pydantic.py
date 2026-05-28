from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from pydantic import BaseModel, Field

load_dotenv()

class MovieReview(BaseModel):
    """ 영화 리뷰 분석 결과 """
    title: str = Field(description="영화 제목")
    sentiment: str = Field(description="감성 분류: 긍정, 부정, 중립")
    score: int = Field(description="1~10 점수")
    summary: str = Field(description="리뷰 요약 (1~2문장)")
    keywords: list[str] = Field(description="핵심 키워드 3개")

llm = ChatOpenAI(model="gpt-4o-mini")

parser = PydanticOutputParser(pydantic_object=MovieReview)
# print("포맷 명령문: ")
# print(parser.get_format_instructions())

prompt = ChatPromptTemplate.from_template(
    """ 다음 영화 리뷰를 분석해주세요. 
    리뷰: {review}

    {format_instructions}
    """
)

chain = prompt | llm | parser

reviews = [
    "인터스텔라는 우주 탐사를 소재로 한 SF 영화인데, 가족애와 인간의 희망을 감동적으로 담아냈어요. 압도적인 영상미와 음악 덕분에 몰입감이 매우 뛰어납니다.",
    "범죄도시는 통쾌한 액션과 강렬한 캐릭터가 매력적인 범죄 액션 영화예요. 특히 마동석의 시원한 액션과 유머가 큰 재미를 줍니다.",
    "라라랜드는 음악과 색감이 아름다운 뮤지컬 영화예요. 꿈과 사랑 사이에서 고민하는 청춘들의 이야기를 감성적으로 담아냈습니다."
]

for review in reviews:
    result = chain.invoke({
        "review": review,
        "format_instructions": parser.get_format_instructions()
    })

    print(f"제목: {result.title}")
    print(f"감성: {result.sentiment} (점수: {result.score}/10)")
    print(f"요약: {result.summary}")
    print(f"키워드: {result.keywords}")
    print('-' * 30)