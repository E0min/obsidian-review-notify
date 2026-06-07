---
title: Kruscal 알고리즘
aliases: [Kruskal, Kruscal, MST, minimum spanning tree, 크루스칼, 유니온파인드, union-find, 최소신장트리]
type: concept
status: budding
created: 2026-05-23
updated: 2026-05-24
tags: [cs/algorithm, codingtest, status/budding, 무방향그래프, MST, 그리디]
notion-url: https://www.notion.so/Kruscal-44be423cbd54493abf38d106127c043d
related:
  - "[[_MOC]]"
  - "[[그래프]]"
  - "[[그리디]]"
  - "[[Prim]]"
source: ["Notion: 코딩 테스트 알고리즘 이론"]
migrated-from: "Notion: Kruscal 알고리즘"
---

# 🎟️ Kruscal 알고리즘

> TL;DR: 간선을 가중치 오름차순 정렬 → 사이클 없는 간선만 선택 → MST 완성. Union-Find로 사이클 탐지. O(E log E). 희소 그래프에 적합.

---

# 1. 정의

크루스칼(Kruskal) 알고리즘은 **최소 신장 트리(MST, Minimum Spanning Tree)**를 찾는 알고리즘이다. 신장 트리 = 그래프의 모든 정점을 연결하는 사이클 없는 부분 그래프. 그중 **간선 가중치 합이 최소**인 것이 MST.

## 특징

| 항목 | 내용 |
|------|------|
| **그래프 유형** | 무방향 가중치 그래프 |
| **알고리즘 패턴** | 탐욕적 (Greedy) + 간선 중심 |
| **사이클 탐지** | **유니온-파인드 (Union-Find)** |
| **시간 복잡도** | **O(E log E)** (정렬이 병목) |
| **적합한 그래프** | 희소 그래프 (Sparse) |

---

# 2. 알고리즘 순서

1. **모든 간선을 가중치 오름차순으로 정렬**
2. 정렬된 간선을 순서대로 선택
   - 선택한 간선이 **사이클을 형성하지 않으면** MST에 추가
   - 사이클 여부는 **유니온-파인드**로 확인
3. 간선 수가 **N-1개**가 될 때까지 반복

---

# 3. 의사코드

```plaintext
function Kruskal(graph):
    MST = []
    edges = sorted(graph.edges, by weight ascending)
    disjointSet = DisjointSet(graph.nodes)

    for (u, v, weight) in edges:
        if disjointSet.find(u) != disjointSet.find(v):  // 사이클 없음
            disjointSet.union(u, v)
            MST.add((u, v, weight))

    return MST
```

---

# 4. 유니온-파인드 (Union-Find)

크루스칼의 핵심 — 두 노드가 같은 집합(컴포넌트)인지 확인.

- **find(u)**: u의 루트를 반환 (경로 압축 최적화)
- **union(u, v)**: 두 집합을 병합 (랭크 기반 최적화)
- 같은 루트 → 간선 추가 시 사이클 발생 → 건너뜀

---

# 5. 자바스크립트 구현

```javascript
class DisjointSet {
    constructor(n) {
        this.parent = Array.from({ length: n }, (_, i) => i);
        this.rank = Array(n).fill(1);
    }

    find(u) {
        if (this.parent[u] === u) return u;
        return this.parent[u] = this.find(this.parent[u]); // 경로 압축
    }

    union(u, v) {
        let rootU = this.find(u);
        let rootV = this.find(v);

        if (rootU !== rootV) {
            if (this.rank[rootU] > this.rank[rootV]) {
                this.parent[rootV] = rootU;
            } else if (this.rank[rootU] < this.rank[rootV]) {
                this.parent[rootU] = rootV;
            } else {
                this.parent[rootV] = rootU;
                this.rank[rootU] += 1;
            }
        }
    }
}

function kruskal(n, edges) {
    edges.sort((a, b) => a[2] - b[2]); // 가중치 오름차순 정렬
    const disjointSet = new DisjointSet(n);
    const mst = [];

    for (const [u, v, weight] of edges) {
        if (disjointSet.find(u) !== disjointSet.find(v)) {
            disjointSet.union(u, v);
            mst.push([u, v, weight]);
        }
    }

    return mst;
}

// 테스트
const n = 4;
const edges = [
    [0, 1, 10],
    [0, 2, 6],
    [0, 3, 5],  // ← 선택
    [1, 3, 15],
    [2, 3, 4]   // ← 선택
];

console.log(kruskal(n, edges));
// [[2, 3, 4], [0, 3, 5], [0, 2, 6]] → MST 총 비용 15
```

---

# 6. 크루스칼 vs 프림 비교

| 항목 | 크루스칼 | [[Prim]] |
|------|---------|---------|
| **접근 방식** | 간선 중심 | 정점 중심 |
| **시간 복잡도** | O(E log E) | O(E log V) |
| **적합한 그래프** | **희소 그래프** | **밀집 그래프** |
| **사이클 탐지** | Union-Find | 방문 처리 |
| **구현 복잡도** | Union-Find 필요 | 우선순위 큐 필요 |

---

## Related
- [[_MOC]]
- [[그래프]] — 크루스칼의 대상 자료구조
- [[그리디]] — 가장 작은 간선부터 선택하는 그리디 전략
- [[Prim]] — 같은 MST를 다른 방식으로 구하는 알고리즘

## Sources
- [Notion 원본](https://www.notion.so/Kruscal-44be423cbd54493abf38d106127c043d)
