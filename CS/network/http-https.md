---
title: HTTP와 HTTPS
aliases: [HTTP, HTTPS, SSL, TLS, 암호화, 인증서, CA]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [cs/network, status/budding]
notion-url: ""
related:
  - "[[_MOC]]"
  - "[[쿠키-세션-jwt]]"
  - "[[websocket]]"
  - "[[icmp]]"
  - "[[webrtc]]"
  - "[[웹서비스-운영-과정]]"
  - "[[../../BE/api-design/rest-api]]"
source: ["Notion: JavaScript"]
migrated-from: "Notion: HTTP/HTTPS"
---

# HTTP와 HTTPS

> TL;DR: HTTP는 비연결성·무상태 프로토콜. HTTPS = HTTP + SSL/TLS 암호화 레이어. TLS 핸드셰이크로 대칭키를 안전하게 교환한 뒤 그 키로 통신을 암호화한다.

---

## What

### HTTP (HyperText Transfer Protocol)

웹에서 클라이언트-서버가 데이터를 주고받는 규약. TCP/IP 기반.

**핵심 특성 2가지**:

| 특성 | 설명 | 결과 |
|------|------|------|
| **비연결성 (Connectionless)** | 요청-응답 후 연결 끊음 | 상태 유지 안 됨, Cookie/Session으로 보완 |
| **무상태 (Stateless)** | 서버가 이전 요청 기억 안 함 | 매 요청에 인증 정보 포함 필요, 확장성 좋음 |

```
클라이언트 → 서버: GET /index.html
서버 → 클라이언트: 200 OK (HTML 응답)
연결 종료. 서버는 이 클라이언트를 기억 안 함.
```

### HTTPS (HTTP Secure)

HTTP + SSL/TLS 암호화. 데이터를 암호화해서 도청·변조·위조를 방지.

---

## How — TLS 핸드셰이크 과정

```
클라이언트                          서버
    │                                │
    │──── Client Hello ──────────────▶│ (지원 TLS 버전, 암호화 방식 목록)
    │                                │
    │◀─── Server Hello + 인증서 ──────│ (선택된 암호화 방식 + 공개키 담긴 인증서)
    │                                │
    │  인증서 검증 (CA 서명 확인)       │
    │  ↓                             │
    │──── Pre-Master Secret ─────────▶│ (서버 공개키로 암호화한 임시 비밀값)
    │                                │
    │  양쪽에서 Pre-Master Secret으로 │
    │  대칭키(Session Key) 생성       │
    │                                │
    │◀═══ 암호화된 통신 시작 (대칭키) ═▶│
```

**핵심 메커니즘**:
1. **비대칭 암호화**(공개키/개인키)로 대칭키를 안전하게 교환
2. 실제 데이터 전송은 **대칭 암호화**(AES 등)로 — 빠름
3. **CA(인증 기관)**가 서버 공개키의 진위를 보증 (서명)

### CA 인증서 신뢰 체계

```
루트 CA (최상위, 브라우저에 내장)
  └── 중간 CA (루트 CA가 서명)
        └── 서버 인증서 (중간 CA가 서명)
              └── 서버 공개키 포함
```

브라우저는 루트 CA 목록을 내장 → 체인을 따라 올라가며 서버 인증서의 신뢰성 검증.

---

## HTTP 버전별 특징

| 버전 | 특징 |
|------|------|
| HTTP/1.0 | 요청마다 새 TCP 연결 |
| HTTP/1.1 | Keep-Alive (연결 재사용), 파이프라이닝 |
| HTTP/2.0 | 멀티플렉싱 (하나의 연결로 여러 요청 동시), 헤더 압축, 서버 푸시 |
| HTTP/3.0 | UDP 기반 QUIC 프로토콜, 연결 설정 시간 단축 |

---

## Why it matters

- **SEO**: Google은 HTTPS 페이지를 HTTP보다 높게 랭킹
- **브라우저 경고**: HTTP 사이트는 "안전하지 않음" 표시
- **API 보안**: 인증 토큰, 개인정보를 평문으로 전송하면 도청 가능
- **HTTP/2 사용 조건**: 대부분 브라우저에서 HTTP/2는 HTTPS에서만 지원

---

## Pitfalls

- **자체 서명 인증서 (Self-signed)**: 개발 환경에서만 — 브라우저가 CA 서명 없음으로 경고, 프로덕션 사용 불가
- **인증서 만료**: 갱신 잊으면 사이트 접속 불가 — Let's Encrypt로 자동 갱신 설정
- **Mixed Content**: HTTPS 페이지에서 HTTP 리소스(img, script) 로드 시 브라우저 차단
- **HTTP Strict Transport Security (HSTS)**: `Strict-Transport-Security` 헤더로 브라우저에 항상 HTTPS 사용 강제 → 중간자 공격 방지

---

## Related

- [[쿠키-세션-jwt]] — HTTPS 위에서 동작하는 세션/인증 메커니즘
- [[../../BE/api-design/rest-api]] — HTTP 메서드와 상태 코드

## Sources

- [MDN — HTTP 개요](https://developer.mozilla.org/ko/docs/Web/HTTP/Overview)
- [MDN — HTTPS](https://developer.mozilla.org/ko/docs/Glossary/HTTPS)
- [Cloudflare — TLS 핸드셰이크](https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/)
