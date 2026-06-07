---
title: Dynamic Programming
aliases: [DP, 동적 계획법, dynamic programming, memoization, tabulation, 탑다운, 바텀업, top-down, bottom-up]
type: concept
status: budding
created: 2026-05-23
updated: 2026-05-25
tags: [cs/algorithm, codingtest, status/budding, 코테기본, DP]
notion-url: https://www.notion.so/Dynamic-Programming-11235c5023838008ac6befc9cb35e0f0
related:
  - "[[_MOC]]"
  - "[[재귀]]"
  - "[[분할-정복]]"
  - "[[그리디]]"
  - "[[LCS]]"
  - "[[Knapsack]]"
  - "[[Chained-Matrix-Multiplication]]"
  - "[[벨만-포드]]"
  - "[[플로이드-워셜]]"
source: ["Notion: 코딩 테스트 알고리즘 이론"]
---

# 🛰️ Dynamic Programming

> TL;DR: 최적 부분 구조 + 중복 부분 문제 → 메모이제이션(탑다운) 또는 타뷸레이션(바텀업). 4단계 접근법 + 5가지 발상 패턴(단계/상태/중복/최대최소/제약).

## 노션 원본
- [Dynamic Programming (Notion)](https://www.notion.so/Dynamic-Programming-11235c5023838008ac6befc9cb35e0f0)

---

# 1. 동적 프로그래밍이란?

동적 프로그래밍(DP)은 **최적화 문제**를 해결하는 방법으로, 문제를 더 작은 하위 문제로 나누고, 이를 해결한 후 그 결과를 저장하여 **중복 계산을 방지**하는 알고리즘이다. **최적 부분 구조**와 **중복되는 하위 문제**를 가진 문제에서 매우 유용.

두 가지 방식:
1. **탑다운 (Top-Down, Memoization)**: 재귀적으로 큰 문제를 작은 문제로 나누어 해결. 메모이제이션으로 중복 계산 방지.
2. **바텀업 (Bottom-Up, Tabulation)**: 작은 문제부터 해결하고 그 결과를 바탕으로 큰 문제 해결. 반복문 기반.

**최적성 원칙**: 어떤 문제의 최적 해결책이 **하위 문제들의 최적 해결책으로부터 구성**된다는 원칙. 예: 피보나치 F(n) = F(n-1) + F(n-2)의 최적 해로부터 구성.

---

# 2. Simple Recursion

같은 하위 문제를 반복 계산하는 비효율적 방법. **O(2^n)** 시간복잡도.

```c
function Fib(n){
    if (n < 2) return n;
    else return Fib(n - 1) + Fib(n - 2);
}
```

`Fib(5)` 계산 시 `Fib(3)`와 `Fib(4)`가 여러 번 중복 계산.

---

# 3. Recursion with Memoization (탑다운 방식)

이미 계산된 결과를 저장 → 반복 계산 방지. **O(n)** 시간복잡도.

```c
F[1..n] = {-1, -1, ..., -1};  // 초기화
function Fib(n) {
    if (F[n] > 0) return F[n];  // 이미 계산된 값이 있으면 반환
    if (n < 2) return n;
    else {
        F[n] = Fib(n - 1) + Fib(n - 2);
        return F[n];
    }
}
```

## DP(메모이제이션) 문제 접근법 — 4단계

### 1. '상태' 정의하기 (함수 정의)
- `D(n)` : "n이라는 입력값에 대한 문제의 정답"
- `D(i, j)` : "i부터 j까지의 범위에서 구해야 하는 정답"
- `D(k, w)` : "k번째 아이템까지 고려했고, 남은 용량이 w일 때의 최대 가치"

### 2. 재귀 관계식 (점화식) 세우기
- `D(n)`을 더 작은 문제(`D(n-1)`, `D(n-k)` 등)로 표현하는 규칙
- 예: `D(n) = D(n-1) + D(n-5)`

### 3. 기저 상태 (Base Case) 정의
- `D(0)`, `D(1)` 등 더 이상 쪼갤 수 없는 문제의 초기값

### 4. '메모장' 준비 + 로직 구현
```javascript
function D(n) {
    // (1) 메모 확인
    if (memo[n] !== -1) return memo[n];

    // (2) 기저 상태
    if (n === 0 || n === 1) {
        memo[n] = baseValue;
        return baseValue;
    }

    // (3) 점화식 수행
    const result = D(n - 1) + D(n - 2);

    // (4) 메모 & 반환
    memo[n] = result;
    return result;
}
```

---

# 4. Iteration with Tabulation (바텀업 방식)

작은 문제부터 차례대로 해결. 재귀 X, 반복문. 스택 오버플로우 방지 + 메모리 효율.

```c
function Fib(n) {
    if (n < 2) return n;
    F[0] = 0;
    F[1] = 1;
    for (let i = 2; i <= n; i++) {
        F[i] = F[i - 2] + F[i - 1];
    }
    return F[n];
}
```

## DP(바텀업) 문제 접근법 — 4단계

### 1. '상태' 정의 (DP 테이블)
- `dp[n]` = "n이라는 상태에 대한 정답이 담길 배열의 n번째 칸"

### 2. 점화식 세우기 (탑다운과 동일)

### 3. 'DP 테이블' 준비 + 기저 상태 초기화
```javascript
const dp = Array(N + 1).fill(0);
dp[0] = (0에 대한 정답);
dp[1] = (1에 대한 정답);
```

### 4. 반복문으로 테이블 채우기
```javascript
for (let i = 2; i <= N; i++) {
    dp[i] = dp[i - 1] + dp[i - 2];  // 점화식
}
// 최종 답: dp[N]
```

핵심: `dp[i]` 계산 시 `dp[i-1]`, `dp[i-2]`는 **이전 반복에서 이미 계산되어 저장된 값**이므로 단순히 가져다 쓰기만 하면 됨.

---

# 5. 다른 알고리즘들과의 비교

### A. 분할 정복 vs DP
- **[[분할-정복]]**: 하위 문제를 독립적으로 해결 후 합침. **동일한 하위 문제를 여러 번 계산**할 수 있음.
- **DP**: 중복 하위 문제를 한 번만 계산하고 재사용. **반복 계산을 줄이기 위해 결과 저장**.

### B. [[그리디]] vs DP
- **그리디**: 각 단계에서 **지역적으로 최적의 선택**. 전체 최적 보장 X.
- **DP**: 가능한 모든 해결책을 계산한 후 **최적의 해결책** 선택. **최적성 원칙** 따름. 시간 더 걸리지만 **전체 최적 보장**.

---

# DP 발상 패턴 — 5가지 단서

## 1. 단계별로 진행되며, 이전 결과가 다음 결정을 좌우하는가?
- **최적 부분 구조**: `i`번째 답이 `i-1`번째까지의 답을 바탕으로 구해짐
- **의존성**: `i`번째 결정에 `i-1`번째 상태만 필요 (혹은 그 이전 정보가 `i-1` 상태에 압축)
- 문제가 **순차적인 결정의 연쇄**로 보인다면 DP

## 2. '상태(State)'를 명확하게 정의할 수 있는가?
- "꼭 알아야 하는 최소한의 정보"가 무엇인지
- "i번째 아이템까지 봤을 때 j 값을 만들 수 있는 경우의 수는?"처럼 명확히
- 상태가 DP 테이블 인덱스(`dp[i][j]`)가 됨
- 변수 너무 많으면(`dp[i][j][k][l][m]...`) DP 아니거나 잘못 정의

## 3. 같은 계산을 반복하게 되는가?
- 재귀(DFS)로 풀 때 **같은 인자의 함수가 여러 번 호출**되면 DP 필요
- **중복되는 부분 문제 (Overlapping Subproblems)**: 다른 경로가 동일한 '상태'로 귀결

## 4. 질문이 '최대/최소/경우의 수/가능성'을 묻는가?
- **최대/최소**: "...의 최댓값은?" / "...에 필요한 최소 비용은?"
- **경우의 수**: "...을 만족하는 경우의 수는?"
- **가능성**: "...이 가능한가?"

## 5. (실용 팁) 제약 조건이 DP를 암시하는가?
- `N` ≈ 1,000,000 : O(N) 또는 O(N log N) → 1차원 DP
- `N` ≈ 2,000~5,000 : O(N²) → 2차원 DP `dp[N][N]`
- `N=100, K=10,000` : O(NK) → 2차원 DP `dp[N][K]`
- `N` ≈ 15~20 : O(2^N) → 비트마스킹 DP

---

## 요약

**"순서대로 진행(1) + 상태 정의 가능(2) + 최대/최소/경우의 수(4) + 제약 조건 O(N²)/O(N*K)(5)"** → DP

---

# 코테 적용 가이드 — 진단 질문

(구 `_patterns/dp.md` 흡수.)

문제 보고 30초 안에 던지는 진단 질문:

- 최적값(min/max/count)을 구하는가?
- 작은 부분 문제로 쪼갤 수 있는가?
- 부분 문제가 **중복**되는가?
- 같은 입력에 같은 출력인가?

4개 중 3개 이상 ✅이면 DP 시도.

## Top-down vs Bottom-up (Python 간이 템플릿)

```python
# Top-down (memoization)
import functools
@functools.cache
def f(i):
    if i <= 1: return i
    return f(i-1) + f(i-2)

# Bottom-up (tabulation)
dp = [0] * (n + 1)
dp[1] = 1
for i in range(2, n + 1):
    dp[i] = dp[i-1] + dp[i-2]
```

## 자주 나오는 문제
- 백준 1149 RGB 거리
- 백준 11053 LIS
- LeetCode 322 Coin Change
- 프로그래머스 정수 삼각형

코드 원본: `~/깃허브/CodingTest/dp/`

---

## Related
- [[_MOC]]
- [[재귀]] — 탑다운의 기반
- [[분할-정복]] — overlapping 여부로 구분
- [[그리디]] — 비교 대상
- [[LCS]], [[Knapsack]], [[Chained-Matrix-Multiplication]] — DP 응용
- [[벨만-포드]], [[플로이드-워셜]] — 그래프 DP
