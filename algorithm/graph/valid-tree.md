# Valid Tree

https://neetcode.io/problems/valid-tree


## 1. DFS
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

## BFS
- TC : O(V + E)
- SC : O(V + E)
```java
public boolean validTree(int n, int[][] edges) {

        Set<Integer> visited = new HashSet();
        List<List<Integer>> adj = new ArrayList();

        for (int i = 0; i < n; i++) {
            adj.add(new ArrayList());
        }
        for (int[] nei : edges) {
            adj.get(nei[0]).add(nei[1]);
            adj.get(nei[1]).add(nei[0]);
        }

        Queue<int[]> q = new LinkedList();
        q.offer(new int[] {0, -1});
        while (!q.isEmpty()) {
            int[] node = q.poll();
            int curr = node[0], parent = node[1];

            if (visited.contains(curr)) {
                System.out.println("cycle detected!");
                return false;
            }

            visited.add(curr);
            for (int nei : adj.get(curr)) {
                // 방금 전 방문한 노드는 다시 방문할 필요가 없다
                if (nei == parent) continue;
                
                q.offer(new int[] {nei, curr});
            }
        }

        return visited.size() == n;
    }
```
- DFS와 동일하다
    - 결국 이전에 방문한 노드라면 스킵
    - 이미 방문했다면 false를 반환한다

## 3. Disjoint Set Union
```java
public boolean validTree(int n, int[][] edges) {
        DSU dsu = new DSU(n);
        for (int[] edge: edges) {
            if (!dsu.union(edge[0], edge[1])) { // 이미 같은 그룹내에 있다면 트리가 아님. 사이클 발생
                return false;
            }
        }
        // 모두 합쳐진 경우, 모든 노드가 연결된 상태, 1 이상이면 노드 그룹 말고 연결안된 노드가 있다는 뜻
        return dsu.components() == 1; 
    }

    class DSU {
        int[] Parent, Size;
        int comps;

        public DSU (int n) {
            comps = n;
            Parent = new int[n + 1];
            Size = new int[n + 1];
            for (int i = 0; i <= n; i++) {
                Parent[i] = i; // 스스로가 그룹의 리더
                Size[i] = 1; // 현재 그룹은 1명
            }
        }

        public int find(int node) {
            if (Parent[node] != node) { // 현재 주어진 친구가 그룹의 리더가 아니면
                Parent[node] = find(Parent[node]); // 리더를 찾아서 저장
            }
            return Parent[node]; // 리더를 반환?
        }

        public boolean union(int u, int v) {
            int pu = find(u), pv = find(v); // 각각의 리더를 조회한다
            if (pu == pv) return false; // 리더가 같으면 합칠 필요없다. 이미 같은 그룹
            // 합쳐야 되는 경우
            if (Size[pu] < Size[pv]) { // 사이즈가 더 큰값과 
                int temp = pu;
                pu = pv;
                pv = temp;
            }
            comps--;
            Size[pu] += Size[pv]; // 사이즈가 같은것에 큰것을 병합. 왜?
            Parent[pv] = pu; // 하나의 부모로 병합
            return true; // 합치면 true
        }

        public int components() {
            return comps;
        }
    }
```