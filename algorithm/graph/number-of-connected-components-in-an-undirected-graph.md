# Number of Connected Components in an Undirected Graph

https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/

- TC: O(V + E)
- SC: O(V + E)

```java
   public int countComponents(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList();
        Set<Integer> visited = new HashSet();

        for (int i = 0; i < n; i++) {
            adj.add(new ArrayList());
        }

        for (int[] e : edges) {
            adj.get(e[0]).add(e[1]);
            adj.get(e[1]).add(e[0]);
        }

        int count = 0;
        for (int i = 0; i < n; i++) {
            if (!visited.contains(i)) {
                dfs(i, adj, visited);
                count++;
            }
        }
        return count;
    }

    /**
        0 - 1 - 2 - 3 
        4 - 5

        visited 0 1 2 3
    */
    public void dfs(int node, List<List<Integer>> adj, Set<Integer> visited) {
        if (visited.contains(node)) {
            return;
        }

        visited.add(node);
        for (int nei : adj.get(node)) {
            dfs(nei, adj, visited);
        }
    }

```

# SOLUTION 02: Disjoint Set Union
- TC: O(V + (E + aV))
- SC: O(V)

```java
    public int countComponents(int n, int[][] edges) {
        DSU dsu = new DSU(n);
        int res = n;
        for (int[] edge : edges) {
            // edge 간 비교를 한다. 합칠수 있다면 두 노드간 서로 그룹이 된다
            if (dsu.union(edge[0], edge[1])) {
                res--;
            }
        }
        return res;
    }

    class DSU {
        int[] parent;
        int[] groupSize;

        public DSU(int n) {
            parent = new int[n];
            groupSize = new int[n];
            for (int i = 0; i < n; i++) {
                parent[i] = i;
                groupSize[i] = i;
            }
        }

        /**
        res = 6
            0 - 1 - 2 - 3
            4 - 5
        [0, 1, 2, 3, 4, 5]
         0. 0. 0. 0. 4. 5
         
        [3, 1, 1, 1, 1, 1]
        */
        public boolean union(int u, int v) {
            int pu = find(u); // u의 부모 노드
            int pv = find(v); // v의 부모 노드

            if (pu == pv) return false; // 부모가 같으면 같은 그룹이므로 union 할 필요가 없다
            if (groupSize[pv] > groupSize[pu]) {
                int temp = pu;
                pu = pv;
                pv = temp;
            }
            parent[pv] = pu; // pv의 parent는 pu가 된다
            groupSize[pu] += groupSize[pv]; // pu 그룹의 크기가 pv의 그룹만큼을 흡수한다
            return true;
        };

        private int find(int node) {
            if (parent[node] != node) {
                parent[node] = find(parent[node]);
            }
            return parent[node];
        };
    }
```