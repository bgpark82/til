# Jump Game

https://leetcode.com/problems/jump-game/

## SOLUTION 01. Recursion
- TC: O(N!)
- SC: O(N)
```java
public boolean canJump(int[] nums) {
    return dfs(nums, 0);
}

private boolean dfs(int[] nums, int idx) {
    if (idx == nums.length - 1) return true;
    if (nums[idx] == 0) return false;
        
    boolean result = false;
    int size = Math.min(nums.length - 1, idx + nums[idx]); // index는 input의 길이 이상 넘어가면 안된다
    // 사이즈가 5인 경우, 최악의 경우 5, 4, 3, 2, 1를 탐색한다. 시간복잡도는 O(5!)
    for (int i = idx + 1; i <= size; i++) {
        result |= dfs(nums, i); // 각 노드를 탐색하고 결과물을 취합할 때, true가 하나라도 있으면 반환한다
    }
    return result;
}
```

## SOLUTION 02. Recursion (Simplified)
```java
public boolean canJump(int[] nums) {
    return dfs(nums, 0);
}

private boolean dfs(int[] nums, int idx) {
    if (idx == nums.length - 1) return true;
    if (nums[idx] == 0) return false;
        
    boolean result = false;
    int size = Math.min(nums.length - 1, idx + nums[idx]); // index는 input의 길이 이상 넘어가면 안된다
    // 사이즈가 5인 경우, 최악의 경우 5, 4, 3, 2, 1를 탐색한다. 시간복잡도는 O(5!)
    for (int i = idx + 1; i <= size; i++) {
        result |= dfs(nums, i); // 각 노드를 탐색하고 결과물을 취합할 때, true가 하나라도 있으면 반환한다
    }
    return result;
}
```
- `|=`를 `if`로 변경
    - `|=`의 조건이, 하나라도 true가 있으면 true를 반환한다
    - `if (dfs(nums, i + idx)) return true`와 동일하다
    
## SOLUTION 03. Memoization
```java
public boolean canJump(int[] nums) {
    Map<Integer, Boolean> memo = new HashMap();
    return dfs(nums, 0, memo);
}

private boolean dfs(int[] nums, int idx, Map<Integer, Boolean> memo) {
    if (memo.containsKey(idx)) return memo.get(idx);
    if (idx == nums.length - 1) return true;
    if (nums[idx] == 0) return false;
        
    for (int i = 1; i <= nums[idx]; i++) {
        if (dfs(nums, i + idx, memo)) {
            memo.put(idx, true);
            return true; // 각 노드를 탐색하고 결과물을 취합할 때, true가 하나라도 있으면 반환한다
        }
    }
    memo.put(idx, false);
    return false;
}
```

## SOLUTION 04. Greedy
- TC: O(N)
- SC: O(1)
```java

public boolean canJump(int[] nums) {
    int goal = nums.length - 1;
    for (int i = nums.length - 2; i >= 0; i--) {
        if (i + nums[i] >= goal) {
            goal = i;
        }
    }
    return goal == 0;
}
```