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