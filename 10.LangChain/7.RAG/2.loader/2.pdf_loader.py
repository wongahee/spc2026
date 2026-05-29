# pip install pypdf

from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("./Javascript_Secure_Coding.pdf")
pages = loader.load()

print(f"PDF 페이지수: {len(pages)}\n")
for p in pages:
    if p.page_content.strip():
        print(f"발견한 내용이 있는 첫 페이지의 metadata: \n{p.metadata}")
        print(f"페이지 내용 (앞 100글자): \n{p.page_content[:100]}...")
        break