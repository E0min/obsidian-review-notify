---
title: WebSocket vs REST API
aliases: [WebSocket, 웹소켓, ws, wss, 실시간 통신, SSE]
type: concept
status: budding
created: 2026-05-25
updated: 2026-05-25
tags: [cs/network, status/budding]
notion-url: ""
related:
  - "[[_MOC]]"
  - "[[http-https]]"
  - "[[쿠키-세션-jwt]]"
  - "[[webrtc]]"
  - "[[웹서비스-운영-과정]]"
  - "[[../../BE/api-design/rest-api]]"
  - "[[../../BE/_concepts/백엔드-신규-프로젝트-기술선택]]"
source: ["Notion: Computer DB"]
migrated-from: "Notion: 웹소켓(WebSocket) vs. HTTPS(REST API) 차이점"
---

# WebSocket vs REST API

> TL;DR: REST API는 요청-응답 단방향(매번 새 연결), WebSocket은 한 번 연결 후 양방향 지속 통신. 실시간성이 필요하면 WebSocket, 단순 CRUD는 REST API.

---

## What

| | **REST API (HTTPS)** | **WebSocket** |
|--|----------------------|---------------|
| 통신 방식 | 요청 → 응답 (단방향) | 서버·클라이언트 양방향 자유 전송 |
| 연결 유지 | 매번 새 연결 (Stateless) | 한 번 연결 후 지속 (Persistent) |
| 실시간성 | ❌ (Polling 필요) | ✅ (서버 즉시 Push 가능) |
| 속도 | 연결 맺고 끊어서 상대적으로 느림 | 연결 유지로 빠른 전송 |
| 데이터 전송량 | 요청마다 HTTP 헤더 포함 (비효율) | 최소 패킷으로 효율 전송 |
| 프로토콜 | `http://` / `https://` | `ws://` / `wss://` |
| 보안 | HTTPS (TLS) | WSS (TLS) |

---

## How

### REST API 흐름

```
클라이언트 → GET /messages → 서버 응답 → 연결 종료
(새 메시지 있어도 알 수 없음 — 다시 요청해야 함)
```

```http
GET /messages HTTP/1.1
Host: example.com
→ [{"id":1,"message":"Hello"}, {"id":2,"message":"How are you?"}]
```

**실시간성 부족** → 새 메시지 확인하려면 Polling(주기적 재요청) 필요

### WebSocket 연결

```javascript
// 클라이언트: 연결 수립 (HTTP → WebSocket Upgrade)
const socket = new WebSocket('wss://example.com/socket');

socket.onopen = () => console.log('연결됨');

// 서버에서 새 메시지 발생 시 즉시 Push — 클라이언트가 요청 안 해도 됨
socket.onmessage = (event) => {
  console.log('새 메시지:', event.data);
};

// 클라이언트 → 서버 전송
socket.send(JSON.stringify({ type: 'chat', text: '안녕!' }));

socket.onclose = () => console.log('연결 종료');
```

---

## 언제 무엇을 쓸까

```
REST API가 적합한 경우:
  - 일반 CRUD (회원가입, 로그인, 게시글 조회)
  - 페이지 로드 후 가끔 데이터 교환
  - 캐싱·인증·미들웨어 생태계 활용 필요

WebSocket이 적합한 경우:
  - 실시간 채팅
  - 주식·코인 가격 실시간 업데이트
  - 멀티플레이 게임
  - IoT 센서 데이터 스트리밍
  - 협업 툴 (공동 편집, 커서 위치)
```

**"WebSocket은 항상 좋은 선택이 아니다"** — 실시간성이 필요한 경우에만. REST보다 연결 관리·확장성 복잡도가 높음.

---

## Pitfalls

- **HTTP/2 + SSE 대안**: 단방향 서버 Push만 필요하면 WebSocket보다 SSE(Server-Sent Events)가 더 단순 — HTTP 위에서 동작해 인증·캐싱 인프라 그대로 사용 가능
- **수평 확장**: WebSocket은 상태가 특정 서버에 고정 → 다중 서버 환경에서 Redis Pub/Sub 등으로 연결 공유 필요
- **방화벽 이슈**: 일부 기업 방화벽이 WebSocket Upgrade를 차단 — 폴백 처리 필요 (socket.io가 이를 자동 처리)
- **연결 유지 비용**: 수만 개의 WebSocket 연결은 서버 메모리·fd 소모 → 연결 수 제한 및 Heartbeat 설계 필수

---

## Related

- [[http-https]] — HTTP 연결 모델 (비연결성·무상태)
- [[../../BE/api-design/rest-api]] — REST API 설계 원칙

## Sources

- [MDN — WebSocket API](https://developer.mozilla.org/ko/docs/Web/API/WebSocket)
- [MDN — Server-sent events](https://developer.mozilla.org/ko/docs/Web/API/Server-sent_events)
