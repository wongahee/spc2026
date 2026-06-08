from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
# mnli = Multi-genre Natural Language Inference

# 내부적으로 문장간에 연관성
# 1. 함의 (Entailment)
# 예) 오늘 비가 많이 내린다. 우산이 필요할 수 있다.

# 2. 모순 (Contradiction)
# 예) 오늘 비가 많이 내린다. 오늘은 맑은 날이다.

# 3. 중립 (Natural)
# 예) 오늘 비가 많이 내린다. 나는 피자를 좋아한다. - 연관 x

text = "I just upgraded my computer's graphics card."
# 나는 내 컴퓨터의 그래픽 카드를 업그레이드 했다.
# 이 문장은 기술에 관한 것이다.
# 이 문장은 스포츠에 관한 것이다.
# 이 문장은 요리에 관한 것이다.
# 이 문장은 정치에 관한 것이다.

# text 분류
candidate_labels = ["technology", "sports", "cooking", "politics"]

result = classifier(text, candidate_labels=candidate_labels)

print(f"문장: {text}")
for label, score in zip(result["labels"], result["scores"]):
    print(f" {label:12} {score:.3f}")

print(f"최종 분류: {result['labels'][0]}")