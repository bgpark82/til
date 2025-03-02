# Map.computeIfAbsent
- java 8 도입

설명
- 키가 존재하면, 해당 해당 키의 **값을 반환**
- 키가 존재하지 않으면, **두번째 인자를 실행**, **반환값을 맵에 저장**하고 **값을 반환**
```java
default V computeIfAbsent(K key, Function<K, V> function)
```

예시
```java
Map<Integer, Set<String>> map = new HashMap();
HashSet<String> set = map.computeIfAbsent(1, key -> new HashSet());
```
