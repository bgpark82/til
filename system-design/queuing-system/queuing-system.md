# Queuing System

패스트 캠퍼스 강의 내용 요약

# 요약
- 자바의 Reactive 라이브러리 및 Reactive Redis 사용
- Redis의 Sorted Set을 사용하여 시간 순서대로 데이털르 정렬 (근데 굳이 Sorted Set이 필요했을까 어차피 시간 순서대로 저장될텐데)
- `filter(i -> i)` : Sorted Set으로 저장 시, 같은 key 값을 가지면 false를 반환한다. true일떄만 데이터를 처리하도록 한다
- `switchIfEmpty`: 만약 false를 반환하면 값이 비기 때문에 에러를 Mono로 감싸서 반환한다
- map은 단순히 Mono 내부값을 변환하는데만 사용하되, 새로운 Mono를 반환하지 않고 기존 Mono를 사용한다
- flatMap은 비동기적으로 실행되는 후속 Mono를 실행해서 반환하는 역할을 한다. 기존에 실행되던 Mono<Boolean>은 무시되어 새로운 Mono를 반환할 수 있도록 만든다
- `rank`는 정렬된 집합에서 몇번째로 작은지 반환한다. (오름차순 정렬)
- 레디스의 키 값으로 여러개의 큐를 생성할 수 있다 (예를들어, 키 `user:queue:1`와 키 `user:queue:2`는 다른 라이프 사이클을 가진다)