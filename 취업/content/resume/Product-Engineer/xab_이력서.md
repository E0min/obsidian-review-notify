### xAB (A/B 테스트 기반 SNS)

서비스 개요: 두 가지 선택지에 대한 실시간 투표 및 댓글 토론이 가능한 소셜 네트워크 서비스. Next.js App Router 위에서 인증·실시간 동기화·모달 라우팅을 풀스택으로 담당했습니다.

팀원: 4명 (FE 4명)

기술 스택: TypeScript, Next.js, React Query, Zustand, Supabase, Tailwind CSS

- 게시글 상세 진입 시 피드 위치와 맥락이 끊기는 문제를 Next.js App Router의 병렬 라우트와 인터셉팅 라우트를 결합한 모달 라우팅으로 해결해 피드 위치를 유지한 채 상세 화면을 띄웠습니다.

- 새로고침 없이 다른 사용자의 댓글·투표가 즉시 반영되도록 Supabase Realtime의 `postgres_changes` 이벤트 구독을 React Query 캐시 갱신 로직과 연동했습니다.

- 미인증 사용자의 보호 경로 접근을 차단하기 위해 `@supabase/ssr` 기반 Next.js 미들웨어로 매 요청마다 서버 측 세션을 검증하고 로그인 페이지로 리다이렉트하게 구성했습니다.

- 메인 피드 초기 로딩 지연을 줄이기 위해 TanStack Query의 `useInfiniteQuery`와 Intersection Observer 트리거를 결합해 페이지 단위 분할 호출 기반 무한 스크롤 피드를 구현했습니다.

- 로드밸런서 환경에서 OAuth 콜백 오리진이 잘못 구성되어 로그인 후 사용자가 잘못된 도메인으로 떨어지는 문제를 콜백 라우트에서 `X-Forwarded-Host` 헤더를 우선 참조해 원본 오리진을 복원하는 분기로 해결했습니다.
