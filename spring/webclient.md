# WebClient

## WebClient 설정
```kotlin
@Validated // 인터페이스, 클래스의 메소드 레벨에서 검증 활성화, 이 경우는 클래스 전체 메소드 (@Valid는 객체 자체를 검증)
interface GenericWebClientPropertiesV1 {

    // 필드를 get할 때 검증
    @get:NotBlank
    val url: String

    @get:Valid // 객체 내부의 중첩객체 검증
    val timeout: TimeoutProperties

    fun configure(
        builder: WebClient.Builder,
        webClientProperties: WebClientProperties
    ): WebClient.Builder = builder.apply { builder ->
        builder.baseUrl(url)
            .codecs { configurer ->
                configurer.defaultCodecs()
                    // 메모리에서 변환할 때 한번에 변환 가능한 크기
                    // 웹 클라이언트는 데이터를 청크 단위로 읽음
                    // 만약 1mb로 지정했는데 데이터가 더 크다면 에러발생
                    .maxInMemorySize(DataSize.ofMegabytes(webClientProperties.maxInMemorySize).toBytes().toInt())
            // 커넥터로 네트워크 연결관리 (Netty)
            // 커넥션 풀 관리, 타임아웃 설정, SSL 설정, Netty, HttpClient 선택 가능
            }.clientConnector(
                // Reactor Netty 기반 커넥터
                            ReactorClientHttpConnector(
                    HttpClient.create()
                        // 시스템 프로퍼티에 설정된 프록시를 사용,
                        // 시스템 프로퍼티 jvm 실행할 때 전달하는 변수 (-D)
                        .proxyWithSystemProperties()
                        .option(CONNECT_TIMEOUT_MILLIS, webClientProperties.connectionTimeoutInMillis)
                        .option(CONNECT_TIMEOUT_MILLIS, timeout.connection.toMillis().toInt())
                        .responseTimeout(timeout.response)
                        .doOnConnected { conn ->
                            conn.addHandlerLast(
                                ReadTimeoutHandler(
                                    webClientProperties.readTimeoutInMillis.toLong(),
                                    TimeUnit.MILLISECONDS
                                )
                            )
                            conn.addHandlerLast(
                                WriteTimeoutHandler(
                                    webClientProperties.writeTimeoutInMillis.toLong(),
                                    TimeUnit.MILLISECONDS
                                )
                            )
                        })
            )
    }
}
```