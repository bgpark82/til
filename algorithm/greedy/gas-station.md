# Gas station

https://neetcode.io/problems/gas-station

```java
public int canCompleteCircuit(int[] gas, int[] cost) {
        int n = gas.length;

        for (int i = 0; i < n; i++) {
            int tank = gas[i] - cost[i];
            if (tank < 0) continue;

            int j = (i + 1) % n;
            while (j != i) {
                tank += gas[j];
                tank -= cost[j];
                if (tank < 0) break;
                j = (j + 1) % n;
            }
            if (j == i) return i;
        }
        return -1;
    }
```