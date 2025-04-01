# Disjoint Set Union

용어
- Disjoin Set: 서로소 집합, 서로 겹치지 않는 집합 = 서로소 집합
- Union: 합치기

정의
- 각 노드를 집합으로 묶어서 같은 그룹인지 파악하는 방법

왜
- 사이클을 찾을 때
- 모두 한 그룹인지 확인

예시
1. 그룹 만들기
    - 반에 10명이 있다
    - 처음에는 개인이 따로 있는 상태
    - 각 개인이 자기 자신 그룹의 리더
2. 친구 사귀기 (Union)
    - 서로 친해지면서 그룹 만들기
    - 만약 1번과 2번이 친구가되면 같은 그룹이 된다
    - 이때 한명이 리더가 된다
3. 같은 그룹 확인  (Find)
    - 다른 친구도 같은 그룹인지 확인
    - 리더가 같은지 확인한다
    - 만약 두 친구의 리더가 같은 사람이라면 같은 그룹
    - 리더가 다르면 다른 그룹이니 연결 가능
4. 최적화
    - 친구를 만날 때마다 각 그룹의 리더가 누구인지 탐색하게 된다
    - 시간이 많이 걸리니 리더가 누구인지 바로 대답하도록 만듦

어떻게
1. 그룹 만들기
2. Union (합치기)
3. Find (그룹 확인)
4. Compression (경로 최적화)


예시
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

    public DSU (int n) {
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
        return Parent[node]; // 그룹의 최종 리더를 반환
    }

    public boolean union(int u, int v) {
        int pu = find(u), pv = find(v); // 각각의 리더를 조회한다
        if (pu == pv) return false; // 리더가 같으면 합칠 필요없다. 이미 같은 그룹
        // 합쳐야 되는 경우
        if (Size[pu] < Size[pv]) { // 사이즈가 작은 그룹을 큰 그룹에 병합하는게 더 좋다. pv를 작은 그룹으로 만들기 위함
            int temp = pu;
            pu = pv;
            pv = temp;
        }
        Parent[pv] = pu; // pv의 부모가 pu가 됨
        Size[pu] += Size[pv]; // pv 그룹이 pu 그룹에 병합되어 그만큼 사이즈가 커짐
        return true; // 합치면 true
    }

    public int components() {
        return comps;
    }
}
```