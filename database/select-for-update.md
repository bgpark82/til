# SELECT FOR UPDATE

SELECT FOR UPDATE는 특정 행에 배타락을 걸기 위해 사용한다
- 트랜잭션 A가 특정행에 배타락을 걸면 다른 트랜잭션들은 조회만 가능하다
- update와 delete는 불가능하다
- 해당 행은 다른 트랜잭션이 배타락을 걸 수 없다

```sql
-- Transaction A 시작
BEGIN;
SELECT * FROM payment WHERE id = 1 FOR UPDATE;

-- Transaction B 시작
BEGIN;
SELECT * FROM payment WHERE id = 1 FOR UPDATE; -- 불가능: 1번 행은 이미 배타락이 걸려있으므로 불가능하다
SELECT * FROM payment WHERE id = 1; -- 가능: 조회는 가능하다
UPDATE payment SET status = COMPLETE WHERE id = 1; -- 불가능: 업데이트는 불가능하다 
```
언제 사용할까?
- 하나의 트랜잭션만 값을 변경하고 싶을 때
- 내가 데이터를 읽고 곧바로 변경할 때!
    1. ATM 출금처리: 다른 트랜잭션이 동일한 계좌를 변경 못함
```sql
BEGIN;
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;
```
    2. 주문 재고 차감
```sql
BEGIN;
SELECT stock FROM products WHERE id = 1 FOR UPDATE;
UPDATE products SET stock = stock - 1 WHERE id = 1;
COMMIT;
``` 
배타락을 대기를 막기 위해서는?
- `SKIP LOCK` 사용
- 락이 걸려있으면 잠그지 않는다



# SELECT FOR SHARE
SELECT FOR UPDATE는 특정 행에 공유락을 걸기 위해 사용한다
- 트랜잭션 A가 특정행에 공유락을 걸면 다른 트랜잭션들은 조회와 공유락을 걸 수 있다
- update와 delete는 불가능하다
- 해당 행은 다른 트랜잭션들이 공유락을 걸 수 있다
```sql
-- Transaction A 시작
BEGIN;
SELECT * FROM payment WHERE id = 1 FOR SHARE;

-- Transaction B 시작
BEGIN;
SELECT * FROM payment WHERE id = 1 FOR SHARE; -- 가능: 1번 행은 여러 트랜잭션에 의해 공유락을 걸 수 있다
SELECT * FROM payment WHERE id = 1; -- 가능: 조회는 가능하다
UPDATE payment SET status = COMPLETE WHERE id = 1; -- 불가능: 업데이트는 불가능하다 
```
언제 사용하늕가?
- 여러 프로세스가 같은 데이터를 기반으로 판단할 떄: 데이터를 수정 못하므로 평가 중에 값을 바꿀 수 없다
- 즉, 여러 트랜잭션이 트랜잭션 내에서 값 변경없이 조회할 때
근데 왜 여러 트랜잭션에 공유락을 걸까?
- 모든 것은 트랜잭션이 시작하고 종료되기 전에 일어난다
- 트랜잭션 A가 1행에 공유락을 걸고, 트랜잭션 B가 1행에 공유락을 걸면, 트랜잭션 A와 B 둘다 데이터를 변경할 수 없다
이미 공유락을 걸면 배타락은 걸 수 있을까?
- 공유락이 걸려있으면 배타락도 걸 수 없고 오직 공유락만 걸 수 있다
