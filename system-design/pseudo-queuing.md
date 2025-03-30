# Pseudo Queueing

데이터베이스의 **pseudo queueing(유사 큐잉)**은, 데이터베이스 테이블을 마치 큐처럼 사용하는 패턴을 말합니다. 
큐잉 시스템이 따로 없거나, 간단한 작업에 메시지 브로커를 도입하기엔 부담스러울 때 사용됩니다.
주로 작업 처리를 위한 **작업 대기열(job queue)**나 비동기 처리가 필요할 때 활용됩니다.

🚦 어떻게 작동하나?
1. 테이블 생성
작업을 저장할 테이블을 만들어요. 보통 이런 컬럼을 사용합니다:
```
id (기본 키)
status (대기, 처리 중, 완료 등 상태 관리)
payload (처리할 데이터)
created_at (작업 생성 시간)
updated_at (상태 변경 시간)
작업 추가 (Enqueue)
새로운 작업이 들어오면, 테이블에 새 레코드를 삽입해요.
```
2. 작업 처리 (Dequeue)
처리할 작업을 가져올 때는 SELECT FOR UPDATE 또는 UPDATE + RETURNING 같은 동작으로 락을 걸어 다른 프로세스가 동시에 작업을 가져가지 못하게 막아요.
예시 (PostgreSQL 기준):

```sql
UPDATE job_queue
SET status = 'PROCESSING', updated_at = NOW()
WHERE id = (
  SELECT id FROM job_queue
  WHERE status = 'PENDING'
  ORDER BY created_at
  LIMIT 1
  FOR UPDATE SKIP LOCKED
)
RETURNING *;
```
3. 작업 완료 처리
작업이 끝나면 상태를 **'COMPLETE'**로 바꾸거나, 작업 결과를 기록해요.

4. 오류 처리 및 재시도
실패한 작업은 'FAILED' 상태로 두고, 재시도 로직을 추가할 수 있어요.

🎯 장점
1. 메시지 브로커(RabbitMQ, Kafka 등)를 따로 도입하지 않고, 익숙한 DB만으로 큐잉 구현이 가능해요.
2. 트랜잭션 처리를 통해 작업의 원자성을 보장할 수 있어요.

⚠️ 단점
1. 다량의 작업이 쌓이면 성능이 저하될 수 있어요.
2. 폴링(Polling)을 통해 작업을 가져오는 경우, DB 부하가 커질 수 있어요.
3. 대규모 트래픽 처리에는 메시지 브로커를 사용하는 게 더 나아요.
4. 이 방식이 적합한 상황인지, 혹은 메시지 브로커 도입이 나을지 고민된다면 구체적인 상황을 말해줘요. 🚀