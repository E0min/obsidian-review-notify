---
title: WebRTC (Web Real-Time Communication)
aliases: [WebRTC, web real-time communication, P2P 실시간 통신, 화상 통화]
type: concept
status: budding
created: 2026-05-25
updated: 2026-05-25
tags: [cs/network, status/budding, web, realtime]
notion-url: https://www.notion.so/1c835c50238380569c91c923d2d11558
related:
  - "[[_MOC]]"
  - "[[websocket]]"
  - "[[http-https]]"
source: ["Notion: Computer DB — WebRTC"]
migrated-from: "Notion: WebRTC (Web Real-Time Communication)란?"
---

# WebRTC (Web Real-Time Communication)

> TL;DR: 브라우저 간 **P2P 연결**로 오디오·비디오·데이터를 실시간 전송하는 표준 기술. 화상 회의·VoIP·P2P 파일 공유의 기반. STUN/TURN으로 NAT·방화벽 우회, WebSocket으로 시그널링 조합이 일반적.

---

## What

플러그인 없이 브라우저에서 실시간 음성·영상·데이터 전송을 가능하게 하는 W3C/IETF 표준.

**핵심 특징**
- **P2P (Peer-to-Peer)** 연결 — 서버 없이 직접 데이터 교환
- **저지연(Low Latency)** 실시간 통신
- **DataChannel**로 일반 데이터(채팅·파일)도 전송
- Google 개발, W3C/IETF 표준화

**활용 사례**
- 화상 회의: Google Meet, MS Teams, Jitsi Meet
- VoIP: WhatsApp Web, Discord Web, Skype
- P2P 파일 공유: WebTorrent
- 원격 제어·스트리밍: Parsec, Stadia

---

## 핵심 기술 요소

| 구성 요소 | 역할 |
|---|---|
| **RTCPeerConnection** | P2P 연결 생성·미디어 스트림 송수신 |
| **MediaStream (getUserMedia)** | 카메라·마이크 미디어 캡처 |
| **RTCDataChannel** | P2P 데이터 전송 API (채팅·파일) |
| **ICE (Interactive Connectivity Establishment)** | NAT·방화벽 우회 |
| **STUN/TURN 서버** | 피어 간 연결 수립 보조 |

---

## How — 연결 5단계

```
1. getUserMedia → 카메라·마이크 스트림 획득
2. Signaling     → SDP(Session Description Protocol) 교환 (보통 WebSocket 사용)
3. ICE 후보 교환 → STUN/TURN으로 공인 IP·중계 경로 탐색
4. RTCPeerConnection 수립
5. MediaStream·RTCDataChannel 송수신
```

### 1) 미디어 스트림 가져오기

```javascript
navigator.mediaDevices.getUserMedia({ video: true, audio: true })
  .then(stream => {
    document.getElementById("localVideo").srcObject = stream;
  })
  .catch(err => console.error("카메라/마이크 접근 실패:", err));
```

### 2) P2P 연결 (RTCPeerConnection + SDP)

```javascript
const peerConnection = new RTCPeerConnection();

peerConnection.createOffer()
  .then(offer => peerConnection.setLocalDescription(offer))
  .then(() => sendToSignalingServer(peerConnection.localDescription));
```

### 3) 데이터 전송 (RTCDataChannel)

```javascript
const dataChannel = peerConnection.createDataChannel("chat");
dataChannel.send("Hello WebRTC!");

dataChannel.onmessage = event => {
  console.log("받은 메시지:", event.data);
};
```

### 4) ICE 서버 설정

```javascript
const peerConnection = new RTCPeerConnection({
  iceServers: [
    { urls: "stun:stun.l.google.com:19302" },                              // STUN (공인 IP 탐색)
    { urls: "turn:turn.example.com", username: "user", credential: "pwd" } // TURN (중계)
  ]
});
```

- **STUN**: 공인 IP/Port 알아내기 — 대부분의 P2P 연결에 충분
- **TURN**: 방화벽으로 직접 연결 불가일 때 트래픽 중계

---

## WebRTC vs WebSocket vs HTTP

| 항목 | WebRTC | WebSocket | HTTP (REST API) |
|---|---|---|---|
| 연결 방식 | **P2P** | 서버-클라이언트 | 요청-응답 (Stateless) |
| 지연 시간 | **매우 낮음** | 낮음 | 높음 |
| 미디어 스트리밍 | ✅ | ❌ | ❌ |
| 데이터 전송 | ✅ (DataChannel) | ✅ | ❌ |
| 서버 의존성 | 낮음 (STUN/TURN만) | 높음 | 높음 |

→ 실제 서비스에서는 **WebRTC(데이터 전송) + WebSocket(시그널링)** 조합이 일반적.

---

## Pitfalls

- **NAT/방화벽 문제**: STUN으로 대부분 해결되지만 기업망 등은 TURN 필수 (TURN 트래픽 비용 ↑)
- **시그널링 복잡**: SDP·ICE 후보 교환 로직 직접 구현 부담 → 보통 WebSocket 시그널링 서버 별도 운영
- **모바일 네트워크 품질 저하**: 망 전환·약한 신호에서 화질 떨어짐, 끊김
- **브라우저 호환성**: 코덱·API 동작 차이로 크로스 브라우저 테스트 필수

---

## Related

- [[_MOC]]
- [[websocket]] — WebRTC 시그널링 채널로 자주 결합
- [[http-https]] — HTTPS 기반 페이지에서만 카메라/마이크 권한 획득 가능

## Sources

- [Notion 원본 — WebRTC (Web Real-Time Communication)란?](https://www.notion.so/1c835c50238380569c91c923d2d11558)
