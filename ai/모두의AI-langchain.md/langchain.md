# LangChain

https://www.youtube.com/watch?v=WWRCLzXxUgs&t=353s&ab_channel=%EB%AA%A8%EB%91%90%EC%9D%98AI

## LangChain
언어 모델로 구동되는 애플리케이션을 개발하기 위한 프레임워크
애플리케이션은 API로 언어 모델을 호출한다
- 데이터 인식: 언어 모델을 다른 데이터 소스에 연결
- 에이전트 기능: 언어 모델이 환경과 상호작용

### 왜 사용하는가
ChatGPT의 한계
1. 정보 접근 제한
2. 인터넷 접근 가능: 최근 데이터 반영 안됨 (할루시네이션, 2021년 1월까지만)
3. 토큰 제한: GPT-3.5, GPT-4 토큰 제한 있음 (4096, 8192 토큰)

ChatGPT의 한계 해결 방법
- 위 3개 문제를 해결하기 위해 개량해야 한다

1. 파인 튜닝
    - 딥러닝 모델의 weight를 조정하여 원하는 용도로 모델을 구축
    - 블룸버그는 금융 전문 데이터로 파인 튜닝을 통해 모델을 구축
    - 단점: 학습을 다시 해야해서 비용이 크다
2. N-shot 학습
    - 출력 예시를 주고 답변을 시키는 방식
    - 단점: 정보를 기반으로 정보를 얻기 힘들다
3. **in-context learning**
    - 문맥을 제시하고, 해당 문맥 기반으로 모델이 출력
    - 질문하고자 하는 정보를 주고, 해당 정보를 기반으로 대답
    - **LangChain에서 사용**

ChatGPT의 한계를 LangChain으로 돌파
1. 정보 접근 제한
    - Vectorstore 기반 정보 탐색
    - Agent 기반 검색 결합
2. 토큰 제한
    - TextSplitter를 활용한 문서 분할
3. 환각현상
    - 주어진 문서에 대해서만 답하도록 Prompt 입력

## LangChain 구조
- LLM: 언어 모델 (OpenAI, PALM-2, LLAMA, Anthropic, etc)
- Prompt: 언어 모델에 입력되는 문장 (Prompt Template, Chat Prompt, Example Selector, N shot learning, Output Parser)
- Index: 문서를 탐색하도록 구조화하는 모듈 (Document Loader, Text Splitter, Vector Store)
- Memory: 채팅 이력을 기억, 이를 기반으로 대화 가능
- Agent: 특정 행동을 취하는 것
- Chain: 프롬프트를 주었을 때, 출력을 만들고, 출력을 기반으로 다음 프롬프트를 만드는 것 (LLM Chain, Question Answering Chain, Summarization Chain, Retrieval Question/Answering)
- Agent: 기존 Prompt Template으로 수행할 수 없는 작업 가능하게 만듦. 웹검색, SQL 쿼리 등 (Custom Agent, Custom Multication Agent, Conversation Agent)

## 예시: PDF 챗봇 구축
![chatbot](./langchain-pdf-chatbot.png)
1. 문서 업로드(Document Loader): PDFLoader로 문서 가져오기
2. 문서 분할(Text Splitter): PDF 문서를 여러 문서로 분할 (토큰 제한이 있기 때문)
3. 문서 임베딩(Vector Store): 문서를 벡터로 변환
4. 문서 임베딩 검색(Retrieval): 문서를 저장한 곳에서 검색
5. 문서 질문/답변(Question Answering): 문서를 질문/답변 체인으로 만들기
    - 질문과 유사한 문장을 받았을 때 프롬프트로 생성해야 함
    - ChatGPT 파인튜닝하는게 아니다
    - 문서를 필요할 때마다 써먹기 위해 LLM에게 줄 뿐이다
    - 내가 질문한 것과 가장 비슷한 텍스트를 가져와서 프롬프트로 만들어서 LLM에게 준다
    - 너가 질문한건 이거고, 가장 비슷한 문장으로 PDF에 이런게 있었어
    - 이렇게 하면 ChatGPT가 이해하기 쉽다


