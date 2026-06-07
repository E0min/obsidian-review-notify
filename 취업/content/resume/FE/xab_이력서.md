### xAB (A/B 테스트 기반 SNS)

서비스 개요: 두 가지 선택지에 대한 실시간 투표 및 댓글 토론이 가능한 소셜 네트워크 서비스

팀원: 4명 (FE 4명)

기술 스택: TypeScript, Next.js, React Query, Zustand, Supabase, Tailwind CSS

- 메인 피드 초기 로딩 지연을 해결하기 위해 TanStack Query의 `useInfiniteQuery`와 Intersection Observer 트리거를 결합해 페이지 단위 분할 호출과 지연 로딩이 적용된 무한 스크롤을 구현했습니다.

- 실시간 댓글·투표 정합성을 보장하기 위해 Supabase Realtime의 `postgres_changes` 이벤트 구독을 도입해 새로고침 없이 다른 사용자 활동이 즉시 반영되는 동기화 환경을 구축했습니다.

- 게시글 상세 진입 시 피드 맥락이 끊기던 문제를 해결하기 위해 Next.js App Router의 병렬 라우트와 인터셉팅 라우트를 결합한 모달 라우팅을 구현해 피드 위치를 유지한 채 상세 화면이 노출되도록 했습니다.

- 알림·세션 전역 상태를 Zustand 스토어로 관리하면서 Supabase Realtime 구독 핸들을 함께 보관해 컴포넌트 결합도를 낮추고 중복 구독 리소스 누수를 차단했습니다.

- 보호 경로 접근을 차단하기 위해 `@supabase/ssr` 기반 Next.js 미들웨어로 매 요청 서버 세션을 검증해 미인증 사용자를 리다이렉트하도록 구성했습니다.

- 로드밸런서 환경의 OAuth 콜백 오리진 오류를 콜백 라우트에서 `X-Forwarded-Host` 헤더 우선 참조로 복원했습니다.
