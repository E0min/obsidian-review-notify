### chatGraph (AI 대화 시각화 플랫폼)

서비스 개요: LLM과의 대화를 꼬리물기 형태의 마인드맵 그래프로 시각화하는 웹 서비스입니다. LLM 응답 대기 동안 발생하는 사용자 흐름 단절을 줄이고 시각화 라이프사이클을 통합하는 클라이언트 책임을 맡았습니다.

팀원: 4명 (FE 2명, BE 2명)

기술 스택: TypeScript, React, Next.js, D3.js, Zustand, Tailwind CSS, TanStack Query, Vitest, LLM API (서버 경유)

- 새 토픽 생성 시 LLM 응답 대기로 화면이 멈추는 문제를 해결하고자 sessionStorage와 temp ID로 즉시 라우팅 후 성공 시 실제 ID로 교체하는 Optimistic 라우팅을 설계해 대기 중에도 채팅 화면을 곧바로 띄웠습니다.

- 사이드바 토픽 클릭 시 초기 로딩 지연을 줄이고자 Zustand 스토어에 LLM 응답을 프리패치하고 useSuspenseQuery의 initialData로 주입해 라우트 전환 시 빈 화면 없이 데이터를 즉시 그렸습니다.

- 팀원이 도입한 D3.js Force Simulation이 리렌더 시 SVG 트리와 충돌하는 문제를 useEffect cleanup과 `d3.selectAll("*").remove()`로 해결해 데이터 변경 시 SVG 재구성을 보장했습니다.

- 확장에 대비해 Feature-First 구조로 features·views·shared를 분리하고, 843줄까지 비대해진 use-question-tree 훅을 책임 단위로 나눠 355줄로 축소했습니다.

- 페이지 컴포넌트의 책임을 분산하고자 TopicContentLayout·StandardChatView·OptimisticChatView로 뷰 계층을 분리하고 Suspense 경계와 컴포지션을 재설계했습니다.

- findPathToNode 경로 탐색·Zustand 토픽 토글·새 토픽 시작 훅에 Vitest 회귀 테스트를 작성해 핵심 흐름의 회귀를 자동 감지했습니다.
