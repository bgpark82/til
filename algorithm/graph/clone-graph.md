# Clone Graph

https://leetcode.com/problems/clone-graph/description/
- TC: O(V + E)
- SC: O(V) 최악의 경우 모든 node가 스택 메모리에 쌓인다
```java
/**
    undirected graph
    1 -> 2
    2 -> 1, 3
    3 -> 2
    
    curr = new Node(1)
    list nei = graph(1).nei
*/
class Solution {
    public Node cloneGraph(Node node) {
        Map<Node, Node> oldToNew = new HashMap();
        return dfs(node, oldToNew);
    }

    // node(1)
    //      node(2)
    //          node(1)
    //
    // 1:1
    // 2:2
    // 문제는 이미 한번 방문했다면 더 이상 depth를 늘리면 안된다
    // val은 필요가 없다. node가 있기 때문에
    private Node dfs(Node node, Map<Node, Node> oldToNew) {
        if (node == null) {
            return null; // neighbors에 null이 추가되도 된다
        }

        if (oldToNew.containsKey(node)) {
            return oldToNew.get(node);
        }
        
        Node copy = new Node(node.val);
        oldToNew.put(node, copy); // 첫방문이라면 old에 new를 매핑해놓는다. 나중에 또 방문하면 new만 반환하면 된다
        
        for (Node next : node.neighbors) {
            copy.neighbors.add(dfs(next, oldToNew));
        }

        return copy;
    }
}
```
시간복잡도가 O(V + E)인 이유
- DFS에서 만약 A가 B,C 방문하는 경우
- A 노드를 방문할 때, 메모리에 스택이 쌓이면서 O(1)이 된다
- 해당 스택 안에서, A노드의 인접 노드들이 for loop을 돌면서 O(N)의 시간복잡도가 소요된다
- 근데 O(V * E)가 아닌 이후는, 방문한 노드는 다시 방문하지 않는다. 즉, 해당 노드로 간선이 뻗어나갈 필요가 없다
- 