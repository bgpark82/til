# Hand of Straight

https://leetcode.com/problems/hand-of-straights/description/

## SOLUTION 01: Brute Force
- TC: O(NlogN)
- SC: O(N)
```java
public boolean isNStraightHand(int[] hand, int groupSize) {
        // size of hand should be multiples of groupSize
        // e.i) hand = 8, group = 4 -> 2 group 
        // e.i) hand = 7, group = 4 -> 1.X group -> false
        // if hand modulo groupSize is not zero, then we have no perfect group
        // if remainder is not zero
        if (hand.length % groupSize != 0) return false;

        // map to store the count of numbers
        Map<Integer, Integer> map = new HashMap();
        for (int num : hand) {
            map.put(num, map.getOrDefault(num, 0) + 1);
        }

        // sort to have consective array
        Arrays.sort(hand);
        // check consecutive numbers
        for (int num : hand) {
            // if already visited then we can skip
            if (map.get(num) <= 0) continue;
            // window of number from num to groupSize
            for (int i = num; i < num + groupSize; i++) {
                // if it's not consecutive then return false
                if (map.getOrDefault(i, 0) == 0) return false;
                map.put(i, map.get(i) - 1);
            }
        }
        return true;
    }
```
그리디는 정말 피지컬로 풀어야되는게 아닐까?
- 전형적인 패턴같은게 없으니 정말 컴퓨터가 연산하는 방식대로 생각해야 되는 것 같다