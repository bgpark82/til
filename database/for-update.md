# SELECT FOR UPDATE

SELECT FOR UPDATE는 특정 행에 배타락을 걸기 위해 사용한다
트랜잭션 A가 배타락을 걸면 다른 트랜잭션들은 조회만 가능하고, update/delete가 불가능하다
또한, 