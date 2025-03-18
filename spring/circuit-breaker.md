# Circuit Breaker

시스템 장애를 방지하고 복원력(resilience)를 높이기 위해 사용하는 디자인 패턴이다

## 왜 필요한가
마이크로서비스에서 한 서비스가 느려지면 다른 서비스도 연쇄적으로 영향을 받는다 
최악의 경우 전체 시스템이 멈추게 된다
Circuit Breaker는 이런 장애 전파를 막기 위해 동작한다

## 동작방식
1. Closed (닫힘)
  - 모든 요청이 정상적으로 서비스로 전달됩니다.
  - 실패 횟수를 카운팅하며, 정해진 임계치를 넘지 않으면 그대로 유지됩니다.
2. Open (열림)
  - 실패가 일정 횟수나 비율을 넘으면 차단기가 열려서, 모든 요청을 바로 실패로 처리합니다.
  - 서비스가 회복될 시간을 주어, 시스템 과부하를 막는 역할을 해요.
3. Half-Open (반열림)
  - 일정 시간이 지난 후, 일부 요청만 서비스로 보내서 정상 여부를 확인합니다.
  - 성공하면 다시 Closed 상태로 돌아가고, 실패하면 Open 상태를 유지해요.

## 장점
- 장애 전파 방지: 서비스가 실패하면 실패응답을 바로 반환한다
- 빠른 복구: 장애 서비스가 복구 되는지 주기적으로 확인
- 안정성: 장애 발생해도 다른 서비스는 정상 동작

## 주의
- 임계치가 너무 낮다면 정상 동작하는 서비스도 실패할 수 있다
- Open 상태에서 시간을 두고 Half-Open으로 전환해야 한다. 그렇지 않으면 장애가 계속 지속된다

![circuit breaker diagram](/images/circuit-breaker-diagram.png)
```yaml
resilience4j.circuitbreaker:
  configs:
    default:  # 기본 설정 그룹을 정의
      slidingWindowType: TIME_BASED  # 시간 기반 슬라이딩 윈도우 방식 사용
      slidingWindowSize: 60  # 60초 동안의 요청 기록을 유지하여 실패율 계산
      permittedNumberOfCallsInHalfOpenState: 10  # HALF-OPEN 상태에서 허용되는 호출 수
      waitDurationInOpenState: 60s  # OPEN 상태에서 HALF-OPEN 상태로 전환되기까지의 대기 시간
      failureRateThreshold: 60  # 서킷이 OPEN 상태로 전환되는 실패율 임계값(%)
      eventConsumerBufferSize: 10  # 이벤트 소비자 버퍼 크기
      registerHealthIndicator: true  # 헬스 인디케이터 등록 활성화
      ignoreExceptions:  # 아래 예외는 실패로 집계하지 않음
        - common.exception.ClientErrorException  # 클라이언트 오류는 실패 카운트에 포함하지 않음
  instances:
    evaluationPayment:  # 'evaluationPayment'라는 서킷 브레이커 인스턴스 생성
      baseConfig: default  # 위에서 정의한 default 설정을 사용
```