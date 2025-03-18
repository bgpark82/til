# DSL

```kotlin
import java.util.Calendar
import DateUtil.Tense.*

class DateUtil (
	val number: Int,
    val tense: Tense
) {
    enum class Tense {
       ago, from_now
    }
    override fun toString(): String {
        val today = Calendar.getInstance()
        when (tense) {
            ago -> today.add(Calendar.DAY_OF_MONTH, -number)
            from_now -> today.add(Calendar.DAY_OF_MONTH, number)
        }
        return today.getTime().toString()
    }
}

// DSL
// 1. 외부 DSL: 높은 자유도, 파서 필요
// 2. 내부 DSL: 파서 필요 x
//		- 새미콜론 생략 가능: 노이즈가 적음
//		- infix: 점과 괄호 제거, 영어처럼 보임, 중위표기법 지원 (피연산자 사이 위치하는 수학적 표시)
//		- 확장함수로 도메인 특화: 함수를 타입에 인젝팅 가능 (2.days(ago) -> 2 days ago)
//		- 람다 전달시 괄호제거 : 함수 마지막 파라미터가 람다면 괄호 밖에 위치
//		- 암시적 리시버 : 

infix fun Int.days(timing: DateUtil.Tense) = DateUtil(this, timing)
println(2.days(ago))
println(2 days ago)

```

## Custom DSL
```kotlin
fun main() {
    
    "Release meeting" meetingV1 { 
        println("meetingV1")
    }
    
    "Release meeting" meetingV2 {
        println("meetingV2: $this")
    }
    
    "Release meeting" meetingV3 {
        println("meetingV3: $this")
        at(14.30)
        by(15.20)
    }

    "Release meeting" meetingV4 {
        println("meetingV3: $this")
        // this at 14.30 // infix는 객체 참조 (this) 반드시 필요
        // this by 15.20
        start at 14.30
        end by 15.20
    }
    
    "Release meeting" meetingV5 {
        println("meetingV5: $this")
        start at 14.30
        end by 15.20
	}
}

infix fun String.meetingV1(block: () -> Unit) {
    println("step 1")
	block() // 여기서 println("meetingV1")이 실행된다
}

// Meeting.() -> Unit으로 meeting의 확장함수로 만들어야 한다
infix fun String.meetingV2(block: MeetingV1.() -> Unit) {
    println("step 2")
	val meeting = MeetingV1()
    meeting.block() // 여기서 println("meetingV2")가 실행되는데 Meeting(리시버)이라는 객체에 바인딩된다
    println(meeting)
}

class MeetingV1

infix fun String.meetingV3(block: MeetingV2.() -> Unit) {
    println("step 3")
    val meeting = MeetingV2(this) // this는 String(receiver)을 뜻한다
    meeting.block()
    println(meeting)
}

class MeetingV2(val title: String) {
    
    var startTime: String = ""
    var endTime: String = ""
    
    // at과 by가 뭘 의미하는지 모르겠다, 괄호도 왜 있는걸까
    fun at (time: Double) { startTime = convertToString(time) } 
    fun by (time: Double) { endTime = convertToString(time) }
    
    private fun convertToString(time: Double) = String.format("%.02f", time)
    
    override fun toString() = "$title meeting starts $startTime end $endTime"
}

infix fun String.meetingV4(block: MeetingV3.() -> Unit) {
    println("step 4")
    val meeting = MeetingV3(this) // this는 String(receiver)을 뜻한다
    meeting.block()
    println(meeting)
}

class MeetingV3(val title: String) {
    
    var startTime: String = ""
    var endTime: String = ""
    
    // start가 by를, end가 at을 부를 수 있음
    val start = this
    val end = this
    
    infix fun at (time: Double) { startTime = convertToString(time) } 
    infix fun by (time: Double) { endTime = convertToString(time) }
    
    private fun convertToString(time: Double) = String.format("%.02f", time)
    
    override fun toString() = "$title meeting starts $startTime end $endTime"
}

open class MeetingTime(var time: String = "") {
    protected fun convertToString(time: Double) = String.format("%.02f", time)
}

class StartTime : MeetingTime() {
    infix fun at (theTime: Double) { time = convertToString(theTime) } 
}

class EndTime : MeetingTime() {
    infix fun by (theTime: Double) { time = convertToString(theTime) } 
}

class MeetingV4(val title: String) {
    val start = StartTime()
    val end = EndTime()

    override fun toString() = "$title meeting starts ${start.time} end ${end.time}"
}

    
infix fun String.meetingV5(block: MeetingV4.() -> Unit) {
    println("step 5")
    val meeting = MeetingV4(this) // this는 String(receiver)을 뜻한다
    meeting.block()
    println(meeting)
}
```