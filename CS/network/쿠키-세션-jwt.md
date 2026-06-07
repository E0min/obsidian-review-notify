---
title: 쿠키·세션·JWT·캐시
aliases: [cookie, session, JWT, cache, 쿠키, 세션, 캐시, 인증, Cache-Control, ETag]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [cs/network, status/budding]
notion-url: ""
related:
  - "[[_MOC]]"
  - "[[http-https]]"
  - "[[웹서비스-운영-과정]]"
  - "[[../../BE/api-design/rest-api]]"
  - "[[../../BE/_concepts/백엔드-신규-프로젝트-기술선택]]"
  - "[[../../FE/nextjs/rsc-fetch-헤더]]"
source: ["Notion: JavaScript"]
migrated-from: "Notion: 쿠키·세션·JWT·캐시"
---

# 쿠키·세션·JWT·캐시

> TL;DR: HTTP 무상태를 보완하는 3가지 — Cookie(클라이언트 저장 4KB 이하), Session(서버 저장 + 클라이언트 세션ID), JWT(서버리스 토큰, 자체 검증). 캐시는 Cache-Control/ETag로 재요청 최소화.

---

## What

HTTP는 **무상태(Stateless)** — 서버가 이전 요청을 기억하지 않는다. 로그인 상태 유지, 장바구니 등 "기억"이 필요한 경우 쿠키/세션/JWT로 보완한다. 캐시는 불필요한 재요청을 줄이는 별개의 메커니즘.

---

## How

### Cookie

브라우저에 저장되는 작은 데이터 조각. 매 요청마다 자동으로 서버에 전송.

```http
Set-Cookie: session_id=abc123; HttpOnly; Secure; SameSite=Strict; Max-Age=86400
```

| 속성 | 설명 |
|------|------|
| `HttpOnly` | JavaScript에서 접근 불가 → XSS 방지 |
| `Secure` | HTTPS에서만 전송 |
| `SameSite=Strict` | 다른 도메인 요청 시 쿠키 전송 안 함 → CSRF 방지 |
| `Max-Age` | 초 단위 유효기간 (없으면 세션 쿠키 → 브라우저 종료 시 삭제) |
| 크기 제한 | 4KB |

```javascript
// JavaScript에서 쿠키 읽기 (HttpOnly가 아닌 경우만)
document.cookie; // "name=value; other=data"

// 서버에서 Set-Cookie 없이 클라이언트 쿠키 설정
document.cookie = "preference=dark; Max-Age=604800"; // 7일
```

### Session

서버가 상태를 저장하는 방식. 클라이언트는 세션 ID만 쿠키로 보유.

```
로그인 요청 (ID/PW)
       ↓
서버: 세션 생성 → DB/Redis에 저장
      세션 ID를 Set-Cookie로 전송
       ↓
브라우저: 쿠키에 세션 ID 저장

다음 요청
       ↓
브라우저: 세션 ID 쿠키 자동 전송
서버: 세션 ID로 DB 조회 → 사용자 확인
```

**특징**:
- 서버 메모리/DB 사용 → 서버 부담
- 세션 ID 탈취 = 계정 탈취 (but 서버에서 세션 무효화 가능)
- 다중 서버 환경에서 세션 공유 필요 (Redis 등)

### JWT (JSON Web Token)

서버가 서명한 토큰을 클라이언트가 보관. 서버는 상태를 저장하지 않음 (Stateless).

```
Header.Payload.Signature
```

```javascript
// Payload 예시 (Base64 디코딩 가능 — 민감 정보 넣지 말 것)
{
  "sub": "user_123",
  "role": "admin",
  "exp": 1716500000  // 만료 시각 (Unix timestamp)
}
```

**검증 과정**:
1. 클라이언트 → `Authorization: Bearer <JWT>` 헤더로 전송
2. 서버: 서명 검증 (비밀키로) + 만료 시각 확인
3. DB 조회 없이 토큰 자체에서 사용자 정보 추출

| | Session | JWT |
|--|---------|-----|
| 상태 저장 | 서버 (DB/Redis) | 없음 (클라이언트) |
| 확장성 | 서버 간 세션 공유 필요 | 어느 서버든 검증 가능 |
| 토큰 무효화 | 서버에서 즉시 삭제 가능 | 만료 전까지 무효화 어려움 |
| 페이로드 | 서버에만 있음 | 클라이언트에서 열람 가능 |
| 적합 | 소규모, 보안 중요 | 마이크로서비스, 모바일 API |

---

### Cache (캐시)

서버 응답을 재사용해 네트워크 요청 최소화.

#### Cache-Control 헤더

```http
Cache-Control: public, max-age=3600
# public: CDN/프록시도 캐시 가능
# max-age=3600: 3600초(1시간) 동안 유효

Cache-Control: private, max-age=0, no-cache
# private: 브라우저만 캐시 (CDN 저장 안 됨)
# no-cache: 캐시 저장하되, 사용 전 서버에 재검증 요청
# no-store: 캐시 자체를 저장하지 않음

Cache-Control: immutable, max-age=31536000
# immutable: 만료 전까지 절대 변하지 않음 (정적 자산에 사용)
```

#### ETag (Entity Tag) — 조건부 요청

```
최초 요청:
서버 → 브라우저: 200 OK, ETag: "abc123"

캐시 만료 후 재요청:
브라우저 → 서버: GET /data, If-None-Match: "abc123"
서버: 변경 없음 → 304 Not Modified (body 없음, 빠름)
서버: 변경 있음 → 200 OK + 새 ETag
```

#### 실전 Next.js 설정

```typescript
// next.config.ts — 정적 자산 캐시
const nextConfig = {
  async headers() {
    return [
      {
        source: '/_next/static/(.*)',
        headers: [{ key: 'Cache-Control', value: 'public, max-age=31536000, immutable' }],
      },
      {
        source: '/api/(.*)',
        headers: [{ key: 'Cache-Control', value: 'no-store' }],
      },
    ];
  },
};
```

---

## Pitfalls

- **JWT 페이로드 암호화 오해**: JWT는 서명(무결성 보장)만, 암호화가 아님 — Base64 디코딩하면 내용 열람 가능. 민감 정보(비밀번호, 카드번호) 절대 넣지 말 것
- **JWT 만료 후 갱신 설계**: 짧은 access token(15분) + 긴 refresh token(7일) 패턴으로 보안과 UX 균형
- **Cookie SameSite 미설정**: CSRF 공격 취약 → `SameSite=Lax` 이상 설정
- **no-cache vs no-store 혼동**: `no-cache`는 캐시하되 재검증 필요, `no-store`는 아예 캐시 안 함
- **인증 API에 캐시**: `Authorization` 헤더가 있는 응답은 `private`으로만 (CDN에 캐시되면 다른 사용자에게 노출)

---

## Related

- [[http-https]] — HTTP 무상태·비연결성 배경
- [[../../BE/api-design/rest-api]] — API 인증 헤더 규약
- [[../../FE/nextjs/rsc-fetch-헤더]] — RSC에서 Cookie 수동 전달 패턴

## Sources

- [MDN — HTTP cookies](https://developer.mozilla.org/ko/docs/Web/HTTP/Cookies)
- [MDN — Cache-Control](https://developer.mozilla.org/ko/docs/Web/HTTP/Headers/Cache-Control)
- [JWT.io — JWT 소개](https://jwt.io/introduction)
