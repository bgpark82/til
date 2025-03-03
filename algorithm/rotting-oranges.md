# Rotting Fruit

https://leetcode.com/problems/rotting-oranges/

# SOLUTION 01: Breath First Search
- Time Complexity: O(m * n)
- Space Complexity: O(m * n)
```java
public int orangesRotting(int[][] grid) {
        // 오렌지가 모두 상해야 몇분 걸렸는지 유효하다
        // 즉, 오렌지의 개수를 알고 있어야 한다.
        // time만으로는 주변에 부패되지 않은 오렌지 확인이 어렵다
        int fresh = 0;
        int minutes = 0;
        Queue<int[]> queue = new LinkedList();
        int[] dx = new int[] {1, -1, 0, 0};
        int[] dy = new int[] {0, 0, 1, -1};
        for (int r = 0; r < grid.length; r++) {
            for (int c = 0; c < grid[0].length; c++) {
                if (grid[r][c] == 1) {
                    fresh++;
                }
                if (grid[r][c] == 2) {
                    queue.offer(new int[] {r, c});
                }
            }
        }

        // 마지막 오렌지가 썩었음에도 queue에 입력되므로 fresh > 0 조건을 추가해야 한다
        while (fresh > 0 && !queue.isEmpty()) {
            // queue 사이즈만큼만 한번에 제거되어야 한다. 그게 time의 의미이기 때문
            int level = queue.size();

            for (int i = 0; i < level; i++) {
                int[] cur = queue.poll();

                for (int d = 0; d < 4; d++) {
                    int y = cur[0] + dy[d];
                    int x = cur[1] + dx[d];

                    if (y < 0 || x < 0 || y >= grid.length || x >= grid[0].length || grid[y][x] == 2 || grid[y][x] == 0) continue;

                    // 이미 마지막 오렌지가 썩었음에도 불구하고 여전히 queue에 넣고 있다
                    grid[y][x] = 2;
                    fresh--; // fresh orange 개수 줄임
                    queue.offer(new int[] {y, x});
                }
            }
            minutes++;
        }

        return fresh == 0 ? minutes : -1;
    }
```
매 루프마다 queue에는 썩은 오렌지 근처의 신선한 오렌지가 썩은 상태로 들어가게 된다
queue에 담긴 오렌지는 모두 같은 시간(같은 레벨의)에 썩은 오렌지이다. 

queue에 담을 때 주의할 점은 마지막에 썩은 오렌지이다.
마지막에 썩은 오렌지는 만약 신선한 오렌지가 없다면 더 이상 주변을 썩힐 수 없다. 
그러므로 queue에 들어가면 불필요한 연산을 하게 된다
그러므로 fresh > 0 조건을 추가해야 한다.

