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

- wait 큐는 사용자를 대기시키고, proceed 큐는 wait 큐에서 가장 먼저온 사람을 제거하고 진행시키는데 사용한다
- `popMin`: 가장 먼저 온 (timestamp가 가장 작은) N명을 큐에서 추출한다
- 추출한 사용자를 proceed 큐에 순서대로 추가한다
- `rank`: proceed 큐에서 진입이 가능한지 살펴본다
- 즉, wait 큐에 계속 사용자를 추가한 다음 proceed 큐에서 
- sortedset을 사용하는 이유
    - 특정 사용자 기준으로 정렬을 바꾸거나 우선순위를 바꿀 때 로직을 바꿀 수 있다
    - rank 로직을 제공하여 몇번째 순서인지 알 수 있다

