---
title: "6. Synchronization Examples"
aliases: [동기화 예제, Synchronization Examples, 고전적 동기화 문제]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [cs/os, status/budding]
notion-url: https://www.notion.so/f957048dee954aef85b5dad172d43bc3
related:
  - "[[_MOC]]"
  - "[[5-Synchronization-Tools]]"
  - "[[7-Deadlocks]]"
source: ["Notion: 운영체제"]
migrated-from: "Notion: 👒 6. Process Management - Synchronization Examples"
---

# 6. Synchronization Examples

> TL;DR: 고전적 동기화 문제 3가지 — Bounded Buffer(생산자-소비자), Readers-Writers, Dining Philosophers.

동기화의 클래식한 문제들을 살펴본다.

## 1. Bounded-Buffer Problem (유한 버퍼 문제)

n개의 버퍼 공간이 존재할 때:
- 세마포의 `mutex` = 1
- 세마포 `full` = 0 (채워진 버퍼 수)
- 세마포 `empty` = n (빈 버퍼 수)

**생산자 프로세스의 구조**:
```javascript
while(true) {
    wait(empty);  // 버퍼가 비어있는지 확인
    wait(mutex);

    /* 버퍼에 생산한 것을 넣는다 */

    signal(mutex);
    signal(full);
}
```

**소비자 프로세스의 구조**:
```javascript
while(true) {
    wait(full);   // 버퍼가 채워져 있는지 확인
    wait(mutex);

    /* 버퍼에 있는 것 소비 */

    signal(mutex);
    signal(empty);
}
```

## 2. Readers-Writers Problem

- 하나의 데이터베이스를 병행적으로 실행되는 다수의 프로세스가 공유
- **Reader**: 데이터를 읽기만 하므로 동시에 여러 명이 읽어도 됨
- **Writer**: 동시에 여러 명이 쓴다면 문제 발생 → **Mutual Exclusive하게 접근 필요**

**Writer 프로세스의 구조**:
```javascript
while(true) {
    wait(rw_mutex); // rw_mutex는 1로 initialized

    /* writing is performed */

    signal(rw_mutex);
}
```

**Reader 프로세스의 구조**:
```javascript
while(true) {
    wait(mutex);         // mutex, rw_mutex는 1로 초기화
    read_count++;        // read_count는 0으로 초기화
    if(read_count == 1)
        wait(rw_mutex);  // 첫 번째 reader가 writer 차단
    signal(mutex);

    /* reading is performed */

    wait(mutex);
    read_count--;
    if(read_count == 0)
        signal(rw_mutex); // 마지막 reader가 writer 허용
    signal(mutex);
}
```

## 3. Dining-Philosophers Problem (식사하는 철학자들 문제)

- 5명의 철학자가 원형 테이블에 앉아 있음
- 철학자는 밥을 먹기 위해 양쪽에 있는 젓가락을 하나씩 사용해야 함
- 동시에 배고파진 철학자들이 자신의 왼쪽 젓가락을 집으면 → 아무도 식사 진행 불가

**교착상태 해결 방법**:
1. 최대 4명만 앉게 한다.
2. 한 철학자가 두 개를 동시에 집을 수 있을 때만 젓가락을 집을 수 있게 한다.
3. 홀수 번호의 철학자는 왼쪽, 짝수 번호의 철학자는 오른쪽의 젓가락을 먼저 집게 한다.

> **주의**: 교착상태가 해결된다는 것이 **기아(Starvation)를 방지하지는 않는다.**

이 문제는 병행 실행 시 **교착상태와 기아**를 발생시키지 않고 여러 스레드/프로세스에게 여러 자원을 할당해야 할 필요를 단순히 표현한 것이다.

## Related
- [[_MOC]]
- [[5-Synchronization-Tools]]
- [[7-Deadlocks]]

## Sources
- Notion: 운영체제 — https://www.notion.so/f957048dee954aef85b5dad172d43bc3
