# Lazy

✅ Kotlin의 by lazy 정리
📌 정의
by lazy는 Kotlin의 지연 초기화(Lazy Initialization) 방식으로, 해당 프로퍼티가 처음으로 호출될 때 초기화되고, 이후에는 캐시된 값을 재사용한다.

```kotlin
val value: Type by lazy {
    // 초기화 로직
}
```

# ⚙️ 동작 방식
최초 접근 시 초기화 블록이 실행된다.

이후에는 해당 값을 메모리에 저장해두고, 같은 값을 반환한다 (한 번만 초기화됨).

기본적으로 스레드 안전(synchronized) 하다.

# ✅ 사용 목적
성능 최적화
→ 비용이 큰 연산(예: DB 연결, 복잡한 계산)을 최초 접근 시까지 미뤄서 전체 성능 향상

메모리 절약
→ 사용되지 않는 값은 아예 초기화하지 않아 메모리 낭비 방지

코드 간결화
→ 초기화 시점 제어 + 명확한 선언 방식 → 유지보수성 향상

초기화 순서 제어
→ 의존성이 있는 객체들이 있을 때 적절한 시점에 안전하게 초기화

# ✅ 장점
장점	설명
🎯 지연 초기화	필요할 때만 초기화되어 자원 절약
🚀 성능 최적화	무거운 연산을 처음 한 번만 실행
🧠 코드 간결성	명시적인 초기화 코드를 줄일 수 있음
💾 메모리 절약	안 쓰면 초기화도 안 함
🧩 초기화 순서 관리	순차적, 안전한 초기화 가능

# ❌ 단점
단점	설명
🐢 첫 접근 시 딜레이	초기화 비용이 한꺼번에 발생할 수 있음
🐛 예상치 못한 지연 초기화	초기화되지 않은 상태에서 접근 시 문제 발생
🔍 디버깅 어려움	언제 초기화되는지 파악 어려움
🔄 동시성 문제 가능성	동기화 설정이 잘못되면 race condition 발생 가능
🧶 설계 복잡도 증가	너무 자주 쓰면 흐름이 불명확해질 수 있음

# ✅ 실전 예시
```kotlin
val heavyResource: String by lazy {
    println("Initializing resource...")
    Thread.sleep(2000)
    "Loaded"
}

fun main() {
    println("Before access")
    println(heavyResource) // 여기서만 초기화
    println(heavyResource) // 캐시된 값 사용
}
```
📌 출력:

```mathematica
Before access
Initializing resource...
Loaded
Loaded
```

🧪 LazyThreadSafetyMode
```kotlin
val nonThreadSafe: String by lazy(LazyThreadSafetyMode.NONE) { ... }
val threadSafe: String by lazy(LazyThreadSafetyMode.SYNCHRONIZED) { ... }
val threadSafeOnce: String by lazy(LazyThreadSafetyMode.PUBLICATION) { ... }
```

# ❓ 언제 사용하면 좋은가?
리소스 소비가 크고 자주 쓰이지 않는 경우

순환 참조나 초기화 순서가 중요한 상황

UI 초기화 (Android ViewModel 등)

설정 값이나 환경 정보의 지연 초기화

# 요약 문장 한 줄
by lazy는 무거운 초기화 작업을 딱 한 번만, 정확히 필요할 때만 실행하고 캐싱하는 Kotlin의 지연 초기화 기능이다.

