# Course Schedule 2

## SOLUTION 01: DFS
```java
class Solution {
    /**
        0 -> 1 
        근데 왜 0,1,2가 나오지?
        아마 순서가 없으면 그냥 list에 채워넣어도 괜찮다 왜냐하면 정답은 여러개가 될 수 있기 때문이다
        1
        visited: 0 1
        visited을 돌면서 안채워진 것 채우기

        0 -> 1 -> 2 -> 0 : if cycle happen, it's not valid

    */
    public int[] findOrder(int numCourses, int[][] prerequisites) {
        Set<Integer> visited = new HashSet();
        Set<Integer> cycle = new HashSet();
        List<List<Integer>> adj = new ArrayList();
        List<Integer> ans = new ArrayList();

        for (int i = 0; i < numCourses; i++) {
            adj.add(new ArrayList());
        }

        for (int[] pre : prerequisites) {
            adj.get(pre[0]).add(pre[1]);
        }

        for (int course = 0; course < numCourses; course++) {
            if (!dfs(adj, visited, cycle, course, ans)) return new int[0];
        }

        for (int i = 0; i < numCourses; i++) {
            if (!visited.contains(i)) {
                ans.add(i);
            }
        }

        int[] res = new int[ans.size()];
        for (int i = 0; i < ans.size(); i++) {
            res[i] = ans.get(i);
        }

        return res;
    }

    private boolean dfs(List<List<Integer>> adj, Set<Integer> visited, Set<Integer> cycle, int cur, List<Integer> ans) {
        if (cycle.contains(cur)) return false; // 현재 노드에서 사이클이 있다면 탈출
        if (visited.contains(cur)) return true; // 현재 노드에서 이미 방문했다면 무시

        cycle.add(cur);
        for (int nei: adj.get(cur)) {
            if(!dfs(adj, visited, cycle, nei, ans)) return false;
        }
        cycle.remove(cur); // 사이클이 없다면 제거
        visited.add(cur);
        ans.add(cur);

        return true;
    }
}
```
DFS이지만 결국 Topology sort (위상정렬)
- cycle을 탐색하는 로직이고, 
    - cycle에서 현재 노드가 갈 수 있는 만큼 dfs 탐색을 한다.
    - cycle은 현재 노드가 cycle을 가지는지 확인하는 단계이다
    - cycle에 현재 노드를 추가하고 연관된 노드들을 방문하면서 자신의 노드를 만난다면 사이클이 만들어진다
- visited은 탐색이 끝나서 방문할 필요가 없는 노드이다
    - visited은 탐색이 다 끝나고, 즉 해당 노드가 사이클이 있는지 다 확인하고 마지막으로 방문했다고 표시한다
    - visited에 있다면 이미 해당 노드는 탐색이 끝났으므로 방문할 가치가 없다

# SOLUTION 02: Topology sort (Kahn's Algorithm)
```java
public int[] findOrder(int numCourses, int[][] prerequisites) {
        // 각 노드의 전입차수 계산 (indegree)
        int[] indegree = new int[numCourses];
        List<List<Integer>> adj = new ArrayList();
        for (int i = 0; i < numCourses; i++) {
            adj.add(new ArrayList());
        }
        for (int[] pre : prerequisites) {
            indegree[pre[1]]++;
            adj.get(pre[0]).add(pre[1]);
        }
        Queue<Integer> q = new LinkedList();
        for (int i = 0; i < numCourses; i++) {
            if (indegree[i] == 0) {
                q.offer(i); 
            }
        }

        // 전입차수가 0인 노드를 먼저 방문한다. 즉, 가장 마지막에 듣는 강의가 가장 먼저들어가게 된다
        // 그것을 방지하기 위해 가장 먼저 방문하는 노드는 결과 배열의 가장 마지막에 넣어버린다
        int finish = 0;
        int[] output = new int[numCourses];
        while (!q.isEmpty()) {
            int cur = q.poll();
            // output은 방문한 순서
            output[numCourses - finish - 1] = cur;
            finish++;
            for (int nei : adj.get(cur)) {
                // 현재 노드에서 주변 노드로 방문하면서 주변 노드는 indegree하나를 일음
                indegree[nei]--;
                if (indegree[nei] == 0) {
                    q.add(nei);
                }
            }
        }

        if (finish != numCourses) return new int[0];
        return output;
    }
```
- 전입차수를 이용한 topology sort
    - 전입차수가 가장 낮은 노드를 먼저 방문한다
    - 즉, 가장 마지막에 들어야할 과목을 먼저 듣는다
    - 가장 마지막에 듣는 과목부터 반대로 탐색해 나간다
    - 결과 배열은 처음 방문하는 과목이 가장 마지막이여야 하므로 numCourses - finish - 1에 대상 노드를 넣어야 한다
    - numCourse 개수와 finish 개수가 다르면 완전한 그래프가 아니므로 전체 수강한게 아니다