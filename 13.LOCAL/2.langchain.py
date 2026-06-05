# pip install langchain-openai langchain-anthopic
# pip install langchain-ollama

from langchain_ollama import ChatOllama

llm = ChatOllama(model="mistral")

response = llm.invoke("안녕? 한마디로 너를 소개해줘.")

print(response.content)