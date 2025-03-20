# Retrieval

## RAG (Retrieval-Augmented Generation)
- 파인튜닝: 외부 데이터를 활용해서 모델을 학습시키는 것 (학습을 위한 GPU 비용 많이 듦)
- RAG: 외부 데이터를 활용해서 모델을 튜닝하는 것
- 둘 다 모두 LLM이 가지지 않은 지식을 포함해서 답변하도록 하는 프레임워크
- 외부데이터의 문장을 참고하여 답변

![rag](./rag.png)



## Retrieval
![retrieval](./retrieval.png)
1. Document Loader: 문서를 로드하는 것
2. Text Splitter: 문서를 분할하는 것
3. Vector Store: 문서를 벡터로 변환하는 것
4. Retrieval: 사용자 질문과 유사한 문장을 검색하는 것
5. Chain: 검색한 문장을 기반으로 유사 문자을 출력하는 것 



![document-loader](./document-loader.png)
1. page content: 문서의 내용을 가져오는 것
2. metadata: 문서의 메타데이터를 가져오는 것 (문서 위치, 제목, 페이지 넘버)

- answer: 문서의 내용을 가져오는 것 (page content)
- sources: 답변의 출처, (metadata) (LLM이 어떤 문서를 참고했는지 직접 확인)





