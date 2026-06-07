---
title: Sliding Window 패턴
aliases: [슬라이딩 윈도우, sliding window]
type: concept
status: seedling
created: 2026-05-23
updated: 2026-05-25
tags: [cs/algorithm, status/seedling, career/fe, codingtest]
related:
  - "[[_MOC]]"
  - "[[two-pointer]]"
  - "[[monotonic-stack]]"
migrated-from: "CodingTest/_patterns/sliding-window.md"
---

# Sliding Window 패턴

> TL;DR: 연속 부분 배열/문자열에서 조건 만족하는 최적값. 윈도우를 늘리고 줄이며 O(n).

## Two types
1. **고정 크기** — k 크기 합/평균
2. **가변 크기** — 조건 만족하는 최대/최소 길이

## Typical pattern (가변)
```python
left = 0
best = 0
state = init()
for right in range(len(arr)):
    add(state, arr[right])
    while not condition(state):
        remove(state, arr[left])
        left += 1
    best = max(best, right - left + 1)
```

## 자주 나오는 문제
- LeetCode 76 Minimum Window Substring
- LeetCode 3 Longest Substring Without Repeating
- 프로그래머스 연속 부분 수열

## Related
- [[_MOC]]
- [[two-pointer]] — 단순 형태
- [[monotonic-stack]]
