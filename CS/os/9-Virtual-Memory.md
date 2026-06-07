---
title: "9. Virtual Memory"
aliases: [가상 메모리, Virtual Memory, 요구 페이징, Demand Paging]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [cs/os, status/budding]
notion-url: https://www.notion.so/d75ee837abd0446abb8eea6c642cbb2b
related:
  - "[[_MOC]]"
  - "[[8-Memory-Management]]"
  - "[[10-Mass-Storage-Structure]]"
source: ["Notion: 운영체제"]
migrated-from: "Notion: 🧯 9. Memory Management - Virtual Memory"
---

> [!tldr] TL;DR
> 가상 메모리 - 프로세스 전체가 메모리에 올라오지 않아도 실행 가능. Demand Paging, Page Fault 처리, 페이지 교체 알고리즘(FIFO/Optimal/LRU), Thrashing 방지.

가상 메모리는 프로세스 전체가 메모리 내에 올라오지 않더라도 실행이 가능하도록 하는 기법이다.

## 1. Background

- 프로그램에서는 거의 실행되지 않는 부분도 있고, 모든 부분을 동시에 요구하는 경우는 거의 없다.
- 프로그램을 메모리에 **부분적으로 load**하는 이점:
  - 프로그램은 Physical Memory의 크기에 제한받지 않음
  - 각 프로그램의 Memory 사용량이 줄어들면서 CPU 이용률과 처리율 향상
- 가상 메모리: **Logical Memory와 Physical Memory를 분리**하여 필요한 부분만 Physical Memory에 적재

## 2. Demand Paging

- 페이지들이 실행 과정에서 실제로 필요해질 때 적재됨
- **Demand Paging**: 요구되는 page만 관리
- **Swapping**: 전체 프로세스를 페이징

### A. Basic Concept

- pager: 프로세스 전체를 swap-in하는 대신 실제 필요한 page들만 메모리로 읽어옴
- **valid bit**: 해당 page가 메모리에 적재되어 있음
- **invalid bit**: 해당 page가 유효하지 않거나, 유효하지만 디스크에 있음

### B. Page Fault

- 메모리에 없는 페이지를 접근하려고 하면 Page Fault Trap 발생

Page Fault 처리 과정:
1. 내부 테이블(PCB)을 검사하여 메모리 참조가 valid/invalid인지 확인 (User mode)
2. invalid 참조면 프로세스 중단, valid이지만 메모리에 없으면 디스크에서 가져옴 (Kernel mode)
3. 빈 자유 프레임을 찾음 (Kernel mode)
4. 디스크에서 새로 할당된 frame으로 해당 page를 읽어들임 (Kernel mode)
5. 페이지 테이블을 갱신 (valid bit 설정) (Kernel mode)
6. 중단되었던 명령어를 다시 수행 (User mode)

- **순수 요구 페이징**: 모든 Page가 적재되어 더이상 fault가 발생하지 않을 때까지 반복
- 프로그램들은 **참조의 지역성** 성질을 가져 요구 페이징은 만족할만한 성적을 냄

## 3. Page Replacement

빈 프레임이 없을 때 현재 사용되지 않는 프레임을 찾아서 비우고 새로운 페이지를 할당

Page Replacement 과정:
1. 디스크에서 필요한 페이지의 위치 확인
2. 빈 페이지 프레임 찾기 (없으면 페이지 교체 알고리즘으로 희생 프레임 선정)
3. 빼앗은 프레임에 새 프레임을 읽어오고 테이블 수정
4. Page Fault가 발생한 지점에서부터 계속 진행

**변경 비트(Dirty bit)**: CPU가 Page에 write했다면 내용이 바뀐 것이므로 디스크에 다시 저장 필요. 바뀌지 않았다면 디스크에 다시 저장할 필요 없음 → 오버헤드 감소

### B. FIFO Page Replacement

- 메모리에 가장 오래 있던 Page가 교체됨

