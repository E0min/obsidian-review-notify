---
title: "11. I/O Systems"
aliases: [입출력 시스템, I/O, 인터럽트, DMA]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [cs/os, status/budding]
notion-url: https://www.notion.so/9c56058085ee4012abb8a2a73e41c774
related:
  - "[[_MOC]]"
  - "[[10-Mass-Storage-Structure]]"
  - "[[12-File-System-Interface]]"
source: ["Notion: 운영체제"]
migrated-from: "Notion: 📒 11. Storage Management - I/O Systems"
---

# 11. I/O Systems

> TL;DR: 컴퓨터 I/O 하드웨어(Polling/Interrupt/DMA), 블로킹·논블로킹·동기·비동기 I/O 모델, 커널 I/O 서브시스템(버퍼링/캐싱/스풀링).

컴퓨터의 두 가지 주요 작업은 **연산처리작업(processing)**과 **입출력 작업(I/O)**이다.

---

## 1. Overview
- 입출력 장치는 갈수록 다양해지지만, 관련 인터페이스는 점점 표준화되어 가고 있다.
- **Device Driver(SW)**: 모든 하드웨어를 **일관된 인터페이스**로 표현하며 이 인터페이스를 커널의 입출력 서브시스템에게 제공

---

## 2. I/O Hardware

- **Port**: 입출력 장치들이 컴퓨터에 접속되는 연결점
- **Bus**: 하나 이상의 장치들이 공동으로 사용하는 회선의 집합 + 프로토콜
- **Device Controller(HW)**: 포트나 버스나 입출력 장치들을 제어하는 전자 회로의 집합체
- **Device Driver**: 다양한 하드웨어를 일관된 인터페이스로 표현해 Device Controller와 Device 간의 차이를 숨겨줌

Device Controller의 레지스터:
- **상태 레지스터**: 하드웨어 장치의 현재 상태를 읽음
- **명령 레지스터**: 하드웨어 장치가 특정 동작을 하도록 요청
- **데이터 레지스터**: 하드웨어 장치에 데이터를 보내거나 받음

### A. Polling (Busy-Waiting)
- Device Controller는 자신의 상태를 상태 레지스터에 기록
- 바쁠 때는 busybit를 설정, 준비되면 busybit를 소거
- 호스트는 busybit가 사라질 때까지 반복적으로 상태 비트를 확인

### B. Interrupt
- 장치가 준비되었을 때 알려주는 것이 polling보다 효율적
- CPU와 Device들을 연결하는 Bus에 **Interrupt-request line**이 따로 있음
- Device Controller가 이 request line으로 interrupt 요청을 보냄
- CPU가 인터럽트를 알아차리고 **ISR(Interrupt Service Routine)** 실행
- **인터럽트 벡터**: 여러 요청에 대한 Interrupt handler들의 메모리 주소를 가짐

ISR 실행 과정:
1. CPU의 각종 레지스터, Program counter 등을 저장
2. 인터럽트 요청에 대한 적절한 Interrupt Handler를 찾아 요청 수행
3. 수행 후 저장했던 정보들을 불러와 CPU 상태 복구

### C. DMA (Direct Memory Access)
- CPU가 데이터의 I/O를 반복적으로 요청하는 것은 낭비 → DMA라는 특수 프로세서에게 위임
- 호스트는 메모리에 **DMA 명령 블록** (전송할 주소, 전송받을 주소, 전송할 비트수)를 쓰고 DMA에게 알려줌
- DMA는 CPU의 도움 없이 직접 I/O를 수행
- 메모리 Bus 사용 시 충돌이 일어날 수 있음 → DMA가 우선

---

## 3. Application I/O Interface
- 추상화와 캡슐화, 계층화를 통해 모든 입출력 장치들이 일관된 방법으로 다루어질 수 있는 인터페이스를 구성
- **장치 드라이버층**: 여러 I/O Device 간의 차이를 숨겨서 표준 인터페이스로 보이도록 함

---

## 4. I/O Models

### A. Blocking I/O vs Non-blocking I/O (호출하는 함수에 대한 리턴)

| 모델 | 설명 |
|------|------|
| **Blocking I/O** | Kernel에 I/O call을 보내고 작업이 끝날 때까지 기다림. 즉시 완료 불가 시 봉쇄 상태로 진입 |
| **Non-blocking I/O** | Kernel에 I/O call을 보내고 즉시 리턴 (데이터 없거나/조금있거나/완료). 다른 프로세스를 수행하면서 중간중간 작업 완료를 확인 |

### B. Synchronous vs Asynchronous (작업 완료에 대한 관심 주체)

| 모델 | 설명 |
|------|------|
| **Synchronous** | User에서 호출한 함수의 작업 완료 여부를 반복해서 Kernel에 물어봄. 순서에 맞춰 진행 |
| **Asynchronous** | 태스크가 순서에 맞추어 일어나지 않음. Kernel에 callback을 추가하여 완료 여부를 알려줌 |

예시:
- Synchronous: 건물은 1층부터 N층까지 순서대로 지어야 한다.
- Asynchronous: 방은 1호부터 n호까지 순서대로 지을 필요가 없다.

---

## 5. Kernel I/O Subsystem

### A. I/O Scheduling
- I/O를 실행할 순서를 결정
- 시스템의 효율 향상 / 공정한 접근 / 대기시간 줄이기

### B. Buffering
버퍼링의 이유:
- 생산자와 소비자의 속도차이 (이중 버퍼: 동시에 쓰고/읽는 과정이 일어날 경우를 위해)
- 데이터 전송 크기가 다른 경우의 완충
- 응용 프로그램 I/O의 Semantic: System call 시점의 Application Buffer 내용이 Kernel Buffer로 복사

### C. I/O Protection
- User(Application)은 I/O Device에 대한 입출력 명령을 직접 못함
- I/O Device 명령은 System call → Kernel 영역 → 인터럽트 벡터에 기록하며 실행
- Kernel mode와 User Mode

---

## Related
- [[_MOC]] — 운영체제 MOC
- [[10-Mass-Storage-Structure]] — 대용량 저장 장치
- [[12-File-System-Interface]] — 파일 시스템 인터페이스

## Sources
- [Notion 원본](https://www.notion.so/9c56058085ee4012abb8a2a73e41c774)
