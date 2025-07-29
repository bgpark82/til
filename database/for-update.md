# 📌 SELECT FOR UPDATE

## ✅ 요약 및 핵심 학습 내용
- `SELECT FOR UPDATE`는 선택된 행에 배타적 잠금(exclusive lock)을 설정하는 SQL 구문입니다. 이를 통해 현재 트랜잭션이 완료될 때까지 다른 트랜잭션이 해당 행을 수정하거나 잠그는 것을 방지합니다.
- "읽기-수정-쓰기" 작업 중 발생할 수 있는 경쟁 상태(race condition)를 방지하고 데이터 일관성을 보장하는 데 사용됩니다.
- `FOR UPDATE`로 행이 잠기면, 다른 트랜잭션이 동일한 행에 대해 `UPDATE`, `DELETE` 또는 `SELECT ... FOR UPDATE`를 시도할 경우 블로킹(blocking)됩니다. 일반적인 `SELECT`는 여전히 데이터를 읽을 수 있습니다.

## 🔍 상세 설명
`SELECT FOR UPDATE`는 데이터베이스에서 특정 행(row)에 대해 배타적 잠금(exclusive lock)을 거는 역할을 합니다. 이 잠금이 걸린 행은 현재 트랜잭션이 커밋(commit)되거나 롤백(rollback)될 때까지 다른 트랜잭션에서 수정하거나 삭제할 수 없습니다.

이는 여러 트랜잭션이 동시에 같은 데이터에 접근하여 수정하려 할 때 발생하는 **데이터 불일치(lost update) 문제**를 해결하기 위해 사용됩니다.

예를 들어, 은행 계좌에서 잔액을 차감하는 시나리오를 생각해볼 수 있습니다.
1.  **트랜잭션 A**가 계좌 잔액을 조회합니다 (예: 1000원).
2.  동시에 **트랜잭션 B**도 동일한 계좌 잔액을 조회합니다 (예: 1000원).
3.  **트랜잭션 A**가 100원을 차감하고 잔액을 900원으로 업데이트합니다.
4.  **트랜잭션 B**는 이 사실을 모른 채, 자신이 조회했던 1000원에서 50원을 차감하고 잔액을 950원으로 업데이트합니다.
5.  결과적으로 트랜잭션 A의 작업은 유실되고(lost update), 최종 잔액은 950원이 되어 데이터 정합성이 깨집니다.

`SELECT FOR UPDATE`를 사용하면 이 문제를 다음과 같이 해결할 수 있습니다.

```sql
-- 트랜잭션 A
BEGIN;
-- id=1인 계좌에 배타락을 건다.
-- 이 시점부터 다른 트랜잭션은 이 행에 대한 잠금을 획득할 수 없다.
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;

-- 애플리케이션 로직 수행...
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT; -- 잠금 해제

-- 트랜잭션 B (동시에 실행)
BEGIN;
-- 트랜잭션 A가 커밋할 때까지 여기서 대기(block)한다.
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;

-- A가 커밋한 후, 변경된 최신 데이터를 읽고 잠금을 획득한다.
UPDATE accounts SET balance = balance - 50 WHERE id = 1;
COMMIT;
```

## (선택) 문제 및 해결책
- **문제:** 교착 상태(Deadlock). 두 개 이상의 트랜잭션이 서로 상대방이 점유한 리소스에 대한 잠금을 획득하려고 기다릴 때 교착 상태가 발생할 수 있습니다. 예를 들어, 트랜잭션 A는 행 1을 잠그고 행 2를 기다리고, 트랜잭션 B는 행 2를 잠그고 행 1을 기다리는 상황입니다.
- **해결책:** 모든 트랜잭션에서 리소스에 대한 잠금을 일관된 순서로 획득하도록 설계합니다. (e.g. 항상 테이블 A를 먼저 잠그고 테이블 B를 잠근다). 또한, 트랜잭션의 길이를 가능한 한 짧게 유지하여 잠금 점유 시간을 줄이는 것이 중요합니다.

## 🤔 회고 및 다음 단계
- **적용 분야:** 재고 관리 시스템, 은행 애플리케이션, 예약 시스템 등 공유 리소스에 대한 "읽기-수정-쓰기" 패턴이 필요한 모든 시나리오에 유용합니다.
- **다음 학습 주제:** `FOR SHARE` (PostgreSQL) 또는 `LOCK IN SHARE MODE` (MySQL)와 같은 공유 잠금(shared lock) 모드를 학습해볼 수 있습니다. 또한, 대안으로서 버전 컬럼을 사용하는 낙관적 잠금(optimistic locking)에 대해 알아보는 것도 좋습니다.

## 🔗 참고 자료
- [PostgreSQL: Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html)
- [MySQL: Locking Reads](https://dev.mysql.com/doc/refman/8.0/en/innodb-locking-reads.html)