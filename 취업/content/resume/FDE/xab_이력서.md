### xAB (A/B 테스트 기반 SNS)

서비스 개요: 두 가지 선택지에 대한 실시간 투표 및 댓글 토론이 가능한 소셜 네트워크 서비스

팀원: 4명 (FE 4명)

기술 스택: TypeScript, Next.js, React Query, Zustand, Supabase, Tailwind CSS

- 메인 피드 초기 로딩 지연을 줄이기 위해 TanStack Query의 `useInfiniteQuery`와 Intersection Observer 트리거를 결합한 페이지 단위 분할 호출·지연 로딩 기반 무한 스크롤 피드를 구현했습니다.

- 댓글·투표 상호작용의 정합성을 보장하기 위해 Supabase Realtime의 `postgres_changes` 이벤트 구독을 도입해 새로고침 없이 다른 사용자의 활동이 즉시 반영되는 동기화 환경을 구축했습니다.

- 게시글 상세 진입 시 피드 맥락이 끊기는 문제를 해결하기 위해 Next.js App Router의 병렬 라우트와 인터셉팅 라우트를 결합한 모달 라우팅을 구현해 피드 위치를 유지한 상태에서 상세를 띄웠습니다.

- 알림과 세션 상태의 전역 관리를 위해 Zustand 스토어에 Supabase Realtime 구독 핸들을 함께 보관하도록 설계해 컴포넌트 결합도를 낮추고 중복 구독으로 인한 리소스 누수를 막았습니다.

- 미인증 사용자의 보호 경로 접근을 차단하기 위해 `@supabase/ssr` 기반 Next.js 미들웨어를 도입해 매 요청마다 서버 측에서 세션을 검증하고 로그인 페이지로 리다이렉트하도록 구성했습니다.

- 로드밸런서 환경에서 OAuth 콜백 오리진이 잘못 구성되는 문제를 방지하기 위해 콜백 라우트에서 `X-Forwarded-Host` 헤더를 우선 참조해 원본 오리진을 복원하는 분기를 구현했습니다.
