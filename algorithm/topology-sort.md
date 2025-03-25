# Topology sort

위상정렬
- 방향성 그래프(DAG)에서 각 노드를 선행 관계에 맞게 순서대로 정렬하는 알고리즘
- 예시) A 강의를 먼저들어야 B 강의를 들을 수 있다

방법
1. 전입 차수 (indegree) 방법
    - 각 노드의 전입 차수를 계산한다
    - 전입 차수가 0인 노드를 큐에 넣는다
    - 큐에서 노드를 하나씩 커낸다
    - 노드와 연결된 다른 노드의 진입 차수를 하나씩 줄인다
    - 진입 차수가 0이된 노드를 큐에 추가한다
    - 큐가 비어 있으면 위상정렬 종료
2. DFS 방법
    - 모든 노드를 방문하지 않은 상태로 시작
    - 각 노드를 DFS로 탐색한다
    - 해당 노드와 연결된 모든 노드를 탐색한다
    - 탐색이 끝난 노드를 결과 리스트 뒤에서부터 추가한다
    - 모든 노드를 다 탐색 후 결과 리스트를 반환한다
```java
public List<Integer> findOrder(int numCourses, int[][] prerequisites) {
    Map<Integer, List<Integer>> graph = new HashMap<>();
    for (int[] prereq : prerequisites) {
        graph.computeIfAbsent(prereq[1], k -> new ArrayList<>()).add(prereq[0]);
    }

    Set<Integer> visited = new HashSet();
    Set<Integer> inProgress = new HashSet();
    List<Integer> order = new ArrayList();

    for (int course = 0; course < numCourses; course++) {
        if (!dfs(course, graph, visited, inProgress, order)) {
            return new ArrayList<>();
        }
    }
    return order;
    }

    private boolean dfs(int course, Map<Integer, List<Integer>> graph, 
                    Set<Integer> visited, Set<Integer> inProgress, 
                    List<Integer> order) {
        if (inProgress.contains(course)) {
            return false; // 사이클 발견
        }
        if (visited.contains(course)) {
            return true; // 이미 방문한 노드는 다시 방문하지 않음
        }

        inProgress.add(course); // 현재 탐색 중인 노드 -> 현재 노드가 사이클을 가지는지 확인 가능
        for (int prereq : graph.getOrDefault(course, new ArrayList<>())) {
            if (!dfs(prereq, graph, visited, inProgress, order)) {
                return false;
            }
        }
        inProgress.remove(course); // 탐색 종료 후 current 노드 제거 -> 해당 노드는 사이클이 없다고 할 수 있다
        visited.add(course); // 탐색 완료된 노드
        order.add(course); // 완료된 노드는 결과 리스트에 추가

    return true;
}
```