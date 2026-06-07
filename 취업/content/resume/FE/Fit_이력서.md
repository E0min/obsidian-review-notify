### Fit (사일런트 컨퍼런스 플랫폼)

서비스 개요: 무선 헤드폰을 통해 다중 채널의 발표를 골라 듣는 사일런트 컨퍼런스의 온라인/오프라인 하이브리드 중계 플랫폼

팀원: 5명 (FE 3명, BE 2명)

기술 스택: Vite, React, WebRTC, STOMP, SockJS, Framer Motion, Redux Toolkit, redux-persist, Tailwind CSS

- 수백 ms 단위의 저지연 오디오 전송을 위해 RTCPeerConnection API로 발표자·청중 양측 시그널링 클라이언트를 구현하고 STOMP 토픽 위에서 SDP와 ICE 후보를 교환하는 1:N 오디오 송수신 흐름을 설계했습니다.

- SDP 협상 전 도착한 ICE 후보 유실로 연결 실패가 반복되던 문제를 해결하기 위해 ref에 ICE 큐를 두고 setRemoteDescription 직후 일괄 flush하는 버퍼링 로직을 적용해 PeerConnection 성공률을 높였습니다.

- 모바일 망과 행사장 Wi-Fi의 일시 단절에 대비해 STOMP 클라이언트에 reconnectDelay 5초·4초 간격 heartbeat를 설정하고 자체 TURN 서버를 ICE 후보군에 추가해 NAT 환경 연결률을 유지했습니다.

- 시그널링 트래픽과 혼잡도 데이터의 채널 점유 충돌을 막기 위해 혼잡도 전용 STOMP 클라이언트를 별도 구성해 `/sub/session` 토픽만 구독시키고, 채널 간 인원 쏠림을 실시간으로 화면에 반영했습니다.

- 인증 토큰과 좋아요 세션을 Redux Toolkit으로 관리하면서 redux-persist whitelist에 auth만 포함해 새로고침 후 세션은 유지하되 휘발성 데이터가 영속화되는 부작용을 차단했습니다.

- 백엔드 팀과 STOMP `Bearer` 헤더 인증 규약과 토픽 네이밍을 합의해 시그널링 연동 방식을 맞췄습니다.
