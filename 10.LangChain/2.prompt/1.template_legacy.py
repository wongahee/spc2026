from langchain_core.prompts import PromptTemplate

template = "당신은 작명가입니다. 다음 상품을 만드는 회사의 이름을 지어주세요. 상품명: {product}"
# 을/를 문제를 해결하기 위해 변수명을 맨 뒤에 적음

prompt = PromptTemplate(input_variables=['product'], template=template)
# template = 변수

filled_prompt = prompt.format(product="스마트폰")
print("완성된 프롬프드: ", filled_prompt)

filled_prompt = prompt.format(product="자율주행 자동차")
print("완성된 프롬프드: ", filled_prompt)

print("-" * 80)
test_products = [
    "모바일 게임", "로봇 장난감", "가방", "영어 교육 플랫폼", "전기 자전거"
]

for product in test_products:
    final_prompt = prompt.format(product=product)
    print(f"[{product}] {final_prompt}")