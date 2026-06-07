---
title: "4. CPU Scheduling"
aliases: [CPU 스케쥴링, CPU Scheduling, 프로세스 스케쥴링]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [cs/os, status/budding]
notion-url: https://www.notion.so/bdf198e656664d5bb03fe8bb082c5e00
related:
  - "[[_MOC]]"
  - "[[3-Thread-Concurrency]]"
  - "[[2-Process-Management-Process]]"
  - "[[5-Synchronization-Tools]]"
source: ["Notion: 운영체제"]
migrated-from: "Notion: 🪞 4. Process Management - CPU Scheduling"
---

# 4. CPU Scheduling

> TL;DR: 다중 프로그래밍에서 CPU 이용률 최대화를 위한 스케쥴링 알고리즘들 - FCFS, SJF, Priority, RR, Multilevel Queue.

CPU 스케쥴링은 다중 프로그래밍(MultiProgramming)의 기본이다. 스케쥴링을 통해 CPU에서 연산되는 프로세스, 스레드를 교환하면서 컴퓨터를 보다 효율적으로 사용할 수 있다.

## 1. 기본 개념

**다중 프로그래밍(Multi-programming)**: CPU 이용률을 최대화하기 위해 다수의 프로세스를 메모리에 유지하며, CPU의 대기 시간을 최대한 없게 한다.

### A. CPU-I/O의 Burst Cycle
- 프로세스의 실행은 **CPU Burst**와 **I/O Burst**의 사이클로 이루어진다.
- CPU 스케쥴링의 성공은 프로세스들의 이런 성질에 의해 좌우된다.
- 짧게 지속되는 CPU burst의 빈도가 오래 지속되는 것보다 많다.

### B. CPU Scheduler와 Preemitive Scheduling
- CPU 스케쥴러: ready queue에 있는 프로세스 중 하나를 선택하여 CPU를 할당
- **Non-preemitive**: I/O or event wait, exit 시 프로세스가 CPU를 자발적으로 내놓는다.
- **Preemitive**: 이 이외의 경우 프로세스 실행 중 CPU 자원을 뺏어온다.

### C. Dispatcher
- 디스패처는 CPU의 제어를 스케쥴러가 선택한 프로세스에게 주는 모듈
- **Dispatch latency**: 한 프로세스가 끝나고 다음 프로세스가 실행되기 전까지 걸리는 시간
- 프로세스 실행: user mode / 스케쥴러에 의한 선택과 문맥교환: kernel mode

디스패처가 하는 일:
1. 문맥 교환 (실행 중이던 프로세스를 PCB에 저장 후 실행할 프로세스의 PCB를 메모리에서 불러옴)
2. 문맥교환 후 다시 user mode로 전환

## 2. Scheduling Criteria
- **CPU 이용률**: CPU를 최대한 바쁘게 유지
- **처리량**: 단위 시간당 완료된 프로세스의 개수
- **총 처리 시간**: 프로세스의 제출 시간과 완료 시간의 간격
- **대기 시간**: 프로세스가 준비완료 큐에서 대기하면서 보낸 시간의 합
- **응답 시간**: 사용자와의 대화식 시스템에서 짧게 짧게 반응하는 것이 중요

## 3. Scheduling Algorithm

### A. FCFS (First Come, First Served) — 선착순 실행
- CPU를 먼저 요청하는 프로세스가 할당받는 방식
- Non-preemitive 방식
- **문제**: CPU-burst가 긴 프로세스가 먼저 실행 시 다른 프로세스의 waiting 시간이 매우 길어짐 (Convoy Effect)

### B. SJF (Shortest Job First) — 작업시간 낮은 순으로 실행
- CPU burst 시간이 짧은 프로세스부터 실행
- Non-preemitive: 한 번 실행되면 끝날 때까지 인터럽트 없음
- Preemitive: 새 프로세스가 남은 시간보다 짧으면 인터럽트 발생
- **한계**: CPU burst 시간의 예측이 어렵다.

**CPU Burst 시간 예측방법**:
- **정적인 방법**: 커널 프로세스 < usermode < interactive < foreground < background
- **동적인 방법 (Exponential Averaging)**: 다음 CPU Burst의 길이가 이전 값과 비슷하다고 기대하고 근사값을 계산

### C. Priority Scheduling — 우선순위
- 각 프로세스에 우선순위를 연관하여 우선순위가 높은 순서대로 실행
- 우선순위는 내부적 기준(시간 제한, 메모리 요구, 평균 I/O burst 등)과 외부적 기준으로 정해짐
- Preemitive/Non-preemitive 모두 가능
- **문제**: Starvation — 우선순위가 낮은 프로세스가 계속 실행되지 못함
- **해결**: Aging — 시간이 지남에 따라 우선순위를 높이는 기법

### D. Round Robin Scheduling — n분 스피치
- FCFS와 비슷하지만 **Time Quantum(시간 할당량)** 이후 다음 프로세스로 문맥교환
- CPU Burst < Time Quantum: 프로세스가 자발적으로 CPU 반납
- CPU Burst > Time Quantum: 인터럽트 발생, 프로세스는 준비완료 큐 꼬리에 삽입
- **Time Quantum 크기 영향**:
  - 크면: FCFS와 차이 없음
  - 작으면: 잦은 문맥교환으로 많은 오버헤드 발생

### E. Multilevel Queue Scheduling (다단계 큐 스케쥴링)
- 프로세스별 특징에 따라 다른 그룹으로 분류
- 준비완료 큐를 여러 큐로 만들어 각 큐마다 우선순위 설정
- 프로세스 특성에 따라 하나의 큐에 **영구적으로** 할당
- 큐 우선순위: 시스템 프로세스 > 대화형 프로세스 > 대화형 편집 > 일괄처리 > 학생 프로세스

### F. Multilevel Feedback Queue Scheduling
- 다단계 큐와 달리 프로세스가 큐들 사이를 이동하는 것을 허용
- 낮은 우선순위 큐에서 오래 대기하는 프로세스는 특정 시간 후 높은 우선순위 큐로 이동
- CPU burst 시간이 주어진 시간 할당량 안에 끝나지 않으면 낮은 우선순위 큐의 꼬리로 이동

## 4. Thread Scheduling
- 사용자 수준 스레드: 스레드 라이브러리에 의해 관리 (커널은 모름)
- 커널 수준 스레드: CPU 상에서 실행되기 위해 커널 수준 스레드에 mapping 필요
- **PCS(프로세스 경쟁 범위)**: 동일한 프로세스에 속한 스레드들 사이에서 CPU 경쟁
- **SCS(시스템 경쟁 범위)**: 시스템 상의 모든 스레드 사이에서 CPU 경쟁

## Related
- [[_MOC]]
- [[3-Thread-Concurrency]]
- [[2-Process-Management-Process]]
- [[5-Synchronization-Tools]]

## Sources
- Notion: 운영체제 — https://www.notion.so/bdf198e656664d5bb03fe8bb082c5e00
