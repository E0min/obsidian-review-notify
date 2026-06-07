---
title: OS (Operating Systems) MOC
aliases: [운영체제 MOC, OS Map of Contents]
type: moc
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [cs/os, type/moc, status/budding]
related:
  - "[[../CS/_MOC]]"
source: ["Notion: 운영체제"]
migrated-from: "Notion: ♦️ 운영체제 데이터베이스"
---

# 운영체제 (Operating Systems) MOC

> TL;DR: 운영체제 0~13장 전체 노트. 프로세스/스레드/동기화/메모리/파일시스템까지 핵심 CS 이론.

Notion 원본: https://www.notion.so/594e15da9cfb41338c702a79f4bad47d

---

## 목차

### Part 1 — 기초 & 구조
- [[0-Introduction]] — 운영체제 개요, 폰노이만 구조, 부팅, 인터럽트
- [[1-Operating-System-Structures]] — OS 서비스, 시스템 콜, API, OS 구조

### Part 2 — 프로세스 관리
- [[2-Process-Management-Process]] — 프로세스 개념, PCB, 문맥교환, IPC
- [[3-Thread-Concurrency]] — 스레드, 다중코어 프로그래밍, 다중 스레드 모델
- [[4-CPU-Scheduling]] — 스케쥴링 알고리즘 (FCFS, SJF, Priority, RR, Multilevel Queue)

### Part 3 — 동기화 & 교착상태
- [[5-Synchronization-Tools]] — Race Condition, Critical Section, Mutex, Semaphore
- [[6-Synchronization-Examples]] — Bounded Buffer, Readers-Writers, Dining Philosophers
- [[7-Deadlocks]] — 교착상태 4가지 조건, 예방/회피(은행원 알고리즘)/탐지/무시

### Part 4 — 메모리 관리
- [[8-Memory-Management]] — Address Binding, MMU, Paging, TLB, Segmentation
- [[9-Virtual-Memory]] — 가상 메모리, Demand Paging, Page Fault, 페이지 교체 알고리즘, Thrashing

### Part 5 — 저장장치 & 파일 시스템
- [[10-Mass-Storage-Structure]] — HDD 구조, 디스크 스케쥴링, RAID
- [[11-IO-Systems]] — I/O 하드웨어, Polling/Interrupt/DMA, Blocking/Non-blocking/Sync/Async
- [[12-File-System-Interface]] — 파일 개념, 접근 방식, 디렉터리 구조, 마운팅, 보호
- [[13-File-System-Implementation]] — 계층적 구조, FCB/inode, 할당 방법, 자유공간 관리

---

## 핵심 개념 빠른 참조

| 개념 | 파일 |
|------|------|
| 프로세스 상태 (new/ready/waiting/running/terminated) | [[2-Process-Management-Process]] |
| 문맥교환 (Context Switching) | [[2-Process-Management-Process]] |
| Race Condition & Critical Section | [[5-Synchronization-Tools]] |
| 은행원 알고리즘 (Deadlock Avoidance) | [[7-Deadlocks]] |
| TLB (Translation Look-aside Buffer) | [[8-Memory-Management]] |
| Page Fault 처리 과정 | [[9-Virtual-Memory]] |
| Thrashing & Working Set | [[9-Virtual-Memory]] |
| RAID | [[10-Mass-Storage-Structure]] |

---

## Related
- [[../CS/_MOC]] — CS 전체 목차
- [[../../CodingTest/_MOC]] — 코딩 테스트

## Sources
- [Notion 원본 DB](https://www.notion.so/594e15da9cfb41338c702a79f4bad47d)
