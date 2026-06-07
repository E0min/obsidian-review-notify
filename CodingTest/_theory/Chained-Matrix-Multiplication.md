---
title: Chained Matrix Multiplication
aliases: [matrix chain multiplication, 행렬 곱 순서, MCM, 연쇄행렬곱셈]
type: concept
status: budding
created: 2026-05-23
updated: 2026-05-24
tags: [cs/algorithm, codingtest, status/budding, DP]
notion-url: https://www.notion.so/Chained-Matrix-Multiplation-11f35c50238380c2955fe6b981e81463
related:
  - "[[_MOC]]"
  - "[[Dynamic-Programming]]"
  - "[[분할-정복]]"
source: ["Notion: 코딩 테스트 알고리즘 이론"]
migrated-from: "Notion: Chained Matrix Multiplication"
---

# 🎣 Chained Matrix Multiplication

> TL;DR: n개 행렬 곱셈 순서 최적화. **결합법칙**으로 결과는 같지만 연산 횟수가 달라짐. DP 점화식으로 최소 연산 순서 탐색. **O(n³)**.

---

# 1. 정의

연쇄 행렬 곱셈(Chained Matrix Multiplication, MCM)은 여러 행렬을 곱할 때 **최소 연산 횟수**가 되는 **괄호 묶기 순서**를 찾는 문제다.

- 행렬 곱셈: 교환법칙 ❌, **결합법칙** ✅
- 순서에 따라 연산 횟수가 천차만별

## 직관적 예시

A1 (10×100), A2 (100×5), A3 (5×50)

| 순서 | 계산 | 연산 횟수 |
|------|------|---------|
| **(A1×A2)×A3** | 10×100×5 + 10×5×50 | **7,500** ✅ |
| A1×(A2×A3) | 100×5×50 + 10×100×50 | 75,000 ❌ |

같은 결과, 10배 차이 — 순서가 핵심이다.

---

# 2. 핵심 아이디어 (DP 3단계)

## 1단계: 구조 정의 (Structure)

n개 행렬 A₁, A₂, ..., Aₙ에서 Aᵢ의 차원은 **P_{i-1} × P_i**.
행렬 Aᵢ부터 Aⱼ까지의 최소 곱셈 횟수를 **m[i, j]**로 정의.

## 2단계: 최적성 원리 (Principle of Optimality)

```
m[i, j] = 0                                        (i = j)
m[i, j] = min{ m[i, k] + m[k+1, j] + P_{i-1}×P_k×P_j }   (i < j, i ≤ k < j)
```

- 분할 지점 k에서 두 부분으로 나눔
- 양쪽 각각의 최솟값 + 두 결과 행렬 곱하는 비용

## 3단계: 하향식 계산 (Bottom-Up)

- 길이 L=1 (단일): m[i,i] = 0
- 길이 L=2, 3, ..., n 순으로 테이블 채우기

---

# 3. 의사코드

```plaintext
function chainMatrix(p[0..n]):
    m[1..n][1..n] = new table

    for i = 1 to n:
        m[i][i] = 0

    for L = 2 to n:             // 연쇄 길이
        for i = 1 to n-L+1:    // 시작 행렬
            j = i + L - 1      // 끝 행렬
            m[i][j] = Infinity
            for k = i to j-1:  // 분할 지점
                q = m[i][k] + m[k+1][j] + p[i-1]*p[k]*p[j]
                if q < m[i][j]:
                    m[i][j] = q

    return m[1][n]
```

---

# 4. 자바스크립트 구현

```javascript
function chainMatrixMultiplication(p) {
    const n = p.length - 1; // 행렬 개수
    // m[i][j]: Aᵢ~Aⱼ 곱하는 최소 연산 횟수 (1-indexed)
    const m = Array.from({ length: n + 1 }, () => new Array(n + 1).fill(0));

    for (let L = 2; L <= n; L++) {           // 연쇄 길이
        for (let i = 1; i <= n - L + 1; i++) { // 시작 인덱스
            const j = i + L - 1;             // 끝 인덱스
            m[i][j] = Infinity;
            for (let k = i; k < j; k++) {   // 분할 지점
                const q = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j];
                if (q < m[i][j]) {
                    m[i][j] = q;
                }
            }
        }
    }

    return m[1][n]; // A₁~Aₙ 전체의 최소 연산 횟수
}

// 예시: A1(10×100), A2(100×5), A3(5×50)
// p = [10, 100, 5, 50] → p[0]=10(A1의 행), p[1]=100(A1의 열=A2의 행), ...
const p = [10, 100, 5, 50];
console.log(chainMatrixMultiplication(p)); // 7500
```

---

# 5. 계산 과정 예시

p = [10, 100, 5, 50] → 행렬 A1(10×100), A2(100×5), A3(5×50)

**L = 2:**
- m[1][2] = 10 × 100 × 5 = **5,000**
- m[2][3] = 100 × 5 × 50 = **25,000**

**L = 3:**
- m[1][3]: k=1 → m[1][1]+m[2][3]+10×100×50 = 0+25000+50000 = 75,000
- m[1][3]: k=2 → m[1][2]+m[3][3]+10×5×50 = 5000+0+2500 = **7,500** ✅

`m[1][3] = 7,500` — **(A1×A2)×A3** 순이 최적

---

# 6. 복잡도

| 항목 | 내용 |
|------|------|
| **시간 복잡도** | **O(n³)** — 3중 루프 (L, i, k) |
| **공간 복잡도** | O(n²) — m 테이블 |
| **재귀 (브루트포스)** | O(2ⁿ) — 모든 괄호 경우의 수 |

---

## Related
- [[_MOC]]
- [[Dynamic-Programming]] — MCM은 DP의 교과서적 예제
- [[분할-정복]] — 분할 방식은 유사하나 MCM은 중복 부분 문제 존재 → DP

## Sources
- [Notion 원본](https://www.notion.so/Chained-Matrix-Multiplation-11f35c50238380c2955fe6b981e81463)
