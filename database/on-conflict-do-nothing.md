# ON CONFLICT DO NOTHING

ON CONFLICT DO NOTHING은 PostgreSQL과 같은 SQL 데이터베이스에서 사용하는 구문으로, 데이터 삽입(INSERT) 시에 **충돌(conflict)**이 발생하면 아무 작업도 하지 않고 무시하라는 의미야.

쉽게 말해서:
어떤 행(row)을 INSERT 하려고 했는데,

이미 그 Primary Key나 Unique 제약조건을 만족하는 데이터가 테이블에 존재하면,

원래는 에러가 나는데,

ON CONFLICT DO NOTHING을 쓰면 그 에러를 무시하고 그냥 넘어감.

예시
sql
Copy
Edit
INSERT INTO users (id, name)
VALUES (1, 'Alice')
ON CONFLICT DO NOTHING;
만약 id = 1인 사용자가 이미 있다면?
→ 그냥 아무 일도 안 하고 넘어감.

없다면?
→ id = 1인 새로운 유저 삽입됨.

언제 쓰냐?
데이터 중복 삽입을 방지하면서,

충돌 시 오류를 피하고 싶을 때.

예: 로그 저장, 중복 사용자 등록 방지, 비 idempotent한 API 호출 시 안전하게 사용.

