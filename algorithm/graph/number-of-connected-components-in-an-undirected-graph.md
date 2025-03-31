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