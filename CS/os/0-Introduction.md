---
title: 0. Introduction
aliases: [OS 개요, 운영체제 입문, OS Introduction]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [cs/os, status/budding]
notion-url: https://www.notion.so/550888fd812e41e7afbd4f68116d75ee
related:
  - "[[_MOC]]"
  - "[[1-Operating-System-Structures]]"
source: ["Notion: 운영체제"]
migrated-from: "Notion: 🏸 0. Introduction"
---

# 0. Introduction

> TL;DR: 운영체제(커널)는 하드웨어 위에서 자원 할당과 공통 기능을 추상화해, 사용자와 응용프로그램이 컴퓨터를 편리하고 효율적으로 사용할 수 있게 한다.

## 핵심 개념 (Key Terms)

- **부팅**: ROM에 저장된 부트로더는 저장장치에 있는 kernel을 메모리로 적재하는 역할을 한다.
- **폰노이만 구조**: CPU가 데이터와 명령어를 처리하는 방식 중 하나로, 데이터와 명령어 모두가 메모리에 저장되며 CPU는 이 메모리를 읽어와서 처리한다.
- **가상화**: 계층상 하위계층에게 일관된 인터페이스를 제공하기 위한 기술이다.

## 1. What's Operating System Do

- 컴퓨터 시스템은 대개 하드웨어, 운영체제, 응용프로그램 및 사용자로 구분된다.
- 운영체제를 보는 관점:
  - **사용자 관점**: 편의성
  - **시스템 관점**: 자원의 공정한 할당
- 운영체제란 순수 하드웨어만으로는 사용이 쉽지 않으며, 다양한 프로그램들은 입출력 장치의 제어와 같은 공통적인 연산을 필요로 한다. 여기에 자원을 할당하는 공통 기능을 하나의 소프트웨어로 융합한 것이다.
- 일반적으로 운영체제는 컴퓨터가 실행하면 항상 실행되는 프로그램으로 **커널(Kernel)** 이라고 불린다.

## 2. Computer System

### A. Computer-System Operation

- 현대의 컴퓨터 시스템은 하나 이상의 CPU와 다수의 장치 제어들로 구성되며 이들은 bus로 연결된다.
- 컴퓨터 구동 시 ROM에 저장된 **부트스트랩 프로그램**이 실행되며 운영체제 커널을 찾아 메모리에 적재한다.
- 커널이 적재되고 실행되면 사건이 발생할 때 서비스를 제공하는데, 이 사건을 **인터럽트(Interrupt)** 라고 부른다. 인터럽트는 System call을 호출하여 발생된다.
- CPU는 인터럽트 요청이 들어온 위치로 가서 **ISR(Interrupt Service Routine)** 을 실행한다.

## Related

- [[_MOC]]
- [[1-Operating-System-Structures]]

## Sources

- Notion 원본: <https://www.notion.so/550888fd812e41e7afbd4f68116d75ee>
- migrated-from: "Notion: 🏸 0. Introduction"
