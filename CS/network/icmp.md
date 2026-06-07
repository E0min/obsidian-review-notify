---
title: ICMP (Internet Control Message Protocol)
aliases: [ICMP, 핑, ping, traceroute, TTL, Destination Unreachable]
type: concept
status: budding
created: 2026-05-25
updated: 2026-05-25
tags: [cs/network, status/budding]
notion-url: ""
related:
  - "[[_MOC]]"
  - "[[http-https]]"
  - "[[websocket]]"
source: ["Notion: Computer DB"]
migrated-from: "Notion: ICMP v4"
---

# ICMP (Internet Control Message Protocol)

> TL;DR: ICMP는 IP 통신의 오류 보고·상태 조회 전용 프로토콜. TCP/UDP와 달리 데이터 전송 목적이 아니며, ping(Echo)과 traceroute(Time Exceeded)가 대표 활용 사례다.

---

## What

IP는 **비신뢰성(Best-effort)** 프로토콜 — 패킷 전달 실패를 알리는 메커니즘이 없다. ICMP가 그 역할을 담당: 라우터·호스트가 오류 상황을 발신지에 보고하고, 네트워크 진단 쿼리를 처리한다.

ICMP 메시지는 IP 패킷에 담겨 전송되며, **오류 보고(Error-reporting)**와 **쿼리(Query)** 두 범주로 나뉜다.

---

## How

### ICMP 메시지 구조

```
| Type (1 byte) | Code (1 byte) | Checksum (2 bytes) |
| 나머지 헤더 (Type별 상이)                           |
| Data: 오류를 일으킨 원본 IP 헤더 + 첫 8 bytes      |
```

- **Type**: 메시지 종류
- **Code**: Type 내 세부 이유
- **Data**: 오류 발생 패킷의 헤더를 포함 → 발신지가 어느 패킷이 문제였는지 파악 가능

---

### 오류 보고 메시지 (Error-Reporting)

#### Type 3 — Destination Unreachable (목적지 도달 불가)

| Code | 의미 | 발생 상황 |
|------|------|-----------|
| 0 | Network Unreachable | 목적지 네트워크로 가는 경로 없음 |
| 1 | Host Unreachable | 네트워크는 찾았으나 호스트 응답 없음 |
| 2 | Protocol Unreachable | 호스트에 도달했으나 해당 프로토콜 미지원 |
| 3 | Port Unreachable | 프로세스가 해당 포트 수신 안 함 (UDP 주로) |
| 4 | Fragmentation Needed & DF Set | 분할 필요한데 DF 비트 설정 → MTU 문제 |

#### Type 11 — Time Exceeded (시간 초과)

```
라우터가 패킷의 TTL을 0으로 감소시키면 패킷 폐기 + Type 11 전송
Code 0: TTL 초과 (라우터에서)
Code 1: Fragment reassembly 시간 초과 (목적지에서)
```

**traceroute 원리**: TTL을 1→2→3... 순차 증가시켜 전송, 각 라우터에서 Type 11을 받아 경로 추적.

#### Type 5 — Redirect (경로 재설정)

라우터가 호스트에게 "더 나은 경로가 있다"고 알림. 호스트의 라우팅 테이블 갱신 유도.

#### Type 4 — Source Quench (혼잡 제어, 구식)

라우터 버퍼 초과 시 발신지에 속도 낮추도록 요청. **현재는 deprecated** — TCP의 혼잡 제어로 대체.

#### Type 12 — Parameter Problem

IP 헤더의 파라미터가 잘못된 경우. Code 0: 잘못된 헤더 필드 포인터 포함.

---

### 쿼리 메시지 (Query)

#### Type 8 / 0 — Echo Request / Echo Reply (ping)

```
발신지 → Type 8 (Echo Request) → 목적지
발신지 ← Type 0 (Echo Reply)   ← 목적지
```

```bash
# ping 동작
ping google.com
# PING google.com: 56 data bytes
# 64 bytes from 142.250.x.x: icmp_seq=0 ttl=117 time=12.4 ms
```

- **TTL 값**: 패킷이 거친 홉 수 추적 가능 (초기 TTL - 수신 TTL)
- **time**: RTT (Round Trip Time) — 왕복 시간

#### Type 13 / 14 — Timestamp Request / Reply (RTT 측정)

```
발신지 → Type 13 (originate timestamp) → 목적지
발신지 ← Type 14 (receive + transmit timestamp) ← 목적지

RTT = (수신시각 - 발신시각) - (목적지 처리시간)
```

---

## 언제 마주치나 (실전)

```
ping → Type 8/0 Echo — 호스트 생존 확인
traceroute → Type 11 TTL Exceeded — 경로 추적
"Connection refused" → Type 3 Code 3 Port Unreachable
"Network unreachable" → Type 3 Code 0 Network Unreachable
MTU 문제 → Type 3 Code 4 Fragmentation Needed
```

---

## Pitfalls

- **ICMP는 오류를 보고할 뿐, 수정하지 않는다** — 재전송은 상위 레이어(TCP) 담당
- **ICMP 차단**: 방화벽이 ICMP를 블록하면 ping/traceroute가 동작하지 않음 — 연결 문제와 혼동 주의
- **ICMP Flooding (Smurf Attack)**: 브로드캐스트 주소로 Echo Request 전송해 네트워크 마비 → 현재 브로드캐스트 ICMP 대부분 차단
- **ICMP는 신뢰성 없음**: ICMP 메시지 자체도 IP 위에서 전송되므로 유실 가능

---

## Related

- [[http-https]] — IP 위의 TCP/HTTP 스택
- [[websocket]] — 응용 계층 통신 프로토콜

## Sources

- Forouzan, *Data Communications and Networking* — ICMP v4 챕터
- [Cloudflare — What is ICMP?](https://www.cloudflare.com/learning/ddos/glossary/internet-control-message-protocol-icmp/)
- [MDN — ping](https://developer.mozilla.org/en-US/docs/Glossary/Ping)
