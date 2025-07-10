# UPDATE WHERE version = ?

OPTIMISTIC LOCK을 구현하기 위해 사용
- 트랜잭션이 충돌없이 진행되었는지 검증한다
- @Version 필드로 데이터 변경여부를 감지한다

낙관적 락
- 트랜잭션 동안 락을 걸지 않는다
    - 읽기/쓰기 성능이 중요할 때, 동시성이 중요할 때
    - 낙관적 락은 마지막 충돌만 확인한다
- 커밋할 때 다른 튼랜잭션이 같은 데이터를 수정했는지 확인한다
- 어떻게?
```sql
-- 트랜잭션 1
BEGIN;
UPDATE users SET name = 'New name 1', version = version + 1 WHERE id = 1 AND version = 1; -- 먼저 수행하면 version이 2가 되어버린다

-- 트랜잭션 2
BEGIN;
UPDATE users SET name = 'New name 1', version = version + 1 WHERE id = 1 AND version = 1; 
-- 트랜잭션 1이 커밋되기 전에 해당 명령을 실행하면 실패한다 (락처럼 무한 대기해버린다)
-- 왜냐면 이미 version이 2가 되어 버렸기 떄문이다
```

장점
- 데이터 출동 감지: 트랜잭션 중에 다른 데이터가 변경되었는지 확인 가능하다
- 동시성 문제: 여러 트랜잭션이 동일한 데이터를 수정하지 않도록 한다
- 낙관적 락: 락을 걸지 않고, 업데이트 시점에 충돌여부를 확인한다
- 데이터 정합성 유지 : 스프링의 경우 OptimisticLockException을 발생시킨다

단점
- 충돌 발생 시, 재시도 필요: 트랜잭션을 다시 수행헤야 한다
- 경쟁이 심하면 성능저하 : 같은 데이터를 자주 업데이트하면 충돌이 자주 발생한다

언제 사용할까
- 다른 사용자가 같은 데이터를 수정하는 일이 적을 때 사용 : 충돌 발생이 적을 경우 (왜냐하면 충돌이 생기면 재시도 계속 해야되기 때문이다)
- 


재시도 로직
- @Retryable로 구현
```java
    @Retryable(
        value = ObjectOptimisticLockingFailureException.class,  // 낙관적 락 예외 발생 시 재시도
        maxAttempts = 3,  // 최대 3번 재시도
        backoff = @Backoff(delay = 200)  // 200ms 후 재시도 (점진적 증가 가능)
    )
    public void updateUser(Long userId, String newName) {
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new RuntimeException("User not found"));
    }
```
- ON CONFLICT: 충돌이 발생하면 자동으로 version이 증가하면서 다시 시도
```sql
INSERT INTO user (id, name, version)
VALUES (1, 'New Name', 2)
ON CONFLICT (id, version)
DO UPDATE SET name = EXCLUDED.name, version = user.version + 1; -- 자동으로 버전 업데이트
```
- 카프카 비동기 처리: 트랜잭션 즉시 카프카로 이벤트 발생, Worker 서비스에서 충돌이 해결될때까지 반복