# Word Letter
https://neetcode.io/problems/word-ladder

- TC: O(ML) 
- SC: O(ML)
```java
    public int ladderLength(String beginWord, String endWord, List<String> wordList) {
        if (!wordList.contains(endWord) || beginWord.equals(endWord)) return 0;

        Set<String> words = new HashSet(wordList); 

        Queue<String> q = new LinkedList();
        q.offer(beginWord);

        int res = 0;
        while (!q.isEmpty()) { // O(m): wordList 길이만큼 반복
            res++;
            int size = q.size(); // 현재 레벨의 단어수

            for (int i = size; i > 0; i--) { 
                String node = q.poll();
                if (node.equals(endWord)) return res;

                for (int j = 0; j < node.length(); j++) { // O(n): 단어 길이만큼 반복
                    for (char c = 'a'; c <= 'z'; c++) {
                        if (c == node.charAt(j)) continue;
                        String nei = node.substring(0, j) + c + node.substring(j + 1);

                        // 유효한 단어이면 큐에 추가하고 중복 방지를 위해 Set에서 제거
                        if (words.contains(nei)) {
                            System.out.println("node=" + node + ", nei=" + nei + ", words=" + words);
                            q.offer(nei);
                            words.remove(nei); // 한 번 사용한 단어는 다시 사용하지 않음
                        }
                    }
                }
            }
        }   
        return 0;
    }  
```