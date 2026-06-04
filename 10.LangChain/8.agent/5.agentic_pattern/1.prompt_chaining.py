from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# [1단계] 리서치 수행중
research_prompt = ChatPromptTemplate.from_template(
    "다음 주제에 대해 핵심 사실 5가지를 간결하게 정리해주세요."
    "\n\n 주제: {topic}"
)

research_chain = research_prompt | llm | parser

# [2단계] 게이트 검증 수행중
gate_prompt = ChatPromptTemplate.from_template(
    """다음 리서치 결과가 적합한지 평가해 주세요. \n
    평가 기준: \n 
    1. 사실 5가지가 올바르게 포함되어있는가? \n 
    2. 각 사실이 구체적이고 검증 가능한가? \n 
    3. 주제와 관련있는가? \n 
    결과: \n 
    PASS 또는 FAIL로만 답하기. (PASS - 설명없이 PASS만, FAIL - 실패 이유를 한 줄로 설명)
    \n\n 리서치 결과: {research}
    """
)

gate_chain = gate_prompt | llm | parser

# [3단계] 분석 수행중
analysis_prompt = ChatPromptTemplate.from_template(
    """다음 리서치 결과를 바탕으로 심층 분석 내용을 작성해주시오. \n
    다음을 포함해주세요: \n
    - 핵심 트랜드 또는 패턴\n
    - 시사점 \n
    - 향후 전장
    \n\n 리서치 결과: {research}"""
)

analysis_chain = analysis_prompt | llm | parser

# [4단계] 보고서 생성 수행중
# CEO에게 보고하는 형태, 실무자가 팀장에게 보고하는 형태, 초등학생도 이해 가능한 형태 등등 도 진행해보기
report_prompt = ChatPromptTemplate.from_template(
    """다음 리서치와 분석된 내용을 바탕으로 간결한 보고서를 작성하시오. \n
    출력 형식: \n
    - 제목 \n
    - 요약 (3줄)\n
    - 핵심 발견사항 \n
    - 결론
    \n\n 리서치: {research} 분석: {analysis}"""
)

report_chain = report_prompt | llm | parser

# Main Pipeline
def run_chaining_pipeline(topic):
    # 1단계: 리서치
    print('[1단계] 리서치 수행중')
    research = research_chain.invoke({'topic': topic})

    # 2단계: 게이트 검증
    print('[2단계] 게이트 검증 수행중')
    gate_result = gate_chain.invoke({'research': research})
    print("2단계 결과: ", gate_result)

    if gate_result.lower() in "fail":
        print("게이트 검증에 실패하여 해당 업무를 재수행합니다.")
    gate_result = gate_chain.invoke({'research': research})
    # 고도화 시, 반복 횟수 정의하기 / 프롬프트 고도화 / 모델 바꾸기 (gpt-4o-mini)

    # 3단계: 분석 수행
    print('[3단계] 분석 수행중')
    analysis = analysis_chain.invoke({'research': research})

    # 4단계: 보고서 생성
    print('[4단계] 보고서 생성 수행중')
    report = report_chain.invoke({'research': research, 'analysis': analysis})

    return report


# 질문
# 1. 2026년도 생성형 AI 시장 동향 조사를 해오시오.

topic = ""

result = run_chaining_pipeline(topic)
print("-" * 60)
print("최종 보고서: ")
print("-" * 60)

# 리서치 -> 분석 -> 보고서
print(result)