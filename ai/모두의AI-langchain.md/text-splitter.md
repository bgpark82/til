# Text Splitter

![text-splitter](./assets/text-splitter.png)
- Chucking: 여러개의 문서를 더 작은 단위로 나눔
- chunk하나당 하나의 벡터
- 청크를 llm으로 보내서 사용자에게 전달
- LLM은 보통 토큰 제한이 있다 (4096개 etc)
- 해당 제한 안에서 질문을 해야 한다
- 청크의 크기, 청크의 구분



## 종류
- RecursiveCharacterTextSplitter: 문자 단위로 나눔, 여러문단 나눔, 간단한 문단 나눔을 기준으로 반복적으로 나눈다
- CharacterTextSplitter: 문단 단위로 나눔, 토큰을 넘어갈 가능성이 높음, 문단이 하나의 토큰이기 떄문, 정확하게는 특정 구분자 기준
- Token Text splitter: 토큰 단위로 텍스트를 분할

## Chunk Overlap
![chunk-overlap](./assets/chunk-overlap.png)
- 이전 청크의 뒷부분을 오버랩한다.
- 오버랩을 하면 중복되는 부분이 있어서 더 정확한 답변을 할 수 있다.
- 왜냐하면 앞문단의 마지막 문단을 제공할 수 있기 때문이다