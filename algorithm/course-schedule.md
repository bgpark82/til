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

        그래프의 핵심은 관계이다
        주로 만드는 방법은 map 혹은 nxn 배열로 관계를 만든다
        예를들어, 1번 강의를 수강하기 위해서 2, 3번을 수강해야 한다면 관계는 다음과 같다
        1: [2, 3]
        - map
        - NxN 배열

        또한 그래프는 방문 여부가 중요하다
        만약 방문을 했다면, 해당 노드는 재방문할 수 없다
        보통 map을 만들어서 방문 여부를 모두 기록하거나
        set을 만들어서 노드 방문여부를 체크한다
        - map
        - NxN 배열
        - set

        그래프의 방문 또한 중요하다
        보통 dfs 혹은 bfs를 사용한다
        만약 최단 경로를 방문하고 싶다면 bfs
        그렇지 않다면 일반적으로 dfs를 사용한다

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
    // 특정 노드로 부터 시작된 그래프에 cycle이 있는지 확인
    private boolean dfs(int crs) {
        // 이미 존재한다면 사이클 발생한 상태
        if (vistied.contains(curr)) return false; 

        // curr이 empty면 더이상 방문할 노드가 없는 상태 (사이클이 아닌 상태)
        if (map.get(curr).isEmpty()) return true; 

        visited.add(crs);
        // 현재 강의를 수강하기 위한 사전 강의 리스트
        for (int pre: map.get(crs)) {
            // 다음 노드에 cycle이 있는 경우 바로 false
            if (!dfs(pre)) return false;
        }
        // 방문을 했다면 사전강의를 들은 상태
        visited.remove(crs);
        // 이미 모두 방문했기 때문에 없애 버린다. 이건 최적화를 위해서이다. 
        // 자식 노드를 모두 방문했었던 노드라면, 자식을 방문할 필요가 없다
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
    
# SOLUTION 02: Topological Sort
- Time Complexity: O(V + E) (V: vertices, E: edges)
- Space Complexity: O(V + E) (V: vertices, E: edges)
```java
public boolean canFinish(int numCourses, int[][] prerequisites) {
        // 전입차수 계산
        int[] indegree = new int[numCourses];
        
        // 관계 설정
        List<List<Integer>> adj = new ArrayList();
        for (int i = 0; i < numCourses; i++) {
            adj.add(new ArrayList());
        }
        for (int[] pre : prerequisites) {
            // pre[0]가 들어야 하는 선수과목 개수
            indegree[pre[1]]++;
            adj.get(pre[0]).add(pre[1]);
        }

        // 전입차수가 0인 큐 넣기
        Queue<Integer> q = new LinkedList();
        for (int i = 0; i < numCourses; i++) {
            if (indegree[i] == 0) {
                q.add(i);
            }
        }

        // 큐를 돌면서 확인
        int finish = 0;
        while (!q.isEmpty()) {
            int node = q.poll();
            // 방문회수인가?
            finish++;

            // 선수과목들 확인
            for (int nei : adj.get(node)) {
                indegree[nei]--;
                if (indegree[nei] == 0) {
                    q.add(nei);
                }
            }
        }

        // 방문한 횟수가 모두 같으면 사이클이 없음
        return finish == numCourses;
    }
```
Topological Sort는 그래프의 순서를 정렬하는 방법이다
- 선후 관계가 있는 그래프를 나열하는 방법
    - 예를들어, 강의 수강, 작업 순서 등
- 동작 방식
    1. 각 노드에 들어오는 간선의 개수를 센다
    2. 전입차수가 0인 노드를 찾는다
    3. 전입차수가 0인 노드를 큐에 넣고 처리한다
    4. 해당 노드가 연결된 노드의 전입차수를 1 감소시킨다
    5. 전입차수가 0인 노드를 큐에 넣고 처리한다
    6. 큐가 비어있으면 사이클 발생
    
