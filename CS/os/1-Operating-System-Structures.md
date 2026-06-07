---
title: 1. Operating System Structures
aliases: [OS 구조, 운영체제 구조, OS Structures]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [cs/os, status/budding]
notion-url: https://www.notion.so/fa29f7760c054101a01f975e8c1eba5c
related:
  - "[[_MOC]]"
  - "[[0-Introduction]]"
  - "[[2-Process-Management-Process]]"
source: ["Notion: 운영체제"]
migrated-from: "Notion: 🎃 1. Operating System Structures"
---

# 1. Operating System Structures

> TL;DR: 운영체제는 서비스, 인터페이스, 시스템 콜/프로그램, 그리고 커널 구조(모놀리식·마이크로커널)라는 세 관점으로 이해할 수 있다.

운영체제를 보는 관점은 세 가지로 나눌 수 있다.

- 운영체제가 제공하는 **서비스**에 초점
- 운영체제가 사용자 및 프로세스에 제공하는 **인터페이스**에 초점
- 시스템의 **구성 요소와 그들의 상호 연결**에 초점

## 1. 운영체제 서비스

- **사용자 인터페이스**: GUI, CLI, 터치 스크린, Batch interface
- **프로그램 실행**: 프로그램을 메모리에 적재하여 실행
- **입출력 연산**: 프로세스가 요청하는 I/O 디바이스들의 입출력 요구
- **파일 시스템 조작**: 파일의 저장, 수정, 삭제, 생성(CRUD)을 지원
- **통신**: 프로세스 간에 정보를 교환해야 할 상황에서 일어난다.
- **오류 탐지**
- **자원 할당**: 하드웨어나 소프트웨어와 같이 컴퓨터의 자원을 여러 사용자들에게 할당
- **회계(Accounting)**: 컴퓨터 자원을 누가 얼마나 사용하는지 사용 통계를 내는 것
- **보호와 보안**

## 2. 사용자 운영체제 인터페이스

### Command Line

- 운영체제가 제공하는 사용자 인터페이스 서비스
- 여러 명령어를 해석할 수 있는 shell을 제공 (BASH, CSH, KSH)
- shell script

### GUI

- 사용자 친화적인 사용자 인터페이스
- 마우스, 터치 스크린을 통해 여러 가지 조작

## 3. 시스템 콜

- **시스템 콜(System Call)**: OS에서 제공되는 서비스에 대한 인터페이스를 제공
- **API**: 프로그래머가 사용가능한 함수의 집합을 명시. API가 프로그램 이식성이 더 좋아서 시스템 콜보다 더 많이 쓰인다.
- 프로그래밍언어들을 위한 런타임 시스템은 운영체제가 제공하는 시스템 호출에 대한 연결 고리로서 동작하는 **시스템 호출 인터페이스**를 제공한다.

## 4. 시스템 호출의 유형

- a. 프로세스 제어
- b. 파일 관리
- c. 장치 관리
- d. 정보의 유지
- e. 통신
- f. 보호

## 5. 시스템 프로그램

- 파일 관리, 상태 정보, 파일 변경, 프로그래밍 언어 지원, 프로그램 적재와 실행, 통신, 백그라운드 서비스

## 6. 운영체제 설계 및 구현

## 7. 운영체제 구조

- **간단한 구조 (Monolithic Kernel)**: 거의 모든 OS 기능이 하나의 커널 공간에서 동작
- **마이크로 커널**: 핵심 기능만 커널에, 나머지는 사용자 공간(서버 프로세스)에 두는 구조

## Related

- [[_MOC]]
- [[0-Introduction]]
- [[2-Process-Management-Process]]

## Sources

- Notion 원본: <https://www.notion.so/fa29f7760c054101a01f975e8c1eba5c>
- migrated-from: "Notion: 🎃 1. Operating System Structures"
