# Vararg

- 전달되는 인자가 가변적일 때 사용
- 특정 함수가 인자 수와 관계없이 여러개의 값을 받을 때 유용
- 매개변수는 배열로 전달
- 배열을 vararg로 전달할 때는 `*` 연산자를 사용한다
```kotlin
    // vararg
    fun sum(vararg xs: Int): Int {
        println(xs::class.simpleName)
		return xs.sum()
    }  // xs는 IntArray로 취급
    fun <T> printAll(vararg ts: T) {
        println(ts.size) // vararg는 Array로 취급됨
        ts.forEach { println(it) }
    }
    // vararg는 오직 하나만 취급 가능하다
    println(sum(1,2))
    printAll(1,2)
    
    // spread operator
    val numbers = intArrayOf(1,2,3,4) 
	println(sum(*numbers)) // array -> vararg
    
    data class Person(
    	val name: String,
        val age: Int
    )
    
   	fun printPerson(vararg person: Person) {
        println()
        println(person.map {it.age to it})
    }
    printPerson(Person(name="peter", age=25))
    
```