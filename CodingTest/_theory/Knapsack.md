---
title: Knapsack Algorithm
aliases: [knapsack, 배낭문제, 0-1 knapsack, fractional knapsack, 냅색]
type: concept
status: budding
created: 2026-05-23
updated: 2026-05-24
tags: [cs/algorithm, codingtest, status/budding, DP, 그리디]
notion-url: https://www.notion.so/Knapsack-Algorithm-11f35c502383808d9a53d3cee46034a0
related:
  - "[[_MOC]]"
  - "[[Dynamic-Programming]]"
  - "[[그리디]]"
source: ["Notion: 코딩 테스트 알고리즘 이론"]
migrated-from: "Notion: Knapsack Algorithm"
---

# 🕢 Knapsack Algorithm

> TL;DR: 무게 제한 배낭에 가치 합 최대화. **0/1 Knapsack (DP, O(nW))** — 물건 쪼갤 수 없음. **Fractional Knapsack (Greedy, O(n log n))** — 물건 쪼갤 수 있음.

---

# 1. 정의

배낭 문제(Knapsack Problem)는 무게 제한 W인 배낭에 n개 물건(무게 wᵢ, 가치 vᵢ)을 담아 **총 가치를 최대화**하는 문제다.

## 두 가지 변형

| 종류 | 물건 분할 | 알고리즘 | 복잡도 |
|------|----------|---------|--------|
| **0/1 Knapsack** | ❌ 못 쪼갬 | **동적 프로그래밍** | **O(n×W)** |
| **Fractional Knapsack** | ✅ 쪼갤 수 있음 | **그리디** (가치/무게 비율 순) | O(n log n) |

코딩 테스트에서 "배낭 문제" = 대부분 **0/1 Knapsack (DP)**.

---

# 2. 0/1 Knapsack — 핵심 아이디어 (DP)

**V[i][j]**: 처음 i개 물건만 고려하고, 무게 제한이 j일 때 달성 가능한 최대 가치

**점화식:**

```
초기: V[0][j] = 0 (물건 없음)

if w_i > j:     V[i][j] = V[i-1][j]         (i번째 물건 못 넣음)
else:           V[i][j] = max(
                    V[i-1][j],               // i번째 물건 안 넣는 경우
                    V[i-1][j - w_i] + v_i    // i번째 물건 넣는 경우
                )
```

**최적 해**: V[n][W]

---

# 3. 의사코드

```plaintext
function Knapsack(v[1..n], w[1..n], W):
    for j = 0 to W:
        V[0][j] = 0          // 물건 없으면 가치 0

    for i = 1 to n:          // 각 물건
        for j = 0 to W:      // 각 무게 제한
            if w[i] > j:
                V[i][j] = V[i-1][j]
            else:
                V[i][j] = max(V[i-1][j], V[i-1][j - w[i]] + v[i])

    return V[n][W]
```

---

# 4. 자바스크립트 구현

```javascript
function knapsack01(values, weights, W) {
    const n = values.length;
    // V[i][j]: 처음 i개 물건, 무게 제한 j일 때 최대 가치
    const V = Array.from({ length: n + 1 }, () => new Array(W + 1).fill(0));

    for (let i = 1; i <= n; i++) {
        const wi = weights[i - 1];
        const vi = values[i - 1];
        for (let j = 0; j <= W; j++) {
            if (wi > j) {
                V[i][j] = V[i - 1][j];
            } else {
                V[i][j] = Math.max(V[i - 1][j], V[i - 1][j - wi] + vi);
            }
        }
    }

    return V[n][W];
}

// 1D 배열로 공간 최적화 (O(W))
function knapsack01Optimized(values, weights, W) {
    const dp = new Array(W + 1).fill(0);

    for (let i = 0; i < values.length; i++) {
        // 역방향으로 순회 — 같은 물건 두 번 선택 방지
        for (let j = W; j >= weights[i]; j--) {
            dp[j] = Math.max(dp[j], dp[j - weights[i]] + values[i]);
        }
    }

    return dp[W];
}

// 사용 예시
const values  = [60, 100, 120];
const weights = [10, 20,  30];
const W = 50;

console.log(knapsack01(values, weights, W));          // 220
console.log(knapsack01Optimized(values, weights, W)); // 220
// → 무게 20+30=50, 가치 100+120=220
```

---

# 5. Fractional Knapsack (그리디)

물건을 쪼갤 수 있다면 **가치/무게 비율** 높은 순으로 선택.

```javascript
function fractionalKnapsack(values, weights, W) {
    const items = values.map((v, i) => ({ v, w: weights[i], ratio: v / weights[i] }));
    items.sort((a, b) => b.ratio - a.ratio); // 비율 내림차순

    let totalValue = 0;
    let remaining = W;

    for (const item of items) {
        if (remaining <= 0) break;
        const take = Math.min(item.w, remaining);
        totalValue += take * item.ratio;
        remaining -= take;
    }

    return totalValue;
}
```

---

# 6. 복잡도 비교

| 방식 | 시간 복잡도 | 공간 복잡도 | 물건 분할 |
|------|-----------|-----------|---------|
| **재귀 브루트포스** | O(2ⁿ) | O(n) | ❌ |
| **0/1 DP (2D)** | **O(n×W)** | O(n×W) | ❌ |
| **0/1 DP (1D 최적화)** | O(n×W) | **O(W)** | ❌ |
| **Fractional Greedy** | O(n log n) | O(n) | ✅ |

**주의**: W가 매우 크면 DP가 비효율적 (Pseudo-polynomial). 이 경우 분기한정법이나 근사 알고리즘 고려.

---

## Related
- [[_MOC]]
- [[Dynamic-Programming]] — 0/1 Knapsack은 DP의 대표 문제
- [[그리디]] — Fractional Knapsack은 그리디 전략

## Sources
- [Notion 원본](https://www.notion.so/Knapsack-Algorithm-11f35c502383808d9a53d3cee46034a0)
