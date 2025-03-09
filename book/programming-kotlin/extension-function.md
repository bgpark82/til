# 확장함수

```kotlin
import java.math.BigInteger
import kotlin.math.abs

// 1. 연산자 오버로딩
val num1 = BigInteger("100")
val num2 = BigInteger("200")
println(num1 + num2)
println(Complex(4,2) * Complex(-3, 4)) // -20 + 10
println(Money(100) + Money(200))

// 2. 확장함수
val circle = Circle(100, 100, 25)
val point1 = Point(110, 110)
val point2 = Point(10, 100)
println(circle.containsV1(point1))
println(circle.containsV1(point2))
println(buildString {
    append("hello ")
    append("word")
})

// 3. 중위 표기법
println(circle contains point1)

// 4. also, let, run, apply
val format = "%-10s%-10s%-10s%-10s"
val str = "context"
val result = "RESULT"
fun toString() = "lexical"

println(String.format(format, "Method", "Argument", "Receiver", "Return", "Result"))
println("==============================")
// let
// let을 호출한 객체를 아규먼트로 전달, 스코프(this)는 렉시컬 스코프 (람다가 정의된 스코프에 바인딩), 람다 결과를 반환
val result1 = str.let { arg -> 
    print(String.format(format, "let", arg, "lexical", result))
    result
}
println(String.format("%-10s", result1))

// also
// also를 호출한 객체를 아규먼트로 전달, 스코프(this)는 렉시컬 스코프 (람다가 정의된 스코프에 바인딩), 람다 결과를 무시하고 arg를 무조건 반환한다
val result2 = str.also { arg -> 
    print(String.format(format, "also", arg, "lexical", result))
    result
}
println(String.format("%-10s", result2))

// run
// 아규먼트를 전달하지 않는다. 대신 run을 호출한 객체(컨텍스트 객체)를 람다의 this에 바인딩, 람다의 결과를 리턴, (즉, arg 못쓰는대신 컨텍스트 객체를 지지고 볶고 싶을 때)
val result3 = str.run {
    print(String.format(format, "run", "N/A", this, result))
    result + " " + this
}
println(String.format("%-10s", result3))

// apply
// 아규먼트를 전달하지 않는다. 대신 run을 호출한 객체(컨텍스트 객체)를 람다의 this에 바인딩, 람다의 결과를 무시하고 this를 리턴한다
val result4 = str.apply { 
    print(String.format(format, "apply", "N/A", this, result))
    result
}
println(String.format("%-10s", result4))

// ex
val mailer = Mailer()
mailer.from("from@agil.com")
mailer.to("to@agil.com")
mailer.subject("your code sucks")
mailer.body("...details...")
println(mailer.send())

// apply
// 인스턴스명 반복을 줄일 수 있음, apply가 계속 나옴, 결과 이후 인스턴스 객체를 사용하고 싶을 때 좋음
println(Mailer()
    .apply { from("from@agile.com") }
    .apply { to("to@agile.com") }
    .apply { subject("your code sucks") }
    .apply { body("...details...")}
    .send())

// apply를 마지막으로 호출한 객체의 컨텍스트(this)에서 람다 실행
println(Mailer().apply { 
    from("from@agile.com") 
    to("to@agile.com") 
    subject("your code sucks") 
    body("...details...") 
}.send())

// run
// 인스턴스를 더 사용할 필요없이 결과 반환하고 싶을 때
println(Mailer().run { 
    from("from@agile.com") 
    to("to@agile.com") 
    subject("your code sucks") 
    body("...details...") 
    send()
})

// let
// 인스턴스를 다른 메소드의 아규먼트로 전달
// 메소드를 호출해서 다음 메소드로 연결 할 때 필요
fun createMailer() = Mailer()
fun prepareAndSend(mail: Mailer) = mailer.run { 
    from("from@agile.com") 
    to("to@agile.com") 
    subject("your code sucks") 
    body("...details...") 
    send()
}
println(prepareAndSend(createMailer())) // 괄호 여러개로 무겁게 느껴짐, 
println(createMailer().let { mailer -> prepareAndSend(mailer)}) // 좀 더 자연스럽게 읽 을 수 있음
println(createMailer().let {prepareAndSend(it)})
println(createMailer().let(::prepareAndSend))

// also
// 반환값이 없을 때 사용하면 좋음
fun prepareMailer(mailer: Mailer): Unit {
    mailer.run {
        from("from@agile.com") 
        to("to@agile.com") 
        subject("your code sucks") 
        body("...details...") 
    }
}
fun sendMail(mailer: Mailer): Unit {
    mailer.send()
    println("Mail sent")
}
val mailerV2 = createMailer() // 흐름이 그닥 좋지않다
prepareMailer(mailerV2)
sendMail(mailerV2)

createMailer()
    .also(::prepareMailer)
    .also(::sendMail)


// 1. 연산자 오버로딩
// 연산자 오버로딩에 해당하는 메소드의 명은 이미 정해져있다 (times, plus)
// 항상 새로운 객체를 반환해야 한다
data class Complex(val real: Int, val imaginary: Int) {
    operator fun times(other: Complex) = 
    	Complex(real * other.real - imaginary * other.imaginary,
               real * other.imaginary + imaginary * other.real)
        
    private fun sign() = if (imaginary < 0) "-" else "+"
    
    override fun toString() ="$real ${sign()} ${abs(imaginary)}"   
}
data class Money(val amount: Int) {
	operator fun plus(other: Money) = Money(amount + other.amount)
}

// 2. 확장함수
// 다른 JVM 언어로 작성된 클래스에 "메소드"와 "속성"을 인젝팅 가능
// 1. 같은 파일 혹은 2. 메소드가 있는 패키지를 임포트하면 함수를 사용할 수 있다
// 내부적으로는 static method를 호출하는 것과 똑같다 (인스턴스에 static method를 생성한 것 뿐!! 컴파일러가 static method로 변경해준다)
// 외부 라이브러리를 확장할 때 유용
data class Point(val x: Int, val y: Int)
data class Circle(val cx: Int, val cy: Int, val radius: Int)
fun Circle.containsV1(point: Point) = 
    (point.x - cx) * (point.x - cx) + (point.y - cy) * (point.y - cy) < radius * radius
// DSL 생성할 떄 유용
fun buildString(action: StringBuilder.() -> Unit): String {
    val sb = StringBuilder()
    sb.action()
    return sb.toString()
}

// 3. 중위 표기법
// 점과 괄호를 지워준다
// 연산자는 중위 표기법으로 가능하다 (메소드는 불가능)
// 장점: 코드의 표현력이 강해지고 노이즈가 적어진다 
// 단점: 하나의 파라미터만 받는다, vararg 사용불가, 기본 파라미터 사용 불가
operator infix fun Circle.contains(point: Point) = 
    (point.x - cx) * (point.x - cx) + (point.y - cy) * (point.y - cy) < radius * radius


// 4. also, apply, let, run
// 람다를 파라미터로 받아, 람다를 실행하고, 객체를 반환한다
class Mailer {
    val details = StringBuilder()
    fun from (addr: String) = details.append("from $addr ...\n")
    fun to (addr: String) = details.append("to $addr ...\n")
    fun subject (line: String) = details.append("subject $line ...\n")
    fun body (message: String) = details.append("body $message ...\n")
    fun send() = " .... sending \n $details"
}
```