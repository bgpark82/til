# Valid Sudoku

https://leetcode.com/problems/valid-sudoku/description/

# SOLUTION 01: Brute Force
- Time Complexity: O(n^2)
- Space Complexity: O(n^2)
```java
// row 확인
        for (int r = 0; r < board.length; r++) {
            Set<Character> set = new HashSet();
            for (int c = 0; c < board[0].length; c++) {
                char ch = board[r][c];
                if (ch == '.') continue;
                if (set.contains(ch)) {
                    return false;
                }
                set.add(ch);
            }
        }

        // column 확인
        for (int c = 0; c < board[0].length; c++) {
            Set<Character> set = new HashSet();
            for (int r = 0; r < board.length; r++) {
                char ch = board[r][c];
                if (ch == '.') continue;
                if (set.contains(ch)) {
                    return false;
                }
                set.add(ch);
            }   
        }

        // 3 x 3
        for (int sqr = 0; sqr < 9; sqr++) {
            Set<Character> set = new HashSet();
            for (int r = 0; r < 3; r++) {
                for (int c = 0; c < 3; c++) {
                    // sqr=0 : 0,0 -> 2,2
                    // sqr=1 : 0,3 -> 2,5
                    // sqr=2 : 0,6 -> 2,8
                    // sqr=3 : 3,0 -> 5,2
                    // sqr=4 : 3,3 -> 5,5
                    // sqr=5 : 3,6 -> 5,8
                    // sqr=6 : 6,0 -> 8,2
                    // sqr=7 : 6,3 -> 8,5
                    // sqr=6 : 6,6 -> 8,8
                    char ch = board[r + ((sqr % 3) * 3)][c + ((sqr / 3) * 3)];
                    if (ch == '.') continue;
                    if (set.contains(ch)) {
                        return false;
                    }
                    set.add(ch);
                }
            }
        }
        return true;
```
각 열과 행, 그리고 3x3 영역을 확인하여 중복된 숫자가 있는지 확인
문제는 매번 HashSet을 생성하는 것은 가비지 컬렉션 대상을 매번 생성하는 격이라 비효율적임

# SOLUTION 02: HashSet
- Time complexity: O(n^2)
- Space complexity: O(n^2)
```java
// row, column, square 저장할 공간을 미리 할당
        // [set, set, set ..] idx = row
        Map<Integer, Set<Character>> rows = new HashMap();
        // [set, set, set ..] idx = col
        Map<Integer, Set<Character>> cols = new HashMap();
        // [set, set, set ..] idx = square
        // 00 01 02 10 11 12 20 21 22 -> square 0 -> 00
        // 03 04 05 13 14 15 23 24 25 -> square 1 -> 01
        // 06 07 08 16 17 18 26 27 28 -> square 2 -> 02
        // 30 31 32 40 41 42 50 51 52 -> square 3 -> 10
        Map<String, Set<Character>> squares = new HashMap();
        // 굳이 영역 대표값을 숫자로 표현할 필요는 없음

        for (int r = 0; r < board.length; r++) {
            for (int c = 0; c < board[0].length; c++) {
                rows.put(r, new HashSet());
                cols.put(c, new HashSet());
                squares.put(r/3 + "," + c/3, new HashSet());
            }
        }

        for (int r = 0; r < board.length; r++) {
            for (int c = 0; c < board[0].length; c++) {
                if (board[r][c] == '.') continue;

                // row, column, sqaure 한꺼번에 계산
                if (rows.get(r).contains(board[r][c]) || 
                cols.get(c).contains(board[r][c]) || 
                squares.get(r/3 + "," + c/3).contains(board[r][c])) {
                    return false;
                }
                // row, column, square에 값 추가
                rows.get(r).add(board[r][c]);
                cols.get(c).add(board[r][c]);
                squares.get(r/3 + "," + c/3).add(board[r][c]); 
            }
        }
        return true;
```
3x3 영역을 "row,column" 형식으로 표현하여 중복 확인
원래는 square 영역을 숫자로 표현하려고 했으나 사실 문자로 하는게 더 쉬운 방법인 것 같다

# SOLUTION 03: HashSet 최적화
- Time complexity: O(n^2)
- Space complexity: O(n^2)
```java
Map<Integer, Set<Character>> rows = new HashMap();
        Map<Integer, Set<Character>> cols = new HashMap();
        Map<String, Set<Character>> squares = new HashMap();

        for (int r = 0; r < board.length; r++) {
            for (int c = 0; c < board[0].length; c++) {
                if (board[r][c] == '.') continue;

                if (rows.computeIfAbsent(r, key -> new HashSet()).contains(board[r][c]) ||
                    cols.computeIfAbsent(c, key -> new HashSet()).contains(board[r][c]) ||
                    squares.computeIfAbsent(r/3 + "," + c/3, key -> new HashSet()).contains(board[r][c])
                ) {
                    return false;
                }

                rows.get(r).add(board[r][c]);
                cols.get(c).add(board[r][c]);
                squares.get(r/3 + "," + c/3).add(board[r][c]);
            }
        }
        return true;
```
위와 같은 코드이지만 `computeIfAbsent` 메서드를 사용하여 가독성을 늘렸다
`computeIfAbsent` 메서드는 키가 존재하지 않으면 두번째 인자를 실행하고 반환값을 맵에 저장하고 반환한다
키가 존재하면 해당 키의 값을 반환한다

# SOLUTION 04: Bitmask
- Time complexity: O(n^2)
- Space complexity: O(n)
```java
        // rows의 경우, 해당 숫자의 배열을 비트로 표현 가능
        // rows : [1 2 . . 3 . . . .] -> [.....321.] -> [000001110]
        // 비교하려는게 4라면 1을 왼쪽으로 4번 밀면 된다  -> 0000010000
        // 단순하게 4라는 숫자의 자리에 1이 있는지 없는지 확인만 하면된다 -> [000001110] & [0000010000]
        // 만약 존재하면 1을 반환하고 아니면 0을 반환한다. 즉, 1이면 이미 존재하니 valid한 스도쿠가 아니다
        // 참고: 해당 바이트코드를 10진수로 바꾸면 14와 16이다 (중요한건 아니다)
        int[] rows = new int[9];
        int[] cols = new int[9];
        int[] squares = new int[9];

        for (int r = 0; r < board.length; r++) {
            for (int c = 0; c < board[0].length; c++) {
                if (board[r][c] == '.') continue;
                // 0부터 시작
                int val = board[r][c] - 1;

                if ((rows[r] & (1 << val)) > 0 ||
                    (cols[c] & (1 << val)) > 0 ||
                    // 00 ~ 22 -> 0
                    // 03 ~ 25 -> 1
                    // 06 ~ 28 -> 2
                    // 30 ~ 32 -> 3 + 0 = 3
                    // 33 ~ 35 -> 3 + 1 = 4 
                    // 36 ~ 35 -> 3 + 2 = 5
                    (squares[((r/3) * 3 + (c/3))] & (1 << val)) > 0
                ) { 
                    return false;
                }

                rows[r] |= (1 << val);
                cols[c] |= (1 << val);
                squares[((r/3) * 3 + (c/3))] |= (1 << val);
            }
        }
        return true;
```
비트마스크를 사용하면 중복확인을 더 빠르게 할 수 있다
**Set으로 중복여부를 확인**한다면 bitmask로 **공간복잡도를 줄여**버릴 수 있다

또한 3x3 영역을 표시할 때, row는 줄이 바뀔 때마다 3씩 증가한다.
반면에 column은 row가 바뀔 때마다 0으로 리셋된다