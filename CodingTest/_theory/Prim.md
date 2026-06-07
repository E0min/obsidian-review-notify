---
title: Prim 알고리즘
aliases: [Prim algorithm, MST, minimum spanning tree, 프림, 최소신장트리]
type: concept
status: budding
created: 2026-05-23
updated: 2026-05-24
tags: [cs/algorithm, codingtest, status/budding, 무방향그래프, MST, 그리디]
notion-url: https://www.notion.so/Prim-b0ba7c0976634ad8a0500644f4cd7dc2
related:
  - "[[_MOC]]"
  - "[[그래프]]"
  - "[[그리디]]"
  - "[[힙으로-우선순위-큐]]"
  - "[[Kruscal]]"
source: ["Notion: 코딩 테스트 알고리즘 이론"]
migrated-from: "Notion: Prim 알고리즘"
---

# 📣 Prim 알고리즘

> TL;DR: 임의 시작 정점 → 연결된 간선 중 최소 가중치 선택 → 새 정점 추가 반복 → MST 완성. 우선순위 큐 기반. O(E log V). 밀집 그래프에 적합.

---

# 1. 정의

프림(Prim) 알고리즘은 **최소 신장 트리(MST, Minimum Spanning Tree)**를 구하는 알고리즘이다. **무방향 가중치 그래프**에서 모든 노드를 최소 비용으로 연결하는 트리를 찾는다.

## 특징

| 항목 | 내용 |
|------|------|
| **그래프 유형** | 무방향 가중치 그래프 |
| **알고리즘 패턴** | 탐욕적 (Greedy) + 정점 중심 |
| **자료구조** | 우선순위 큐 (최소 힙) |
| **시간 복잡도** | O(V²) 인접행렬, **O(E log V)** 인접리스트+힙 |
| **적합한 그래프** | **밀집 그래프 (Dense)** |

---

# 2. 알고리즘 순서

1. 임의의 시작 노드 선택, 우선순위 큐에 `(0, start)` 삽입
2. 큐에서 최소 비용 간선 추출
   - 이미 방문한 노드면 건너뜀
3. 현재 노드를 MST에 추가, 비용 누적
4. 현재 노드의 인접 노드 중 미방문 노드를 큐에 삽입
5. 모든 노드가 방문될 때까지 반복

---

# 3. 의사코드

```plaintext
function Prim(graph):
    visited = []
    minHeap = [(0, startNode)]
    totalCost = 0

    while minHeap is not empty:
        [cost, currentNode] = extractMin(minHeap)
        if currentNode is visited: continue

        mark currentNode as visited
        totalCost += cost

        for [neighbor, weight] of currentNode:
            if neighbor is not visited:
                add [weight, neighbor] to minHeap

    return totalCost
```

---

# 4. 자바스크립트 구현

```javascript
class MinHeap {
    constructor() {
        this.heap = [];
    }

    insert([cost, node]) {
        this.heap.push([cost, node]);
        this.bubbleUp();
    }

    bubbleUp() {
        let index = this.heap.length - 1;
        while (index > 0) {
            let parentIndex = Math.floor((index - 1) / 2);
            if (this.heap[index][0] >= this.heap[parentIndex][0]) break;
            [this.heap[index], this.heap[parentIndex]] = [this.heap[parentIndex], this.heap[index]];
            index = parentIndex;
        }
    }

    extractMin() {
        const min = this.heap[0];
        const end = this.heap.pop();
        if (this.heap.length > 0) {
            this.heap[0] = end;
            this.sinkDown();
        }
        return min;
    }

    sinkDown() {
        let index = 0;
        const length = this.heap.length;
        const element = this.heap[0];

        while (true) {
            let left = 2 * index + 1;
            let right = 2 * index + 2;
            let swap = null;

            if (left < length && this.heap[left][0] < element[0]) swap = left;
            if (right < length) {
                if ((swap === null && this.heap[right][0] < element[0]) ||
                    (swap !== null && this.heap[right][0] < this.heap[left][0])) {
                    swap = right;
                }
            }
            if (swap === null) break;
            [this.heap[index], this.heap[swap]] = [this.heap[swap], this.heap[index]];
            index = swap;
        }
    }

    isEmpty() {
        return this.heap.length === 0;
    }
}

function prim(graph, start = 1) {
    const n = graph.length;
    const visited = new Array(n).fill(false);
    const minHeap = new MinHeap();
    let totalCost = 0;

    minHeap.insert([0, start]);

    while (!minHeap.isEmpty()) {
        const [cost, currentNode] = minHeap.extractMin();

        if (visited[currentNode]) continue;
        visited[currentNode] = true;
        totalCost += cost;

        for (const [neighbor, weight] of graph[currentNode]) {
            if (!visited[neighbor]) {
                minHeap.insert([weight, neighbor]);
            }
        }
    }

    return totalCost;
}

// 사용 예시: 인접 리스트 (0번은 빈 배열, 1부터 시작)
const graph = [
    [],
    [[2, 3], [3, 1]], // 노드 1: (노드2, 비용3), (노드3, 비용1)
    [[1, 3], [3, 3], [4, 6]], // 노드 2
    [[1, 1], [2, 3], [4, 5]], // 노드 3
    [[2, 6], [3, 5]]  // 노드 4
];

console.log(prim(graph)); // MST 총 비용 출력
```

---

# 5. 크루스칼 vs 프림 비교

| 항목 | 프림 | [[Kruscal]] |
|------|------|------------|
| **접근 방식** | 정점 중심 (트리 확장) | 간선 중심 (정렬 후 선택) |
| **시간 복잡도** | O(E log V) | O(E log E) |
| **적합한 그래프** | **밀집 그래프** | **희소 그래프** |
| **사이클 처리** | 방문 처리로 방지 | Union-Find |
| **다익스트라 유사성** | ✅ (구조 유사) | ❌ |

**두 알고리즘 모두 결과 MST의 총 비용은 동일**하나, 시작 정점에 따라 간선 선택이 달라질 수 있음.

---

## Related
- [[_MOC]]
- [[그래프]] — 프림의 대상 자료구조
- [[그리디]] — 매 단계 최소 비용 선택
- [[힙으로-우선순위-큐]] — 우선순위 큐로 최소 간선 추출
- [[Kruscal]] — 같은 MST를 간선 중심으로 구하는 알고리즘

## Sources
- [Notion 원본](https://www.notion.so/Prim-b0ba7c0976634ad8a0500644f4cd7dc2)
