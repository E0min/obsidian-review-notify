---
title: Monotonic Stack 패턴
aliases: [단조 스택, monotonic stack, next greater element]
type: concept
status: seedling
created: 2026-05-23
updated: 2026-05-25
tags: [cs/algorithm, status/seedling, career/fe, codingtest]
related:
  - "[[_MOC]]"
  - "[[sliding-window]]"
  - "[[스택과-큐]]"
migrated-from: "CodingTest/_patterns/monotonic-stack.md"
---

# Monotonic Stack 패턴

> TL;DR: 스택에 단조(증가/감소) 순으로 유지하며 O(n)으로 "다음 큰/작은 원소" 류 문제 해결.

## When to use
- Next/Previous Greater/Lesser Element
- 히스토그램 최대 직사각형
- 주식 시세 류 (다음 큰 값까지의 거리)

## Typical pattern
```python
# Next Greater Element
def nextGreater(arr):
    n = len(arr)
    result = [-1] * n
    stack = []  # 인덱스 저장
    for i in range(n):
        while stack and arr[stack[-1]] < arr[i]:
            result[stack.pop()] = arr[i]
        stack.append(i)
    return result
```

## 자주 나오는 문제
- LeetCode 84 Largest Rectangle in Histogram
- LeetCode 496 Next Greater Element I
- 프로그래머스 주식가격

## Related
- [[_MOC]]
- [[sliding-window]]
- [[스택과-큐]] — 기반 자료구조
- `~/깃허브/CodingTest/stack-queue/`
