---
title: "12. File System Interface"
aliases: [파일 시스템 인터페이스, File System, 디렉터리 구조]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [cs/os, status/budding]
notion-url: https://www.notion.so/c6e865f91f6f4acda6a89fcef82c031b
related:
  - "[[_MOC]]"
  - "[[11-IO-Systems]]"
  - "[[13-File-System-Implementation]]"
source: ["Notion: 운영체제"]
migrated-from: "Notion: 🏝️ 12. File System - File System Interface"
---

# 12. File System Interface

> TL;DR: 파일 시스템 - 파일 속성·연산, 접근 방식(순차/직접/색인), 디렉터리 구조(1단계/2단계/트리/비순환/일반 그래프), 마운팅, 보호.

파일 시스템은 관련된 정보 자료를 저장하는 **실제적인 파일들의 집합체**와 시스템 내의 모든 파일에 관한 정보를 제공하는 **디렉터리 구조**로 구성된다.

---

## 1. File Concept

### A. File Attributes
- 파일은 보조 기억 장치에 기록된 관련 정보의 집합
- 파일의 속성: 이름, 식별자, 타입, 위치, 크기, 보호(접근 제어 정보), 시간, 날짜, 사용자 식별
- 파일에 대한 정보는 **디렉터리 구조**에 의해 유지됨

### B. File Operations
- 파일 생성, 파일 쓰기, 파일 읽기, 파일 위치 재설정, 파일 삭제, 파일 절단
- 반복적인 탐색을 피하고자 `open()` 시스템 호출로 **열린 파일 테이블** 유지
- **프로세스별 테이블**: 각 프로세스가 연 모든 파일 기록
- **범 시스템 열린 파일 테이블**: 파일의 FCB 정보 보유

### C. File Types
- 운영체제가 파일 유형을 지원하면 파일 유형에 따라 파일 연산 명령을 결정

### D. File Structures
- 운영체제가 여러 파일 구조 지원: 적절한 수행 가능, but 운영체제 크기 증가, 응용성 감소
- 운영체제가 파일 형태에 제한 없음: 유연성 극대화, but 응용 프로그램들이 각자 해석 필요

### E. Internal File Structure
- 물리적 레코드(디스크의 한 블록) ↔ 논리적 레코드 변환
- 파일은 블록 단위로 저장 → **내부 단편화 문제** 발생

---

## 2. Access Mode

| 접근 방식 | 설명 |
|---------|------|
| **Sequential Access (순차 접근)** | 테이프 모델 기반. 순차적으로 읽거나 쓰고 파일 위치 포인터는 자동 증가 |
| **Direct Access (직접 접근)** | 디스크 모델 기반. 어떠한 블록이라도 직접 접근 가능 |
| **Index Access (색인 접근)** | 먼저 index를 찾고 그 index로 파일을 직접 접근하여 원하는 레코드 찾음 |

---

## 3. Directory and Disk Structure

- **볼륨**: 저장장치의 할당 바이트들을 분할/조합하는 데이터 구조체
- **파티션**: 볼륨을 분할하는 것

### A. Directory Overview
디렉터리는 파일의 이름을 그 위치로 바꾸어 주는 "심볼 테이블"
- 파일 찾기, 파일 생성, 파일 삭제, 디렉터리 나열, 파일의 재명명, 파일 시스템의 순회

### B. 1단계 디렉터리
- 가장 간단. 모든 파일이 한 개의 디렉터리 밑에 있다.

### C. 2단계 디렉터리
- 각 사용자는 UFD(User File Directory), 시스템은 UFD를 가리키는 MFD(Master File Directory)를 가짐

### D. Tree-Structured Directory
- 임의의 깊이를 가지는 트리 구조. 사용자들이 자신의 종속 디렉터리를 가짐
- 디렉터리의 각 항목: 일반파일(0) 또는 디렉터리 파일(1)

### E. Acyclic-Graph Directory
- 디렉터리들이 하위디렉터리들과 파일을 공유할 수 있도록 허용
- 유닉스에서 공유파일 = **link** (다른 파일이나 하위 디렉터리를 가리키는 포인터)
- **문제점**: dangling pointer, 삭제 시 공유 파일 처리

### F. General Graph Directory
- 순환이 가능한 구조
- **문제**: 참조 계수가 0이 아닌 파일이 존재 가능 → **가비지 콜렉션** 사용

---

## 4. File-System Mounting
- 파일 시스템은 프로세스들에 의해 사용되기 전에 **마운트** 되어야 한다.
1. 운영체제에게 디바이스 이름과 마운트 포인트가 주어짐
2. 운영체제가 디바이스가 유효한 파일 시스템을 포함하는지 확인
3. 운영체제가 파일 시스템이 지정된 마운트 포인트에 장착되었음을 기록

---

## 5. File Sharing

### A. Multiple Users
- 파일과 디렉터리에 대해 **소유자**와 **그룹** 속성이 필요
- 요청한 사용자의 ID를 파일 소유자 속성과 비교하여 요청 허용 여부 결정

### B. Remote File Systems
- WWW, FTP, DFS(Distributed File System)

---

## 6. Protection

### A. Types of Access
- 읽기, 쓰기, 실행, 추가, 삭제, 리스트

### B. Access Control
- 각 파일과 디렉터리에 **접근 제어 리스트(ACL, Access Control List)** 연관
- 사용자 분류: 소유자(Owner), 그룹(Group), 모든 사람(Others)

---

## Related
- [[_MOC]] — 운영체제 MOC
- [[11-IO-Systems]] — I/O 시스템
- [[13-File-System-Implementation]] — 파일 시스템 구현

## Sources
- [Notion 원본](https://www.notion.so/c6e865f91f6f4acda6a89fcef82c031b)
