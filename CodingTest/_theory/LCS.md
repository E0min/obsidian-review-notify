---
title: 최장 공통 부분 수열 (LCS)
aliases: [LCS, longest common subsequence, 최장공통부분수열]
type: concept
status: budding
created: 2026-05-23
updated: 2026-05-24
tags: [cs/algorithm, codingtest, status/budding, DP]
notion-url: https://www.notion.so/LCS-11f35c50238380f3bcebf1f8b42fa080
related:
  - "[[_MOC]]"
  - "[[Dynamic-Programming]]"
  - "[[Chained-Matrix-Multiplication]]"
source: ["Notion: 코딩 테스트 알고리즘 이론"]
migrated-from: "Notion: 최장 공통 부분 수열(LCS)"
---

# ♥️ 최장 공통 부분 수열 (LCS)

> TL;DR: 두 문자열에서 공통으로 나타나는 부분 수열 중 가장 긴 것. **2D DP 테이블**로 O(mn). diff, 유사도 측정, 문자열 비교에 핵심 알고리즘.

---

# 1. 정의

LCS(Longest Common Subsequence)는 두 문자열 X, Y에서 **공통 부분 수열** 중 가장 긴 것을 찾는 문제다.

- **부분 수열**: 연속하지 않아도 되지만, **순서**는 유지해야 함
- **부분 문자열(Substring)** 과 다름: LCS는 연속할 필요 없음

## 예시

```
X = A B R A C A D A B R A
Y = Y A B B A D A B B A D

LCS: BABAD 또는 BAD (여러 가지 가능)
```

---

# 2. 핵심 아이디어 — Principle of Optimality

C[i][j] = X의 처음 i글자와 Y의 처음 j글자 사이의 LCS 길이

**점화식:**

```
초기: C[i][0] = 0, C[0][j] = 0

if x_i = y_j:     C[i][j] = C[i-1][j-1] + 1
if x_i ≠ y_j:     C[i][j] = max(C[i-1][j], C[i][j-1])
```

**의미:**
- 마지막 글자가 같으면 → 둘 다 포함, 이전 LCS + 1
- 마지막 글자가 다르면 → 둘 중 하나를 제외한 최대값

---

# 3. 의사코드

```plaintext
function LCS(x[1..m], y[1..n]):
    C = array[0..m][0..n]

    for i = 0 to m: C[i][0] = 0
    for j = 0 to n: C[0][j] = 0

    for i = 1 to m:
        for j = 1 to n:
            if x[i] == y[j]:
                C[i][j] = C[i-1][j-1] + 1
            else:
                C[i][j] = max(C[i-1][j], C[i][j-1])

    return C[m][n]
```

---

# 4. 자바스크립트 구현

```javascript
function lcs(x, y) {
    const m = x.length;
    const n = y.length;
    // C[i][j]: x[0..i-1]과 y[0..j-1]의 LCS 길이
    const C = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));

    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (x[i - 1] === y[j - 1]) {
                C[i][j] = C[i - 1][j - 1] + 1;
            } else {
                C[i][j] = Math.max(C[i - 1][j], C[i][j - 1]);
            }
        }
    }

    return C[m][n]; // LCS 길이
}

// LCS 문자열 복원 (역추적)
function lcsString(x, y) {
    const m = x.length;
    const n = y.length;
    const C = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));

    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (x[i - 1] === y[j - 1]) {
                C[i][j] = C[i - 1][j - 1] + 1;
            } else {
                C[i][j] = Math.max(C[i - 1][j], C[i][j - 1]);
            }
        }
    }

    // 역추적으로 실제 LCS 문자열 복원
    let result = '';
    let i = m, j = n;
    while (i > 0 && j > 0) {
        if (x[i - 1] === y[j - 1]) {
            result = x[i - 1] + result;
            i--; j--;
        } else if (C[i - 1][j] > C[i][j - 1]) {
            i--;
        } else {
            j--;
        }
    }

    return result;
}

// 사용 예시
const x = 'ABRACADABRA';
const y = 'YABBADABBAD';
console.log(lcs(x, y));       // 6
console.log(lcsString(x, y)); // 'ABABD' 또는 유사한 LCS
```

---

# 5. DP 테이블 시각화

X = "ABCD", Y = "ACBD"

```
    ""  A  C  B  D
""   0  0  0  0  0
A    0  1  1  1  1
B    0  1  1  2  2
C    0  1  2  2  2
D    0  1  2  2  3  ← LCS 길이 = 3
```

오른쪽 아래 값이 최종 LCS 길이.
역추적: 대각선 이동한 위치가 LCS에 포함된 문자.

---

# 6. 복잡도

| 항목 | 내용 |
|------|------|
| **시간 복잡도** | **O(mn)** — 두 문자열 길이 m, n |
| **공간 복잡도** | O(mn) — DP 테이블 / O(n)으로 최적화 가능 |

---

# 7. 활용

- **diff 도구** — 두 파일 변경 사항 비교 (git diff의 핵심)
- **유사도 측정** — 생물정보학 DNA 서열 비교
- **편집 거리** — LCS 길이로부터 삽입/삭제 횟수 도출

---

## Related
- [[_MOC]]
- [[Dynamic-Programming]] — 2D DP 테이블의 대표 예제
- [[Chained-Matrix-Multiplication]] — 같은 DP 구조 (최적성 원리)

## Sources
- [Notion 원본](https://www.notion.so/LCS-11f35c50238380f3bcebf1f8b42fa080)
