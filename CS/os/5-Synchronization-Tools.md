---
title: "5. Synchronization Tools"
aliases: [동기화 도구, Synchronization, 임계 구역, Critical Section]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [cs/os, status/budding]
notion-url: https://www.notion.so/230bd6bed4e848b48daa4571713689c0
related:
  - "[[_MOC]]"
  - "[[4-CPU-Scheduling]]"
  - "[[6-Synchronization-Examples]]"
  - "[[7-Deadlocks]]"
source: ["Notion: 운영체제"]
migrated-from: "Notion: 🖨️ 5. Process Management - Synchronization Tools"
---

# 5. Synchronization Tools

> TL;DR: Race Condition 해결을 위한 임계 구역 3가지 조건(상호배제·진행·Bound Waiting)과 Peterson's, Mutex Locks, Semaphore 구현법.

협력적 프로세스에서 Shared Memory로의 동시 접근은 데이터의 비일관성을 낳을 수 있다.

## 1. 배경

### A. Critical Section (임계 구역)
- **Race Condition**: 두 개의 프로세스가 동시에 특정 데이터를 변경할 경우, 실행 결과가 접근 순서에 따라 달라지는 상황
- **Critical Section**: 한 프로세스가 자신의 임계구역에서 수행하는 동안 다른 프로세스들은 자신의 임계구역에 들어갈 수 없다.

임계 구역은 다음 **세 가지 조건**을 충족해야 한다:

| 조건 | 설명 |
|------|------|
| **상호 배제** | 프로세스 A가 임계구역에서 실행 중이면 프로세스 B는 진입 불가 |
| **진행 (Progress)** | 임계구역 진입 요청 후 무기한 대기하지 않도록 한다 |
| **Bound Waiting** | 진입 요청 후 허용될 때까지 다른 프로세스들이 진입할 수 있는 횟수에 한계가 있어야 함 |

- Non-preemitive 커널: Race Condition 발생하지 않음
- Preemitive 커널: Race Condition 발생 가능

## 2. Peterson's Solution
- 상호배제, 진행, 한정된 대기를 위한 소프트웨어 기반 알고리즘 (프로세스 2개인 경우에만 가능)

```javascript
bool flag[]; // 임계영역 진입 상태 저장
int turn;    // 임계구역을 실행할 프로세스의 순서

while(true) {
    flag[i] = true;  // 해당 번호의 프로세스가 임계구역 진입 준비 완료
    turn = j;        // 임계구역에 진입할 차례의 프로세스 번호

    while(flag[j] && turn == j); // 다른 프로세스가 임계구역에서 나오기 전까지 spinlock

    /* critical section */

    flag[i] = false; // 다음 프로세스가 임계구역에 들어갈 수 있게 false로 변경

    /* remainder section */
}
```

## 3. Synchronize Hardware
- SW 기반 해결책은 현대의 컴퓨터에서 제대로 동작하지 않을 수 있으므로 하드웨어 기반 해결책 사용
- 모든 해결책은 **Locking(임계구역 문제에 락 사용)**에 기반

### A. test_and_set()
```javascript
boolean test_and_set(boolean *target) {
    boolean rv = *target;
    *target = true;  // 항상 true로 set
    return rv;       // 입력값 그대로 반환
}

do {
    while(test_and_set(&lock)); // lock이 false일 때만 진입

    /* critical section */

    lock = false;

    /* remainder section */
} while(true);
```
- **Mutual Exclusive는 만족**, but Progress와 Bounded Waiting은 불만족 (FCFS 처리방식)

### B. compare_and_swap()
```javascript
int compare_and_swap(int *value, int expected, int newvalue) {
    int temp = *value;
    if(expected == *value)
        *value = newvalue;
    return temp;
}

do {
    while(compare_and_swap(&lock, 0, 1) != 0);

    // critical section

    lock = 0;

    // remainder section
} while(true);
```
- **Mutual Exclusive는 만족**, but Progress와 Bounded Waiting은 불만족

## 4. Mutex Locks
- OS 설계자들이 임계구역 문제를 해결하고자 만든 소프트웨어 툴 (Mutual exclusion의 축약)

```javascript
acquire() {
    while(!available); // busywaiting (spinlock)
    available = false;
}

release() {
    available = true;
}
```
- `available` 변수로 락의 가용성 관리
- `acquire()` → critical section → `release()` 순서로 사용

## 5. Semaphore
- mutex와 비슷하지만 프로세스들이 더 정교하게 동기화할 수 있는 도구
- `wait()`와 `signal()`로만 접근 가능

```javascript
wait(S) {         // S가 1 이상이면 임계 영역 진입, S 값 감소
    while(S <= 0); // busy-waiting
    S--;
}

signal(S) {       // 임계 영역 사용 후 반환, S 값 증가
    S++;
}
```

- `wait()`와 `signal()`의 연산은 **atomic**하게 진행된다.

### A. 세마포 사용법

| 종류 | 설명 |
|------|------|
| **이진 세마포 (Binary)** | 세마포의 값이 0과 1 사이의 값만 가능 |
| **카운팅 세마포 (Counting)** | 가용한 자원의 갯수를 세마포로 하여 wait 시 -1, signal 시 +1 |

- 두 방식 다 세마포의 값이 0이면 가용가능한 자원 없음

## Related
- [[_MOC]]
- [[4-CPU-Scheduling]]
- [[6-Synchronization-Examples]]
- [[7-Deadlocks]]

## Sources
- Notion: 운영체제 — https://www.notion.so/230bd6bed4e848b48daa4571713689c0
