---
title: DFS와 BFS
aliases: [DFS, BFS, depth first search, breadth first search, 깊이우선, 너비우선]
type: concept
status: budding
created: 2026-05-23
updated: 2026-05-24
tags: [cs/algorithm, codingtest, status/budding, 코테기본]
notion-url: https://www.notion.so/DFS-BFS-bb1912db71b94e4f8acf405f5c461ba7
related:
  - "[[_MOC]]"
  - "[[그래프]]"
  - "[[트리]]"
  - "[[스택과-큐]]"
  - "[[백트래킹]]"
  - "[[재귀]]"
source: ["Notion: 코딩 테스트 알고리즘 이론"]
migrated-from: "Notion: DFS와 BFS"
---

# 🪜 DFS와 BFS

> TL;DR: DFS는 한 경로를 끝까지(스택/재귀), BFS는 레벨 순서로(큐). DFS는 경로 탐색·백트래킹, BFS는 최단 경로 보장. 둘 다 O(V+E).

---

DFS(Depth-First Search)와 BFS(Breadth-First Search)는 그래프/트리에서 **노드를 탐색하거나 경로를 찾는 데** 사용되는 두 핵심 알고리즘이다.

---

# 1. DFS (깊이 우선 탐색)

한 경로를 끝까지 탐색한 후 더 이상 갈 수 없을 때 되돌아가며 다른 경로를 탐색. **재귀** 또는 **스택** 구현.

## DFS 동작 원리

1. 시작 노드를 스택에 넣고 방문 처리
2. 스택 최상단 노드를 꺼내 인접 노드 탐색
3. 미방문 인접 노드를 스택에 push, 방문 처리
4. 스택이 빌 때까지 반복

## DFS 사용 시점

- **경로가 깊은 곳에 답이 있을 때** — 모든 가능한 경로 탐색
- **백트래킹** 필요할 때 — 재귀 호출 스택이 곧 되돌아가는 수단
- **재귀적 구조** — 트리 순회, 파일 시스템 순회
- **메모리 절약** — BFS보다 큐 크기가 작음

## 구현 1 — 재귀 (인접 리스트)

```javascript
const graph = {
    1: [2, 3],
    2: [4, 5],
    3: [6],
    4: [], 5: [], 6: []
};

const visited = new Set();

function dfs(node) {
    if (visited.has(node)) return;
    console.log(node);
    visited.add(node);
    graph[node].forEach(neighbor => dfs(neighbor));
}

dfs(1); // 1 2 4 5 3 6
```

## 구현 2 — 스택 (인접 리스트)

```javascript
function dfs(start) {
    const stack = [start];
    const visited = new Set();

    while (stack.length > 0) {
        const node = stack.pop();
        if (!visited.has(node)) {
            console.log(node);
            visited.add(node);
            graph[node].forEach(neighbor => {
                if (!visited.has(neighbor)) stack.push(neighbor);
            });
        }
    }
}
```

## 구현 3 — 스택 (인접 행렬)

```javascript
const graph = [
    [0, 1, 1, 0, 0, 0], // 1번 노드
    [0, 0, 0, 1, 1, 0], // 2번 노드
    [0, 0, 0, 0, 0, 1], // 3번 노드
    [0, 0, 0, 0, 0, 0], // 4번 노드
    [0, 0, 0, 0, 0, 0], // 5번 노드
    [0, 0, 0, 0, 0, 0], // 6번 노드
];

function dfs(start) {
    const stack = [start];
    const visited = new Set();

    while (stack.length > 0) {
        const node = stack.pop();
        if (!visited.has(node)) {
            console.log(node + 1); // 0-indexed → +1
            visited.add(node);
            for (let n = graph[node].length - 1; n >= 0; n--) {
                if (graph[node][n] === 1 && !visited.has(n)) stack.push(n);
            }
        }
    }
}

dfs(0);
```

**시간 복잡도: O(V + E)**

---

# 2. BFS (너비 우선 탐색)

한 노드의 모든 이웃 노드를 먼저 탐색한 후 그 이웃들의 이웃을 탐색. **큐(Queue)** 구현.

## BFS 동작 원리

1. 시작 노드를 큐에 넣고 방문 처리
2. 큐에서 노드를 꺼내 인접 노드 탐색 (FIFO)
3. 미방문 인접 노드를 큐에 push, 방문 처리
4. 큐가 빌 때까지 반복

