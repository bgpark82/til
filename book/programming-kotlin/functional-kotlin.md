# Functional Kotlin

함수형 프로그래밍은 명령형 스타일 프로그래밍과 비교했을 때 덜 복잡하다. 함수형 프로그 래밍은 고차함수를 사용하고, 함수형 구성을 한다. 그래서 유동적인 코드를 쓸 수 있고, 그렇게 하면 더 쉽게 이해할 수 있고 쉽게 유지보수 할 수 있다. 람다는 이름이 없는 함수이다. 그리고 다른 함수의 아규먼트로 쉽게 전달될 수 있는 함수이다. 코틀린은 람다를 작성하는데 다양한 옵션을 제공한다. 람다가 요구되는 곳이라면 함수 레퍼런스를 전달해서 함수나 메소드를 재사용할 수 있다. 람다는 상태가 없지만 클로저가 상태를 옮긴다. 하지만 뮤터블 상태를 많이 사용하면 잠재적인 에러를 내재하게 되고 코드의 행동을 혼란스럽게 하므로 사용을 피하도록 하자. 코틀린은 람다에서 return에 대해 까다로운 규칙을 가지고 있다. 라벨 리턴을 사용할 수 있고, 논로컬 리턴은 특수한 경우에만 사용할 수 있다. 게다가 코틀린은 함수와 람다의 호출 오버헤드를 제거하기 위해서 inline 키워드를 제공한다

```kotlin
/**
    * lambda
    * - 고차함수(map, filter)에서 아규먼트로 사용되는 짧은 함수
    * - 이름이 없고, 타입추론으로 리턴 타입 가지는 함수
    * - 선언형: 파라미터, 바디 (명령형: 이름, 리턴타입, 파라미터, 바디)
    * - 멀타라인 람다는 지양한다
    * 고차함수
    * - 계산 대신 람다에게 계산 가능
    */

// 1. 고차함수의 파라미터로 람다 전송
println(isPrimeV1(5))
println(isPrimeV2(5))
println(isPrimeV3(5))
println(isPrimeV4(5))

// 2. 람다를 파라미터로 받는 람다
walkToV1({ i -> print(i) }, 5)
walkToV2(5, { i -> print(i) })
walkToV2(5) { i -> print(i) } // 콤마를 제외하고 람다를 밖으로 뺼 수도 있음
walkToV2(5) { print(it) } // 암시적 파라미터 사용 가능
walkToV2(5, ::print) // 패스수르 람다 (데이터를 변형하지 않고 그대로 전달하는 람다)는 함수이름으로 대체 가능, 람다를 참조로 대체 가능 (::)

// 3. 함수를 리턴하는 함수
val names = listOf("Pam", "Pat", "Paul", "Paula")
println(names.find { name -> name.length == 5}) // Paula
println(names.find { name -> name.length == 4}) // Paul
// 코드가 중복으로 작성됨, Write Every Time (WET, 매번 작성하는 안티패턴)
println(names.find(predicateOfLengthV1(5))) // Paula
println(names.find(predicateOfLengthV1(4))) // Paul
println(names.find(predicateOfLengthV2(5))) // Paula
println(names.find(predicateOfLengthV2(4))) // Paul
println(names.find(predicateOfLengthV3(5))) // Paula
println(names.find(predicateOfLengthV3(4))) // Paul

// 4. 익명함수
println(names.find(checkLengthV1))
println(names.find(checkLengthV2))
println(names.find(checkLengthV3))
println(names.find(checkLengthV4))
println(names.find(fun(name: String): Boolean { return name.length == 5 })) // 익명함수를 바로 사용

// 6. 라벨리턴
callerV1()
callerV2()


// 1. 고차함수의 파라미터로 람다 전송
fun isPrimeV1(n: Int) = n > 1 && (2 until n).none({i: Int -> n % i == 0})
// 람다 파라미터의 타입추론 가능
fun isPrimeV2(n: Int) = n > 1 && (2 until n).none({i -> n % i == 0})
// 고차함수가 하나의 파라미터만 받으면 괄호 생략 가능
fun isPrimeV3(n: Int) = n > 1 && (2 until n).none {i -> n % i == 0} 
// 하나의 파라미터만 받으면 암시적 파라미터 (it) 사용 가능
fun isPrimeV4(n: Int) = n > 1 && (2 until n).none { n % it == 0} 

// 2. 람다를 파라미터로 받는 람다
fun walkToV1(action: (Int) -> Unit, n: Int) = (1..n).forEach { action(it) }
// 람다를 마지막 파라미터로 사용
fun walkToV2(n: Int, action: (Int) -> Unit) = (1..n).forEach { action(it) }
// 패스스루 람다
fun walkToV3(n: Int, action: (Int) -> Unit) = (1..n).forEach(action)
 
// 3. 함수를 리턴하는 함수
fun predicateOfLengthV1(length: Int): (String) -> Boolean {
    return { name: String -> name.length == length}
}
// 타입추론: 함수가 짧고, 블록바디가 없는 경우 사용가능
fun predicateOfLengthV2(length: Int) = { name: String -> name.length == length }
fun predicateOfLengthV3(length: Int): (String) -> Boolean = { it.length == length }

// 4. 익명함수 (비권장, 비동기 프로그래밍에서나 사용)
// 리턴타입 추정: 람다의 파라미터에 타입 지정
val checkLengthV1 = {name: String -> name.length == 5 }
// 리턴타입 고정: 변수에 타입 지정
val checkLengthV2: (String) -> Boolean = { name -> name.length == 5 }
// 비권장: 변수와 람다에 타입 지정
val checkLengthV3: (String) -> Boolean = { name: String -> name.length == 5 }
// 익명함수: 변수의 타입은 타입 추론, 리턴 타입만 지정
// 제약사항: return 키워드 필요, 괄호 안에서만 사용 가능
val checkLengthV4 = fun(name: String): Boolean { return name.length == 5 }

// 5. 클로저
// 람다: 상태없음, 스코프를 로컬변수만 가짐, 클로저 "라고 불림"
val doubleItV1 = { e: Int -> e * 2 }
// 클로저: 로컬이 아닌 속성과 메소드로 스코프를 확장
// 렉시컬 스코프: 클로저가 정의된 곳에서 factor를 못찾으면, 클로저가 정의된 곳으로 "스코프"를 확장, 못찾으면 계속 스코프를 확장
val factor = 2 // 코틀린에서는 mutability가 금기이지만 변수의 var를 허용한다 (위험)
val doubleItV2 = { e: Int -> e * factor}

// 6. 비지역성(non-local)과 라벨(labled, 명시적) 리턴
// 람다는 return을 사용할 수 없다 (익명함수는 가져야 한다)
// 6-1. 라벨리턴: 람다에서 즉시 빠져나가고 싶은 경우, 스코프 밖으로 빠져나가지 못하게 막음
fun callerV1() {
    (1..3).forEach { i -> 
    	invokeWith(i) here@ { // 라벨블록으로 점프, 람다를 빠져나감 == continue
            println("enter for $it")
            if (it == 2) return@here
            println("exit for $it")
        }
        println("end of caller")
    }
}
// 묵시적 라벨리턴: 비권장 (1. 의도가 불명확, 2. 코드 이해 어려움)
fun callerV2() {
    (1..3).forEach { i -> 
    	invokeWith(i) {	// 함수로 점프, 람다를 빠져나감
            println("enter for $it")
            if (it == 2) return@invokeWith 
            println("exit for $it")
        }
    }
}
fun invokeWith(n: Int, action: (Int) -> Unit) {
    println("enter invokeWith $n")
    action(n)
    println("exit invokeWith $n")
}

```