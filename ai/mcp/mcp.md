# MCP

https://www.youtube.com/watch?v=zVSZ2gXvhVE&ab_channel=%EA%B0%9C%EB%B0%9C%EB%8F%99%EC%83%9D

## 탄생 배경
LLM이 Agent로 외부 데이터를 실시간으로 소통가능 하다
LLM이 다른 데이터를 통신할 때마다 프로토콜이 모두 달라 따로 개발해야 했다

## 구성
![mcp](./assets/mcp.png)
1. 클라이언트 : 클로드, IDE 등 외부 데이터를 호출하는 주체
2. MCP 서버: 외부 데이터와 통신하는 서버 (프록시 서버)
    - Github MCP 서버로 commit, push 가능
    - 외부 인터넷으로 자료 검색
3. MCP 마켓플레이스: MCP 서버를 오픈소스로 활용할 수 있는 곳
    - MCP 서버를 마켓플레이스에 배포할 수도 있음
 
장점
1. 재사용성이 좋다
2. 보안성 : AI와 데이터 소스간의 안정적인 상호작용 가능


## MCP 마켓플레이스
https://mcp.so/server/perplexity/ppl-ai
https://mcp.so/
https://smithery.ai/
- Github MCP 서버 사용

## MCP 서버 구축
https://modelcontextprotocol.io/introduction
https://github.com/modelcontextprotocol/python-sdk

## LLM을 이용한 MCP 서버 구축
https://modelcontextprotocol.io/tutorials/building-mcp-with-llms
- mcp doc
- mcp typescript sdk

## Firecrawl을 이용한 크롤링
https://youtu.be/ueJvsEgjKHk?si=qpafLr6-IzaFL7WH

## MCP 서버 리스트
https://github.com/punkpeye/awesome-mcp-servers