# gradle property

그레이들 빌드 설정 파일
- 프로퍼티 설정
- 환경 설정
- 보안 정보
- 빌드 성능 최적화 (병렬 빌드, 캐싱 옵션)

systemProp
- JVM 옵션의 -D로 전달
- build.gradle.kts 혹은 코드에서 에서 접근 가능
- System.getProperties(kotlinVersion)

```gradle
# gradle.properties
systemProp.javaVersion=21
systemProp.kotlinVersion=2.0.20
systemProp.springBootVersion=3.3.4
```

build.gradle.kts에서 사용가능
```gradle
// build.gradle.kts
plugins {
    /**
     * System.getProperties
     * - 자바에서 시스템 속성을 가져오는 메서드
     * - JVM이 시작할 때 설정된 시스템 속성 반환
     * - 시스템 정보, 환경 변수
     */
    val kotlinVersion: String by System.getProperties()
    val springBootVersion: String by System.getProperties()
}
```
