# Island and Treasure
https://neetcode.io/problems/islands-and-treasure
- TC: O(m * n * 4^(m * n))
- SC: O(m * n)

```java
    
// SOLUTION 1: BackTracking
// - INF 노드를 시작으로 계속 탐색해나간다
// - INF 노드로 돌아왔을 때 최대 거리를 저장한다
// - 방문했던 노드들은 백트래킹으로 모두 방문 초기화한다
// - 그리고 다음 칸의 INF 노드를 탐색한다
// - 즉, 노드 하나하나마다 계산해야 하므로 Brute Force에 가깝다
// - 시간 복잡도는 O(m * n * 4^(m * n)) : 2중 for문 * 노드별 4방향
int[] dx = new int[] {1, -1, 0, 0};
int[] dy = new int[] {0, 0, -1, 1};
boolean[][] visited;

// 문제는 반대편에 0이 있으면 어쩔껀데?
// 그래서 0부터 시작하면 안되 INF에서 0으로 가면서 개수를 하나씩 늘려야 한다??
public void islandsAndTreasure(int[][] grid) {
    visited = new boolean[grid.length][grid[0].length];

    for (int i = 0; i < grid.length; i++) {
        for (int j = 0; j < grid[0].length; j++) {
            if (grid[i][j] == Integer.MAX_VALUE) {
                grid[i][j] = dfs(grid, i, j);
            }
        }
    }
}

private int dfs(int[][] grid, int y, int x) {
    if (y < 0 || x < 0 || y >= grid.length || x >= grid[0].length ||  grid[y][x] == -1 || visited[y][x]) return Integer.MAX_VALUE;
    if (grid[y][x] == 0) return 0;
    visited[y][x] = true;
    
    int count = Integer.MAX_VALUE;
    for (int i = 0; i < 4; i++) {
        int cy = y + dy[i];
        int cx = x + dx[i];

        int res = dfs(grid, cy, cx);
        if (res != Integer.MAX_VALUE) {
            count = Math.min(count, 1 + res);
        }
    }

    visited[y][x] = false;
    return count;
}

```
- 그래프에서는 사실 백트래킹 Brute Force에 가깝다 생각한다
    - 왜냐하면 하나의 노드의 상태를 바꾸기 위해 모든 노드들을 방문하고 방문 취소하기 때문이다
    - 이 방법은 시간복잡도가 정말 크다
- 그래프에서는 방문 여부가 중요하다
    - 방문을 이미 했으면 방문하지 않도록 처리해야 한다
