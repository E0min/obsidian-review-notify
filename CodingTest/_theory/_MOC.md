---
type: moc
title: CodingTest/_theory — 알고리즘 이론 인덱스
status: budding
created: 2026-05-23
updated: 2026-05-23
tags: [moc, codingtest, cs/algorithm]
source: ["Notion: 코딩 테스트 알고리즘 이론 (3f9bc876018d49c3b07f245170166934)"]
migrated-from: Downloads/Private & Shared/코딩 테스트 알고리즘 이론 3f9bc876018d49c3b07f245170166934.html
---

# _theory — 알고리즘 이론

> 노션 원본: "코딩 테스트 알고리즘 이론" (Status: In progress)
> 참고서: [교보문고 — E000008410599](https://product.kyobobook.co.kr/book/preview/E000008410599)
>
> 23개 이론 항목 + 3개 풀이 패턴 = 26개. 각 stub의 `notion-url:` frontmatter 클릭 → 노션 원본으로 이동.
> 본문을 옵시디언에 채우면 SSOT가 점진적으로 옵시디언으로 이동.

## 코테 기본 (7)

| 제목 | 노트 | 핵심 |
|------|------|------|
| 🪜 시간복잡도와 디버그 | [[시간복잡도와-디버그]] | Big-O, 디버깅 |
| 🏅 정렬 알고리즘 | [[정렬-알고리즘]] | bubble/selection/insertion/merge/quick |
| 📼 재귀 | [[재귀]] | base case + recursive case |
| 🏏 분할 정복 | [[분할-정복]] | divide & conquer |
| ⛰️ 백트래킹 | [[백트래킹]] | DFS + pruning |
| 🎚️ 그리디 | [[그리디]] | locally optimal |
| 🛰️ Dynamic Programming | [[Dynamic-Programming]] | overlapping subproblems · **코테 가이드 포함** |

## 풀이 패턴 (3)

| 제목 | 노트 | 핵심 |
|------|------|------|
| ↔️ Two Pointer | [[two-pointer]] | 양 끝/단방향 좁히기 → O(n) |
| 🪟 Sliding Window | [[sliding-window]] | 연속 부분 배열, 고정/가변 윈도우 |
| 📚 Monotonic Stack | [[monotonic-stack]] | 다음 큰/작은 원소, 단조 유지 |

## 자료구조 (5)

| 제목 | 노트 | 핵심 |
|------|------|------|
| 🪫 힙으로 우선순위 큐 만들기 | [[힙으로-우선순위-큐]] | priority queue, binary heap |
| 🔮 스택과 큐 | [[스택과-큐]] | LIFO / FIFO |
| 🎀 그래프 | [[그래프]] | vertex, edge, 인접 행렬/리스트 |
| 🥅 트리 | [[트리]] | binary tree, BST, traversal |
| 🎶 해시 (Set, Map) | [[해시-Set-Map]] | O(1) 조회 |

## 그래프 알고리즘 (6)

| 제목 | 노트 | traits |
|------|------|--------|
| 🪜 DFS와 BFS | [[DFS와-BFS]] | 무방향/방향 그래프 · **코테 가이드 포함** |
| 🛕 다익스트라 | [[다익스트라]] | Single Source Shortest Paths, 음수 불가, 방향 그래프 |
| 🎟️ Kruscal | [[Kruscal]] | MST, 그리디, 무방향, 유니온파인드 |
| 📣 Prim | [[Prim]] | MST, 그리디, 무방향, 우선순위 큐 |
| 🌓 벨만-포드 | [[벨만-포드]] | Single Source Shortest Paths, 음수 가능, 방향 그래프, DP |
| ⛓️ 플로이드 워셜 | [[플로이드-워셜]] | All Pairs Shortest Paths, 음수 가능, 방향, DP |

## DP 응용 (3)

| 제목 | 노트 | 핵심 |
|------|------|------|
| 🎣 Chained Matrix Multiplication | [[Chained-Matrix-Multiplication]] | 행렬 곱 순서 최적화, DP |
| ♥️ 최장 공통 부분 수열 (LCS) | [[LCS]] | 2D DP |
| 🕢 Knapsack | [[Knapsack]] | 0/1 vs 분할, DP |

## 스케쥴링 (2)

| 제목 | 노트 | 핵심 |
|------|------|------|
| Shortest Job First | [[Shortest-Job-First]] | 우선순위 큐, SJF |
| 🎯 스케쥴링 | [[스케쥴링]] | 그리디 |

## 진행 상태

| 분류 | 개수 | 작성 진행 |
|------|------|----------|
| 이론 stub (notion-url 참조) | 23 | 0% — 옵시디언에 본문 채우기 시작 |
| 풀이 패턴 (코테 실전) | 3 | seedling |
| 본문 작성됨 (budding 이상) | 2 (DFS와-BFS, Dynamic-Programming) | — |
| evergreen | 0 | — |

## See also
- [[../_MOC]] — CodingTest 전체 진입
- [[../_strategy/_MOC]] — 학습·풀이 메타 프로세스
- [[../_Tips/_MOC]] — 실전 구현·사고 트릭
- [[../../CS/algorithms/_MOC]] — CS 이론 (교과서적)
- 노션 원본 워크스페이스
- 참고서: [교보문고 E000008410599](https://product.kyobobook.co.kr/book/preview/E000008410599)
