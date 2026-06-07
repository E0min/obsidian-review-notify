---
title: "10. Mass-Storage Structure"
aliases: [대용량 저장 장치, Mass Storage, HDD 스케쥴링, RAID]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [cs/os, status/budding]
notion-url: https://www.notion.so/b0be4e7e1902460d8633da5f02478d16
related:
  - "[[_MOC]]"
  - "[[9-Virtual-Memory]]"
  - "[[11-IO-Systems]]"
  - "[[12-File-System-Interface]]"
source: ["Notion: 운영체제"]
migrated-from: "Notion: 🎨 10. Storage Management - Mass-Storage Structure"
---

# 10. Mass-Storage Structure

> TL;DR: 비휘발성 보조기억장치(HDD) 구조와 스케쥴링 알고리즘(FIFO/SSTF/SCAN/C-SCAN/LOOK), RAID 중복성과 병렬성.

비휘발성이고 컴퓨터의 보조기억장치로 사용. 주로 HDD를 예시로 들 수 있다.

---

## 1. 대용량 저장 장치

### A. 하드 디스크 구조
- **Platter** = track × ... × track (Track 50K~100K개 = 12.5~100GB)
- **Track** = sector × ... × sector (Sector 500~2000개 = 256KB~1MB)
- **Sector** = 512 bytes
- **Head**: 데이터를 자기적으로 읽거나 쓰는 장치

### B. 하드디스크 스케쥴링

용어:
- **Seektime**: 디스크 암이 헤드를 원하는 실린더로 옮기는데 필요한 시간
- **Rotational time**: 디스크 헤드가 원하는 섹터 위치로 도달하기까지 회전에 소요되는 시간
- **Band width**: 단위시간당 전송되는 데이터 수

HDD 스케쥴링 목표: 데이터 섹터에 access 하는 데 걸리는 시간(seek + rotational)을 줄이고 bandwidth를 늘려야 한다.

**스케쥴링 알고리즘**:

| 알고리즘 | 설명 |
|---------|------|
| **FIFO** | 먼저 들어온 요청 수행 |
| **SSTF** | 근처에 있는 요청부터 수행 |
| **SCAN** | 디스크 암이 한 끝에서 시작하여 다른 끝으로 이동하며 가는 길에 있는 요청을 모두 처리 |
| **C-SCAN** | SCAN 방식을 양방향 모두 수행 |
| **LOOK** | C-SCAN 변형. 각 방향으로 가다가 요청이 없으면 헤드의 이동방향을 반대로 전환 |

---

## 2. RAID 구조

**RAID (Redundant Arrays of Independent Disks)**:
- 많은 수의 디스크를 병렬적으로 운영하여 데이터 읽기/쓰기 속도를 높임
- 중복 정보를 여러 디스크에 저장하여 데이터 저장의 신뢰성 향상

### A. 중복을 통한 신뢰성 향상 (Redundancy)
- **미러링(Mirroring)**: 모든 디스크의 복사본을 만드는 것. 하나의 논리 디스크 = 두 개의 물리 디스크
- 비휘발성 메모리 캐시를 RAID 배열에 두는 방식도 있음

### B. 병렬성을 이용한 성능 향상
- **데이터 스트라이핑**: 여러 디스크에 각 바이트를 나누어 저장
- 예: 8개의 디스크에 데이터를 8개로 나누어 병렬적으로 읽으면 8배 빠름

### C. RAID 레벨
- 미러링에 패리티 비트와 스트라이핑을 통해 구현한 기법들
- RAID 레벨: 0, 1, 2, 3, 4, 5, 6, 0+1 등 존재

---

## Related
- [[_MOC]] — 운영체제 MOC
- [[9-Virtual-Memory]] — 가상 메모리
- [[11-IO-Systems]] — I/O 시스템
- [[12-File-System-Interface]] — 파일 시스템 인터페이스

## Sources
- [Notion 원본](https://www.notion.so/b0be4e7e1902460d8633da5f02478d16)
