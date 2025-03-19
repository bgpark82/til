# Valid Tree

https://neetcode.io/problems/valid-tree

- TC: O(E + V)
- SC: O(E + V)

```java

    /**
        결국 그래프는 visit을 하냐 안하냐가 중요하다
        사이클 그래프는 결국 한번 visit하게 되어 있다.
    */
    public boolean validTree(int n, int[][] edges) {
        // visited 생성
        List<List<Integer>> adj = new ArrayList();

        // 이중 배열 생성
        for (int i = 0; i < n; i++) {
            adj.add(new ArrayList());
        }
        for (int[] edge : edges) {
            adj.get(edge[0]).add(edge[1]);
            adj.get(edge[1]).add(edge[0]);
        }

        // cycle이 발생하면 무조건 false 반환
        // 문제는 undirect graph는 항상 이전 노드로 방문한다
        // 그래서 prev를 방문하면 무시한다
        Set<Integer> visited = new HashSet();
        if (!dfs(adj, visited, 0, -1)) return false;
        
        return visited.size() == n;
    }

    private boolean dfs(List<List<Integer>> adj, Set<Integer> visited, int curr, int parent) {
        if (visited.contains(curr)) {
            return false;
        }

        /**
            1 <-> 2 -> 3
         parent  curr nei 
        */
        visited.add(curr);
        for (int nei : adj.get(curr)) {
            // cur의 자식들을 방문할텐데, 자식이 이미 부모와 같다면, 즉, 다시 방문한 곳으로 돌아간다면 무시한다
            if (nei == parent) continue;
            // nei을 방문하고 자식들을 찾아볼 예정, 
            if (!dfs(adj, visited, nei, curr)) return false;
        }

        return true;
    }

```
- 그래프에서 cycle이 발생하면 트리가 될 수 없다
    - 문제는 undirect 그래프는 항상 cycle이 발생한다
    - 왜냐하면 바로 이전에 방문한 노드를 반드시 또 방문하기 때문이다
    - 이를 막기 위해 현재 노드와 이전 노드를 상태로 넘겨주고
    - 이전 노드가 현재 노드들에 자식에 포함되어 있다면, 이전 노드는 이미 방문한 노드이므로 무시한다 (방문하지 않는다)
    - 현재 노드의 부모 == 현재 노드의 자식 : 왔던데 되돌아간 격
- 이미 방문한 노드가 실제 노드 개수와 같아야 유효하다
