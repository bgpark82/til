# Generic

```kotlin
fun main() {
 	/**
 	 * Generic
 	 * 
 	 * 자바에서는 타입 불변성을 강조
 	 * - T의 타입이 정확히 일치해야 했다
 	 * - T의 부모나 자식은 사용 불가능했다
 	 * 
 	 * 공변성 (covariance)
 	 * - T의 자식 클래스도 허용 (부모 -> 자식)
 	 * - <? extends T> (?: 는 이미 선언된 Generic의 타입을 유연하게 사용)
 	 * - 제네릭을 사용할 때는 가능, 선언할 때는 사용 불가능 (class Cage<? extends Animal> : 이렇게 선언할 때는 불가능)
 	 * 
 	 * 코틀린은 선언할 때, 사용할 때 둘다 허용한다
 	 * 
 	 * 반공변성
 	 * - 자식 타입이 기대되는 곳에 부모 타입을 사용하는 것 (자식 -> 부모)
 	 * 
 	 */
    
    /**
     * 코틀린
     * 
     * 공변성
     * - 자식이 부모로 대체
     * - <out 부모>
     * - 반환 전용 생성자
     * 
     * 반공변성
     * - 부모가 자식으로 대체
     * - <in 부모>
     * - 매개변수에만 사용 가능
     * 
     * 스타프로젝션
     * - 제네릭 타입 인자를 모를 때
     * - 타입에 구애받지 않고 읽고 쓸때
     * - 모든 타입의 리스트를 받을 수 있음
     * - 타입을 알 수 없기 떄문에 "읽기 전용"만 가능
     * - Any?로 취급됨
     */ 
    //getFruitsV1(arrayOf<Banana>()) // type mismatch 에러, array는 뮤터블, class Array<T>로 정의하므로 불가능
    getFruitsV2(listOf<Banana>()) // 정상 동작, list는 이뮤터블, interface List<out E>로 정의하므로 가능하다
   
}


// 1. 공변성: 상속관계에서 타입간 변환이 자연스럽게 이뤄지는 성질
open class Fruit
class Banana: Fruit()
class Orange: Fruit()

fun getFruitsV1(fruits: Array<Fruit>) {
    println("Number of fruits: ${fruits.size}")
}

fun getFruitsV2(fruits: List<Fruit>) {
    println("Number of fruits: ${fruits.size}")
}

open class Animal
class Dog : Animal()
class Box<out T>(val item: T) {
    fun getItem(): T = item
}

// 2. 타입 프로젝션
fun copyFromTo(from: Array<Fruit>, to: Array<Fruit>) {
    for (i in 0 until from.size) {
        to[i] = from[i]
    }
}

// 3. 스타프로젝션
fun printItem(items:List<*>) //타입이 Any로 처리됨
```