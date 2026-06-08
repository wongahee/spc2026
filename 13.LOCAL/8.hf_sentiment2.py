from transformers import pipeline

# Load the classification pipeline with the specified model
pipe = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")

# Classify a new sentence
# sentence = "I love this product! It's amazing and works perfectly."
sentence = "배고프니까 점심시간 앞당겨"
result = pipe(sentence)

# Print the result
print(result)