## BFS 사용 시점

- **최단 경로** — 같은 깊이의 노드를 먼저 탐색하므로 첫 도달 = 최단 경로 보장
- **레벨별 탐색** — 조직도, 소셜 네트워크 거리
- **최소 이동 거리** 계산

## 구현 — 인접 리스트

```javascript
function bfs(start) {
    const queue = [start];
    const visited = new Set();
    visited.add(start);

    while (queue.length > 0) {
        const node = queue.shift();
        console.log(node);

        graph[node].forEach(neighbor => {
            if (!visited.has(neighbor)) {
                visited.add(neighbor);
                queue.push(neighbor);
            }
        });
    }
}

bfs(1); // 1 2 3 4 5 6
```

## 구현 — 인접 행렬

```javascript
function bfs(start) {
    const queue = [start];
    const visited = new Set();
    visited.add(start);

    while (queue.length > 0) {
        const node = queue.shift();
        console.log(node + 1); // 0-indexed → +1

        for (let neighbor = 0; neighbor < graph[node].length; neighbor++) {
            if (graph[node][neighbor] === 1 && !visited.has(neighbor)) {
                visited.add(neighbor);
                queue.push(neighbor);
            }
        }
    }
}
```

**시간 복잡도: O(V + E)**

---

# 3. DFS vs BFS 비교

| 특징 | DFS | BFS |
|------|-----|-----|
| **탐색 방식** | 한 경로 끝까지 → 되돌아가기 | 레벨별 (같은 깊이 먼저) |
| **자료구조** | **스택** (재귀 콜 스택) | **큐** |
| **최단 경로** | ❌ (보장 안 됨) | ✅ (보장됨) |
| **메모리** | 깊이에 비례 (적음) | 너비에 비례 (많음) |
| **재귀 구현** | ✅ 쉬움 | ❌ 비재귀 큐 기반 |
| **시간 복잡도** | O(V + E) | O(V + E) |
| **적합 문제** | 경로 탐색, 백트래킹, 깊은 곳 탐색 | 최단 경로, 레벨별 탐색 |

## 상황별 선택 가이드

| 상황 | 선택 |
|------|------|
| 최단 경로를 찾아야 할 때 | **BFS** |
| 모든 경로를 탐색해야 할 때 | **DFS** |
| 해가 깊은 곳에 있을 때 | **DFS** |
| 레벨별 탐색 (조직도, 친구 관계 단계) | **BFS** |
| 재귀로 구현해야 할 때 | **DFS** |
| 메모리를 절약해야 할 때 | **DFS** |

---

---

# 4. 코테 적용 가이드

(구 `_patterns/dfs-bfs.md` 흡수.)

## DFS 적용 케이스
- 경로 존재 여부, 백트래킹, 위상 정렬
- 트리 깊이/순서 (preorder/inorder/postorder)
- 사이클 감지

## BFS 적용 케이스
- 가중치 없는 그래프 **최단 거리**
- 레벨 단위 순회 (조직도, 친구 관계 단계)
- 다중 시작점 (multi-source BFS)

## Pseudocode (간이 템플릿)

```python
# DFS (재귀)
def dfs(node, visited):
    if node in visited: return
    visited.add(node)
    for nxt in graph[node]: dfs(nxt, visited)

# BFS
from collections import deque
def bfs(start):
    q = deque([(start, 0)])
    visited = {start}
    while q:
        node, dist = q.popleft()
        for nxt in graph[node]:
            if nxt not in visited:
                visited.add(nxt)
                q.append((nxt, dist + 1))
```

## 자주 나오는 문제
- 백준 1260 DFS와 BFS
- 프로그래머스 게임 맵 최단거리
- LeetCode 200 Number of Islands

코드 원본: `~/깃허브/CodingTest/dfs-bfs/`

---

## Related
- [[_MOC]]
- [[그래프]] — DFS/BFS는 그래프 탐색의 기반
- [[트리]] — 트리 순회에도 DFS/BFS 적용
- [[스택과-큐]] — DFS는 스택, BFS는 큐를 내부 자료구조로 사용
- [[백트래킹]] — DFS + pruning
- [[재귀]] — DFS의 재귀 구현 기반
- [[Dynamic-Programming]] — BFS/DFS + 메모이제이션 결합

## Sources
- [Notion 원본](https://www.notion.so/DFS-BFS-bb1912db71b94e4f8acf405f5c461ba7)
