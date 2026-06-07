---
title: "8. Memory Management"
aliases: [메모리 관리, Memory Management, 페이징, Paging]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [cs/os, status/budding]
notion-url: https://www.notion.so/93895218d7e74d4db8bb260a88701042
related:
  - "[[_MOC]]"
  - "[[7-Deadlocks]]"
  - "[[9-Virtual-Memory]]"
source: ["Notion: 운영체제"]
migrated-from: "Notion: 🚚 8. Memory Management - Memory Management"
---

> [!tldr] TL;DR
> 메모리 관리 기법들 - Address Binding, MMU, Swapping, Contiguous Allocation, Segmentation, Paging(TLB 최적화).

## 1. Background

- CPU는 Program Counter가 지시하는 대로 메모리로부터 명령어를 가져오므로 프로그램은 메모리에 적재되어야 실행 가능
- **레지스터**: 한 클록사이클로 접근 / **메모리**: 여러 클록사이클 필요 → Stall 현상 → 사이에 캐시를 두어 해결
- **Base register**: 프로세스가 메모리에 적재될 가장 낮은 주소
- **Limit register**: 논리 주소의 범위

### A. Address Binding

- **Logical address (Virtual address)**: CPU가 생성하는 주소
- **Physical address**: 메모리가 취급하는 주소

바인딩 시점에 따른 구분:

| 시점 | 설명 | 논리=물리? |
|------|------|-----------|
| **컴파일 시간 바인딩** | 컴파일 시점에 물리주소를 알면 절대 코드 생성 | 논리 = 물리 |
| **적재 시간 바인딩** | 컴파일 시 모른다면 Relocatable code로 만들고 적재 시점에 바인딩 | 논리 = 물리 |
| **실행 시간 바인딩** | 프로세스 실행 중 메모리 내에서 주소 변경 시 | 논리 ≠ 물리 |

### B. Memory Management Unit (MMU)

- run-time에 Virtual addresses를 Physical addresses에 mapping (Contiguous, Paging, Segmentation)
- base register를 relocation register라고 부르며 이 값을 통해 메모리상 프로세스의 주소를 변경

### C. Dynamic Loading

- **Static Loading**: 실행 시 모든 프로그램과 데이터가 적재
- **Dynamic Loading**: 함수가 실행되기 전까지 메모리에 적재되지 않음. 메모리 공간을 효율적으로 사용

### D. Dynamic Linking

- Link 과정이 실행 시기로 미뤄지는 것 (주로 시스템 라이브러리에 사용)
- **stub**: 라이브러리를 어떻게 찾을 것인지에 대한 코드. 실행 시 필요한 라이브러리가 메모리에 적재되어 있는지 확인 후 없으면 디스크에서 로드
- `printf()` 같은 라이브러리를 쓰는 프로세스가 10개 있어도 메모리상에 코드는 한 개만 있으면 됨

## 2. Swapping

- 프로세스가 실행 중에 임시로 예비 저장장치에 스왑되었다가 실행을 계속하기 위해 메모리로 복귀 가능
- 메모리에 공간이 없다면 현재 메모리에 있는 프로세스를 **swap-out**하고 원하는 프로세스를 불러옴

## 3. Contiguous Memory Allocation (연속 메모리 할당)

- 메모리는 OS 영역과 User 프로세스 영역으로 나뉨
- 각 프로세스는 연속된 하나의 메모리 영역을 차지

### B. Memory Allocation (Multi-partition allocation)

- 메모리의 연속적인 공간을 **Hole**이라고 부름
- 프로세스는 자신이 들어갈 수 있는 충분한 크기의 hole을 할당받고 반납

**동적 메모리 할당 문제** (어떤 hole을 선택할까?):

| 방법 | 설명 |
|------|------|
| **First-fit** | 검색해서 처음으로 나온 할당 가능한 hole을 할당 |
| **Best-fit** | 할당 가능한 hole 중 가장 작은 hole을 할당 |
| **Worst-fit** | 할당 가능한 가장 큰 hole을 할당 |

### C. Fragment (단편화)

- **외부 단편화**: 남는 자유 공간들을 모두 합치면 충분하지만 작은 조각으로 분산 → 압축 기법으로 해결 가능
- **내부 단편화**: 할당된 공간이 요구받은 공간보다 클 경우 남는 부분

### D. Segmentation

- 메모리를 사용자 관점에서 볼 수 있게 도움
- 각 Segment는 논리적인 단위 (main, function, method, variable...)
- Segment table(PCB에 저장)의 도움으로 Logical Memory에서 Physical Memory로 mapping
- Segment table: **base**(시작주소)와 **limit**(길이)로 이루어짐

## 4. Paging

- Segmentation의 외부단편화 문제와 압축을 해야 하는 문제를 해결

### A. Basic Method

- **Physical Memory**: frame이라는 같은 크기의 블록으로 나눔
- **Logical Memory**: page라는 같은 크기의 블록으로 나눔
- **page 크기 = frame 크기**
- **page table**: 각 page가 Physical Memory에 대응되는 frame 정보
- 논리주소 = **page number** + **page offset**

Paging 장단점:
- 외부단편화 없음
- 내부 단편화 발생 (frame 내부 공간 낭비)

### B. Implement of Page Table & TLB

- **PTBR(Page Table Base Register)**: 페이지 테이블을 가리키는 레지스터
- 문제: 메모리에 두 번 접근해야 함 (페이지 테이블 + 실제 데이터)
- **TLB(Translation Look-aside Buffer)**: 매우 빠른 연관 메모리. 키(Page Number) + 값(Frame Number) 구조
- **ASID**: TLB 항목이 어느 프로세스에 속한 것인지 알려주는 식별자
- **TLB hit**: TLB에 요청한 Page Number 있음
- **TLB miss**: TLB에 없음 → 페이지 테이블 접근 + TLB에 추가

### C. Protection

- Page table의 각 entry에 **valid/invalid bit**가 있음
- valid: 프로세스의 합법적인 페이지
- invalid: 프로세스의 논리 주소 공간에 속하지 않음 → 트랩 발생

## Related

- [[_MOC]]
- [[7-Deadlocks]]
- [[9-Virtual-Memory]]

## Sources

- Notion: [8. Memory Management - Memory Management](https://www.notion.so/93895218d7e74d4db8bb260a88701042)
