# Course Schedule

https://leetcode.com/problems/course-schedule/description/

# SOLUTION 01: Depth First Search
- Time Complexity: O(V + E) (V: vertices, E: edges)
- Space Complexity: O(V + E) (V: vertices, E: edges)
```java
    /**
        prerequisites[a, b]: b -> a 
        7 courses : 0 ~ 6
        true if finish all courses

        [[2,1],[3,2],[4,3]]
        1 -> 2 
                -> 3 -> 4
    */
    // graph
    private Map<Integer, List<Integer>> map = new HashMap();
    // visited
    private Set<Integer> visited = new HashSet();

    public boolean canFinish(int numCourses, int[][] prerequisites) {
        // setup
        for (int i = 0; i < numCourses; i++) {
            map.put(i, new ArrayList());
        }
        // 2: 1,0 (2를 듣기 위해서는 1과 0을 무조건 수강해야 한다)
        // 3: 2 (3를 듣기 위해서는 2를 무조건 수강해야 한다)
        for (int[] pre : prerequisites) {
            map.get(pre[0]).add(pre[1]);
        }

        // dfs
        for (int c = 0; c < numCourses; c++) {
            // 각각의 코스를 하나하나 방문
            if (!dfs(c)) return false;
            // 각 코스 중 하나라도 false라면
        }
        return true;
    }

    /**
        map
        1: 2,3
        2: 
        3: 1,2
        4: 
        5: 
        6:

        1 3 // 사이클이 발생하는 즉시 false 반환
        1 3 2
    */
    private boolean dfs(int crs) {
        // 이미 방문했다면 cycle 상태
        if (visited.contains(crs)) return false;

        // 현재 노드는 갈 곳이 없음, 혹은 방문 완료
        if (map.get(crs).isEmpty()) return true;

        visited.add(crs);
        // 현재 강의를 수강하기 위한 사전 강의 리스트
        for (int pre: map.get(crs)) {
            if (!dfs(pre)) return false;
        }
        // 방문을 했다면 사전강의를 들은 상태
        visited.remove(crs);
        map.put(crs, new ArrayList());
        // 현재 노드는 별 문제 음슴
        return true;
    }
```
시간 복잡도가 V + E인 이유
- V는 노드로 그래프를 만드는 시간 (Map에 초기화 시간)
- E는 dfs로 노드를 방문하는 시간

> - 그래프의 특징상 노드가 적더라도 간선은 많을 수 있다
> - 예를들어, 노드가 5개이고 간선이 100개라면, 결국 100번 방문해야 한다.
> - 각 하나의 노드를 방문하고, 모든 간선을 방문하는 경우 = O(1 * E)
> - 모든 노드를 방문하고, 각 하나의 간선을 방문하는 경우 = O(V * 1)        
    

