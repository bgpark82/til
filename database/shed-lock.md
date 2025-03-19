# Shed lock

**ShedLock**은 다중 인스턴스 환경에서 스케줄된 작업(예: Spring의 `@Scheduled` 작업)이 **한 번만 실행**되도록 보장하는 라이브러리입니다.  

### 🚨 **왜 필요한가요?**
마이크로서비스 아키텍처나 다중 인스턴스 환경에서는 여러 서버가 같은 코드를 실행하므로, 스케줄링 작업이 인스턴스마다 중복 실행될 위험이 있습니다.  
예를 들어, 3대의 서버가 같은 `@Scheduled` 작업을 실행하면, 한 작업이 3번 실행될 수 있죠. ShedLock은 이를 방지해 **하나의 인스턴스만 작업을 실행**하도록 보장합니다.  

### ⚙️ **어떻게 작동하나요?**
1. **락 획득:** 작업 실행 전에 DB(또는 다른 공유 자원)에 락(lock)을 걸어 "이 작업은 내가 맡았다"고 선언합니다.
2. **작업 실행:** 락을 성공적으로 획득한 인스턴스만 작업을 실행합니다.
3. **락 해제:** 작업이 끝나거나 타임아웃되면 락을 해제합니다.  

### 📦 **간단한 사용법 (Spring Boot 기준)**

1. **의존성 추가 (Gradle 예시):**

```gradle
implementation 'net.javacrumbs.shedlock:shedlock-spring:5.3.0'
implementation 'net.javacrumbs.shedlock:shedlock-provider-jdbc-template:5.3.0'
```

2. **설정 클래스 추가:**  
```java
@Configuration
@EnableScheduling
@EnableSchedulerLock(defaultLockAtMostFor = "10m")
public class SchedulerConfig {
}
```

3. **스케줄 작업에 락 걸기:**  
```java
@Component
public class MyScheduledTask {

    @Scheduled(cron = "0 0 * * * ?") // 매 정시마다 실행
    @SchedulerLock(name = "MyScheduledTask", lockAtMostFor = "10m", lockAtLeastFor = "1m")
    public void executeTask() {
        System.out.println("작업 실행 중...");
    }
}
```

4. **DB 테이블 생성:** (JDBC 사용 시)

```sql
CREATE TABLE shedlock (
    name VARCHAR(64) NOT NULL PRIMARY KEY,
    lock_until TIMESTAMP(3) NULL,
    locked_at TIMESTAMP(3) NULL,
    locked_by VARCHAR(255)
);
```

이렇게 설정하면 여러 인스턴스가 있어도 **하나의 인스턴스만 작업을 실행**하게 됩니다. 🚀  

더 궁금한 게 있으면 편하게 물어봐요! 🙂


# 현재 진행중인 이슈
1. 해결법
The lock mechanism initially used for TransactionPersistence is shedlock. At the same time was implemented a cronjob that unlocks everything at night to let the chance to the persistence to kick in again the next day. As unlocking means removing all locks from the shedlock table and that now new processes use shedlock, there can be issues indeed.
 
What could have happened is that : one pod locked and started deletion, unlocking cron kicked in, an other pod locked and try to delete the same entries that the initial pod deleted. 
 
My suggestion would be to make payment deletion use advisory locks or specialise the unlocking cron.

2. 변경분
- https://gitlab.dev.codefactory.sh/banking-platform/service-accounts-api/-/merge_requests/2908/diffs