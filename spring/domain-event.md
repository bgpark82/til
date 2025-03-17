# Domain Event
https://dev.to/kirekov/spring-data-power-of-domain-events-2okm

스프링에서는 여러 방식으로 이벤트를 전달 할 수 있다

## 1. ApplicationEventPublisher

- 스프링 컨텍스트에 이벤트를 전달할 수 있다

    
```kotlin
@Component
class PaymentService(
    private val eventPublisher: ApplicationEventPublisher
) {
    fun completeOrder(payment: Payment) {
        payment.completeOrder()
    }
}
```


## 2. @DomainEvents
- 도메인 객체에서 도메인 이벤트를 전송할 수 있다
```kotlin
@Entity
class Payment(

    @Id
    @GeneratedValue
    val id: Long,

    val amount: BigDecimal,

    var status: String = "CREATED",

) {

    @Transient
    private val domainEvents = mutableListOf<Any>()

    fun completeOrder() {
        status = "COMPLETED"
        registerEvent(OrderCompletedEvent(id))
    }

    fun registerEvent(event: OrderCompletedEvent) {
        domainEvents.add(OrderCompletedEvent(id))
    }

    /**
     * 도메인 이벤트 발생
     * - save, saveAll
     * - delete, deleteAll, deleteAllInBatch, deleteInBatch
     * - 해당 메소드들을 aggregateRoot를 argument로 받기 때문에, deleteById는 포함되지 않는다
     */
    @DomainEvents
    fun domainEvent(): List<Any> = domainEvents.toList()

    /**
     * 도메인 이벤트 발생 후 호출
     */
    @AfterDomainEventPublication
    fun callbackMethod() {
        // 도메인 이벤트 리스트 초기화
        domainEvents.clear()
    }
}
```

도메인 이벤트를 수신
```kotlin
@Component
class PaymentListener {
    @EventListener
    fun onPaymentCompleted(event: PaymentCompletedEvent) {
        println("Payment completed: ${event.paymentId}")
    }
}
```

## 2. AbstractAggregateRoot
- AbstractAggregateRoot는 도메인 이벤트를 전송할 수 있는 기본 클래스
- Bolderplat를 제거할 수 있다
```kotlin
@Entity
class Payment(

    @Id
    @GeneratedValue
    val id: Long,

    val amount: BigDecimal,

    var status: String = "CREATED",

) : AbstractAggregateRoot<Payment>() {

    @Transient
    private val domainEvents = mutableListOf<Any>()

    fun completeOrder() {
        status = "COMPLETED"
        registerEvent(OrderCompletedEvent(id))
    }
}
```