### C. Optimal Page Replacement

- 앞으로 **가장 오랫동안 사용되지 않을 Page**를 교체
- 미래를 알아야 하므로 실제로 사용하기 어렵다

### D. LRU Page Replacement

- **가장 오랫동안 사용되지 않은 Page**를 교체
- Counter 구현: Page가 reference될 때마다 계수기나 시간을 기록
- Stack 구현: Page reference 시 그 페이지 번호를 stack의 top에 넣음. bottom에 가장 오랫동안 사용되지 않은 페이지가 위치

### E. LRU Approximation (근사 알고리즘)

참조 비트를 이용한 형태:

| 알고리즘 | 설명 |
|---------|------|
| **Additional-Reference Bits** | 8-bit shift register로 참조를 기록. 8bit 값이 가장 작은 페이지가 LRU |
| **Second-Chance** | FIFO 기반. 참조 비트가 1이면 0으로 수정 후 다음으로, 0이면 교체 |
| **Enhanced Second-Chance** | (Reference bit, Modify bit) 쌍으로 4가지 등급으로 분류 |

### F. Counting-Based Page Replacement

- **LFU**: 참조 횟수가 가장 적은 Page를 교체
- **MFU**: 참조 횟수가 가장 적은 Page가 가장 최근에 참조된 것이라는 판단

### G. Page-Buffering Algorithm

- **Keep a pool of Free-Frames**: Page Fault 발생 시 교체될 프레임 내용을 디스크에 기록하기 전에 가용 프레임 풀에서 먼저 새 Page를 읽어들임
- **Keep a list of Modified Pages**: HW가 Idle한 상태일 때 변경된 내용을 디스크에 기록하고 Modified bit를 0으로 수정

## 4. Allocation of Frames

- 너무 적은 프레임을 할당하면 Page Fault 높아져 효율적인 실행 어려움
- **균일 할당**: 모든 프로세스에게 동일한 프레임 할당 → 비효율적
- **비례 할당**: 프로세스의 크기 비율에 맞추어 할당
- 우선순위와 프로세스 크기를 조합한 할당도 사용

### A. Global vs Local Allocation

| 방법 | 설명 |
|------|------|
| **Global Allocation** | 모든 프레임을 대상으로 교체. 우선순위 높은 프로세스가 낮은 프로세스 희생 가능 |
| **Local Allocation** | 각 프로세스가 자신에게 할당된 프레임 중에서만 교체 |

## 5. Thrashing

- 프로세스가 실행하기에 충분한 프레임을 할당받지 못한 경우 반복적으로 Page Fault 발생
- **Thrashing**: 과도한 Paging 작업으로 실제 프로세스 execute 시간보다 Paging에 더 많은 시간을 씀

### A. Thrashing의 원인

- 운영체제가 CPU 이용률이 내려가면 새로운 프로세스를 추가 → Page Fault 비율 증가 → CPU 이용률 더욱 하락 → 악순환

### B. Working-Set Model

- 프로세스 실행의 **지역성 모델**에 기초
- 일정 시간마다 참조한 페이지를 기록하고 최근 N만큼의 참조를 **작업 집합(Working Set)**으로 정의
- 운영체제는 작업 집합 크기에 맞는 충분한 프레임을 할당
- 새로운 지역을 참조할 때 Page Fault율 증가 → 새 지역의 작업 집합이 적재되면 감소

### C. PFF (Page Fault Frequency)

- Page Fault율의 **상한**과 **하한**을 정함
- 상한을 넘으면 프레임을 더 할당, 하한 아래로 내려가면 프레임 수를 줄임

## Related

- [[_MOC]]
- [[8-Memory-Management]]
- [[10-Mass-Storage-Structure]]

## Sources

- Notion: [9. Memory Management - Virtual Memory](https://www.notion.so/d75ee837abd0446abb8eea6c642cbb2b)
