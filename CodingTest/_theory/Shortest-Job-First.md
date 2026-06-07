---
title: Shortest Job First
aliases: [SJF, shortest job first, 최단 작업 우선, SRTF]
type: concept
status: budding
created: 2026-05-23
updated: 2026-05-24
tags: [cs/algorithm, codingtest, status/budding, 우선순위큐, 스케쥴링, 그리디]
notion-url: https://www.notion.so/Shortest-Job-First-12635c502383804f83d7cba0ac1ee12a
related:
  - "[[_MOC]]"
  - "[[힙으로-우선순위-큐]]"
  - "[[스케쥴링]]"
  - "[[그리디]]"
source: ["Notion: 코딩 테스트 알고리즘 이론"]
migrated-from: "Notion: Shortest Job First"
---

# 🕐 Shortest Job First (SJF)

> TL;DR: 실행 시간이 **가장 짧은 작업을 먼저** 처리하는 CPU 스케쥴링 정책. **평균 대기 시간 최소화** 보장. 우선순위 큐 기반. 프로그래머스 "디스크 컨트롤러" 문제의 핵심 알고리즘.

---

# 1. 정의

SJF(Shortest Job First)는 작업 스케쥴링에서 **실행 시간이 짧은 작업을 먼저 처리**하여 전체 평균 대기 시간을 최소화하는 알고리즘이다.

## 특징

| 항목 | 내용 |
|------|------|
| **알고리즘 패턴** | 그리디 (Greedy) |
| **자료구조** | 우선순위 큐 (최소 힙) |
| **장점** | **평균 대기 시간 최소화** |
| **단점** | 기아 문제(Starvation), 실행 시간 사전 파악 필요 |

---

# 2. 두 가지 방식

| 방식 | 설명 | 특징 |
|------|------|------|
| **비선점형 (Non-preemptive)** | 실행 중인 작업은 끝까지 실행 | 구현 단순 |
| **선점형 (Preemptive / SRTF)** | 더 짧은 작업 도착 시 현재 작업 중단 | 평균 대기 시간 더 짧음 |

코딩 테스트에서는 주로 **비선점형** SJF 구현.

---

# 3. 알고리즘 단계 (비선점형)

1. 요청 시간 순으로 jobs 정렬
2. 현재 시간(`currentTime`)까지 도착한 모든 작업을 우선순위 큐에 추가
3. 큐에서 **실행 시간이 가장 짧은** 작업 추출 → 처리
4. 대기 시간 누적: (처리 완료 시간 - 요청 시간)
5. 큐가 빌 때까지 반복 → 평균 반환

---

# 4. 자바스크립트 구현 (프로그래머스 디스크 컨트롤러)

```javascript
function solution(jobs) {
    let answer = 0;
    let currentTime = 0;
    let sumWorkTime = 0;
    const jobCount = jobs.length;

    // 요청 시간 오름차순 정렬
    jobs.sort((a, b) => a[0] - b[0]);

    // 우선순위 큐 역할 (실행 시간 기준 최소값 우선)
    let pq = [];
    let jobIndex = 0;

    while (pq.length > 0 || jobIndex < jobCount) {
        // 현재 시간까지 도착한 작업을 모두 큐에 추가
        while (jobIndex < jobCount && jobs[jobIndex][0] <= currentTime) {
            pq.push(jobs[jobIndex]);
            jobIndex++;
        }

        // 실행 시간 기준 오름차순 정렬 (가장 짧은 작업 먼저)
        pq.sort((a, b) => a[1] - b[1]);

        if (pq.length > 0) {
            const [requestTime, workTime] = pq.shift();
            currentTime += workTime;
            sumWorkTime += currentTime - requestTime; // 대기 시간 = 완료 시간 - 요청 시간
        } else {
            // 큐가 비어있으면 다음 작업 요청 시간으로 점프
            currentTime = jobs[jobIndex][0];
        }
    }

    answer = Math.floor(sumWorkTime / jobCount);
    return answer;
}

// 사용 예시
// jobs: [요청시간, 처리시간]
console.log(solution([[0, 3], [1, 9], [2, 6]])); // 9
// → 작업 처리 순서: [0,3] → [2,6] → [1,9]
// → 대기 시간: (3-0) + (9-2) + (18-1) = 3+7+17 = 27 → 평균 9
```

---

# 5. 힙 기반 최적화 구현

위 구현은 매번 `sort()`를 호출해 O(k log k). 실제 최소 힙을 쓰면 삽입/추출 O(log k).

```javascript
class MinHeap {
    constructor() { this.heap = []; }

    insert(job) {
        this.heap.push(job);
        this._bubbleUp();
    }

    extractMin() {
        const min = this.heap[0];
        const last = this.heap.pop();
        if (this.heap.length > 0) {
            this.heap[0] = last;
            this._sinkDown();
        }
        return min;
    }

    _bubbleUp() {
        let i = this.heap.length - 1;
        while (i > 0) {
            const parent = Math.floor((i - 1) / 2);
            if (this.heap[parent][1] <= this.heap[i][1]) break;
            [this.heap[parent], this.heap[i]] = [this.heap[i], this.heap[parent]];
            i = parent;
        }
    }

    _sinkDown() {
        let i = 0;
        while (true) {
            let smallest = i;
            const left = 2 * i + 1, right = 2 * i + 2;
            if (left < this.heap.length && this.heap[left][1] < this.heap[smallest][1]) smallest = left;
            if (right < this.heap.length && this.heap[right][1] < this.heap[smallest][1]) smallest = right;
            if (smallest === i) break;
            [this.heap[i], this.heap[smallest]] = [this.heap[smallest], this.heap[i]];
            i = smallest;
        }
    }

    isEmpty() { return this.heap.length === 0; }
}
```

---

# 6. 복잡도

| 구현 | 시간 복잡도 |
|------|-----------|
| 배열 sort 방식 | O(n² log n) 최악 |
| **MinHeap 방식** | **O(n log n)** |

---

## Related
- [[_MOC]]
- [[힙으로-우선순위-큐]] — SJF는 최소 힙으로 가장 짧은 작업 추출
- [[스케쥴링]] — SJF는 스케쥴링 전략의 한 종류
- [[그리디]] — 매 순간 가장 짧은 작업 선택하는 그리디 전략

## Sources
- [Notion 원본](https://www.notion.so/Shortest-Job-First-12635c502383804f83d7cba0ac1ee12a)
