---
title: 3. Thread & Concurrency
aliases: [스레드, Thread, 병행성, Concurrency]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [cs/os, status/budding]
notion-url: https://www.notion.so/1d36e5eda44844e6b086e37d653fd740
related:
  - "[[_MOC]]"
  - "[[2-Process-Management-Process]]"
  - "[[4-CPU-Scheduling]]"
  - "[[5-Synchronization-Tools]]"
source: ["Notion: 운영체제"]
migrated-from: "Notion: 👟 3. Process Management - Thread & Concurrency"
---

# 3. Thread & Concurrency

> TL;DR: 스레드는 프로세스 자원을 공유하는 CPU 이용의 기본 단위로, 다중 코어 시대의 병행/병렬 실행과 스레드 풀·암묵적 스레딩으로 효율과 응답성을 끌어올린다.

거의 모든 현대의 운영체제는 한 프로세스가 여러 스레드를 포함하는 특성을 가진다.

## 1. 개요

- **스레드는 CPU 이용의 기본 단위**다: 스레드 ID, 프로그램 카운터, 레지스터 집합, 스택으로 구성된다.
- 한 프로세스에 속한 스레드들은 **코드 영역, 데이터 영역, 힙 영역, 파일들, 운영체제 자원들을 공유**한다.
- Thread는 PCB에서 Program counter와 레지스터에 대한 정보만 다르다.

### A. 동기 (사용 이유)

- 프로세스 생성보다 스레드 생성이 더 효율적이다.
- 웹서버 예시: Main Thread가 클라이언트 요청에 대한 Worker Thread를 생성하여 요청을 수행한다.

### B. 장점

- **응답성**: 프로세스의 어떤 스레드가 blocked 되어도, 다른 스레드에서 응답 가능
- **자원 공유**: 스레드는 자동으로 프로세스의 자원들과 메모리를 공유 (프로세스 간 공유보다 쉬움)
- **경제성**: 프로세스 생성보다 스레드 생성 및 문맥교환이 더 효율적
- **규모 적응성**: 다중 처리기 구조에서 다중 스레드의 이점이 증가

## 2. 다중 코어 프로그래밍(Multicore Programming)

- **병행 실행(concurrency)**: 여러 프로세스/스레드가 CPU 스케쥴링에 의해 (논리적으로 동시에) 실행되는 것
- **병렬 실행(parallelism)**: 다중코어 시스템에서 CPU가 여러 개이니 (물리적으로 동시에) 실행되는 것

### 암달의 법칙(Amdahl's Law)

- 순차적 실행 구성요소 S, 코어의 수 N일 때:

```text
Speedup = 1 / (S + (1 - S) / N)
```

- N이 무한대여도 성능 증가량은 최대 `1/S`로 제한된다.

### A. 프로그래머들의 도전과제

- 태스크 식별, 균형, 데이터 분리, 데이터 종속성, 시험 및 디버깅

### B. 병렬 실행의 유형

- **Data parallelism**: 한 데이터를 부분으로 나누어 각 CPU에 동일한 연산 수행
- **Task parallelism**: 데이터가 아닌 스레드를 다수의 코어에 분배. 각 스레드는 고유한 연산 수행

## 3. 다중 스레드 모델

| 모델 | 설명 | 단점 |
|------|------|------|
| Many-to-One | 많은 사용자 스레드 → 하나의 커널 스레드 | 하나 봉쇄 시 전체 봉쇄, 진정한 병렬 불가 |
| One-to-One | 각 사용자 스레드 → 하나의 커널 스레드 | 커널 스레드 생성 오버헤드 |
| Many-to-Many | 여러 사용자 스레드 → 같거나 적은 수의 커널 스레드 | 위 두 모델의 단점 해결 |

## 4. 스레드 라이브러리

- 스레드 라이브러리는 프로그래머에게 스레드를 생성하고 관리하기 위한 API를 제공한다.
1. 커널의 지원 없이 완전히 사용자 공간에서만 제공
2. 운영체제에 의해 지원되는 커널 수준 라이브러리

## 5. 암묵적 스레딩

- 스레딩의 생성과 관리 책임을 개발자로부터 컴파일러와 runtime 라이브러리에게 넘겨주는 방식

### A. 스레드 풀

**문제**: 매 요청마다 스레드 생성 시 생성 시간 + 한계 수 문제

**해결**: 프로세스를 시작할 때 일정한 수의 스레드들을 미리 풀로 만들어 저장. 요청을 끝마친 스레드는 다시 스레드 풀로 돌아와 대기.

**장점**:

1. 기존 스레드로 서비스하는 것이 새 스레드 생성보다 빠름
2. 스레드 수에 제한을 두어 과부하 방지

## Related

- [[_MOC]]
- [[2-Process-Management-Process]]
- [[4-CPU-Scheduling]]
- [[5-Synchronization-Tools]]

## Sources

- Notion 원본: <https://www.notion.so/1d36e5eda44844e6b086e37d653fd740>
- migrated-from: "Notion: 👟 3. Process Management - Thread & Concurrency"
