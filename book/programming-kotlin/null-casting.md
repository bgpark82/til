# Null과 Type Casting
```kotlin
import java.math.BigInteger
import kotlin.math.abs

fun main() {
    // 1. Null
    println(nickNameV1("William"))
    println(nickNameV2("William"))
    println(nickNameV3("William"))
    println(nickNameV4("William"))
    println(nickNameV5("Will"))
    
    // 2. Type casting
    println(Animal("cow") == Animal("cow")) // true
    println(Animal("cow") == Animal("duck")) // false
    println(AnimalV2("cow") == AnimalV2("cow")) // true
    println(AnimalV2("cow") == AnimalV2("duck")) // false
    
    println(whatToDo(2)) // 숫자 가능
    println(whatToDo("2"))
    
    // 4. 명시적 캐스팅
    for (id in 1..2) {
        // as: 타입이 다르면 에러
        // as?: 타입이 다르면 null 반환 (안전한 캐스팅)
        val message: String? = fetchMessageV1(id) as? String

        println("Message length: ${message}")
    }
    
    // 캐스팅 bottom line
    // 1. 가능한 스마트 캐스팅 사용
    // 2. 불가능 -> 안전한 캐스트 연산자 (as?)
}


// 1. Null
fun nickNameV1(name: String?): String? {
    if (name == "William") {
        return "Bill"
    }
    return null
}

// 자바였으면 이렇게 작성했을 것이다
fun nickNameV2(name: String?): String? {
    if (name != null) {
        return name.reversed().uppercase() 
    }
    return null
}

// Safe call 연산자: null이면 null을 리턴 (값 추출용)
fun nickNameV3(name: String?): String? {
	return name?.reversed()?.uppercase()
}

// Evis 연산자: null이면 다른것을 반환 (값 추출용)
fun nickNameV4(name: String?): String {
	return name?.reversed()?.uppercase() ?: "Joker"
}

// when: null 가능 참조 처리
fun nickNameV5(name: String?): String {
	return when (name) {
        "William" -> "Bill"
        null -> "Joker" // Evis 연산자
        else -> name.reversed().uppercase() // 앞에서 null 체크를 했기 때문에 name이 null이 아님을 확신할 수 있다
    }
}

// 2. Casting
// 타입 체크는 최소화 해야한다 
// - 확장성 측면에서 좋지 않다
// - 개방 폐쇄 원칙에 위배된다
// 하지만 아래 상황은 반드시 해야한다
// - equals
// - when
//
// equals 는 == 와 같다 (매핑된다)

// 스마트 캐스팅
// @Override public boolean equas(Object other) {
//    if (other instanceof Animal) {
//        return age == ((Animal) other).age; // 최악, 이미 타입체크를 했는데 타입 캐스팅을 또해야 한다, 전혀 "스마트"하지 못하다
//    }
//    return false
// }

class Animal(val name: String) {
    override operator fun equals(other: Any?): Boolean {
        return if (other is Animal) name == other.name else false
    }
}

class AnimalV2(val name: String) {
    override operator fun equals(other: Any?): Boolean {
        // 만약 null타입이 null이 안된다고 판별되면 null 불가 타입으로 캐스팅 된다
		return other is AnimalV2 && name == other.name
    }
}

// 3. when : 들어오는 타입에 따라 동적으로 감지한다 -> 진짜 스마트
fun whatToDo(dayOfWeek: Any) = when (dayOfWeek) {
    "Satureday", "Sunday" -> "Relax"
    in listOf("Monday", "Tuesday", "Wednesday", "Thursday") -> "Work Hard"
    is String -> "What" // Any -> String
    in 2..4 -> "Work Hard"
    else -> "idk"
}


// 4. 명시적 타입
// 1이면 String, 아니면 StringBuilder를 반환한다
fun fetchMessageV1(id: Int): Any = if (id == 1) "Record found" else StringBuilder("data not found") 
```