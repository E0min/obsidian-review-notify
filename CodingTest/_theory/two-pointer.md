---
title: Two Pointer 패턴
aliases: [투포인터, two pointer]
type: concept
status: seedling
created: 2026-05-23
updated: 2026-05-25
tags: [cs/algorithm, status/seedling, career/fe, codingtest]
related:
  - "[[_MOC]]"
  - "[[sliding-window]]"
  - "[[../problems/programmers/159994-카드-뭉치]]"
  - "[[../_Tips/출력조건-구조파악]]"
migrated-from: "CodingTest/_patterns/two-pointer.md"
---

# Two Pointer 패턴

> TL;DR: 정렬된 배열에서 양 끝(또는 한 방향)에서 좁혀가며 O(n²) → O(n) 만드는 패턴.

## When to use
- 정렬된 배열에서 합/차/비교 조건
- 슬라이딩 윈도우의 단순 형태
- 중복 제거 in-place

## Typical pattern
```python
left, right = 0, len(arr) - 1
while left < right:
    s = arr[left] + arr[right]
    if s == target: return [left, right]
    if s < target: left += 1
    else: right -= 1
```

## 변형 — 단방향 두 포인터 (시뮬레이션)

양 끝이 아닌 **두 배열을 각각 앞에서부터** 동시에 전진하는 형태:

```javascript
// 두 덱에서 goal 순서 완성 — 카드 뭉치 (159994)
let c1 = 0, c2 = 0, g = 0;
while (g < goal.length) {
    if (arr1[c1] === goal[g])      { c1++; g++; }
    else if (arr2[c2] === goal[g]) { c2++; g++; }
    else return "No"; // 그리디 조기 종료
}
return "Yes";
```

## 자주 나오는 문제
- LeetCode 167 Two Sum II
- LeetCode 15 3Sum
- 프로그래머스 두 개 뽑아 더하기
- [[../problems/programmers/159994-카드-뭉치]] — 두 배열 단방향 포인터 + 그리디 조기 종료

## Related
- [[_MOC]]
- [[sliding-window]] — 비슷한 좁히기·확장 메커니즘
- [[../_Tips/출력조건-구조파악]] — 카드 뭉치 예제의 a/~a 구조
- [[../_strategy/풀이순서]]
