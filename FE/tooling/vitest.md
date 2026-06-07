---
title: Vitest — 유닛·통합 테스트
aliases: [vitest, unit test, testing library, react testing]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/tooling, status/budding]
notion-url: ""
related:
  - "[[_MOC]]"
  - "[[코드-품질-패키지]]"
  - "[[../../FE/nextjs/_MOC]]"
source: ["Notion: JavaScript"]
migrated-from: "Notion: Vitest"
---

# Vitest — 유닛·통합 테스트

> TL;DR: Vite 기반 테스트 러너. Jest API와 호환되며, `jsdom` 환경과 `@testing-library/react`를 조합해 컴포넌트를 DOM 렌더링 없이 테스트한다.

---

## What

Vitest는 Vite 플러그인 생태계를 활용하는 테스트 프레임워크. Jest와 API가 거의 동일해 마이그레이션이 쉽고, ESM 지원·빠른 실행·Hot Module Replacement가 강점.

---

## How

### Part A — 설치 및 설정

```bash
npm install -D vitest @vitejs/plugin-react jsdom @testing-library/react @testing-library/user-event
```

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',   // 브라우저 DOM API 시뮬레이션
    globals: true,           // describe/test/expect를 전역으로 (import 생략)
    setupFiles: ['./vitest.setup.ts'], // jest-dom 매처 등록
  },
});
```

```typescript
// vitest.setup.ts
import '@testing-library/jest-dom';
```

```json
// package.json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}
```

---

### Part B — 기본 테스트 작성

```typescript
// components/Counter.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, test, expect } from 'vitest';
import Counter from './Counter';

describe('Counter 컴포넌트', () => {
  test('초기 카운트가 0이다', () => {
    render(<Counter />);
    expect(screen.getByText('0')).toBeInTheDocument();
  });

  test('버튼 클릭 시 카운트가 1 증가한다', async () => {
    render(<Counter />);
    const button = screen.getByRole('button', { name: /증가/ });
    fireEvent.click(button);
    expect(screen.getByText('1')).toBeInTheDocument();
  });
});
```

#### 주요 쿼리 우선순위 (Testing Library 권장)

```typescript
// 1순위: 접근성 역할 기반 (사용자가 보는 것)
screen.getByRole('button', { name: /제출/ });
screen.getByRole('textbox', { name: /이메일/ });

// 2순위: 레이블/플레이스홀더 텍스트
screen.getByLabelText('비밀번호');
screen.getByPlaceholderText('검색어 입력');

// 3순위: 텍스트 내용
screen.getByText('저장');

// 4순위 (최후): data-testid (접근성 무관 요소만)
screen.getByTestId('error-message');
```

#### fireEvent vs userEvent

```typescript
import userEvent from '@testing-library/user-event';

// fireEvent: 단순 DOM 이벤트 디스패치 (동기)
fireEvent.click(button);
fireEvent.change(input, { target: { value: '텍스트' } });

// userEvent: 실제 사용자 행동 시뮬레이션 (비동기, 더 현실적)
const user = userEvent.setup();
await user.click(button);
await user.type(input, '텍스트');
// → userEvent를 기본으로 쓰고, 동기가 필요할 때만 fireEvent
```

#### 비동기 쿼리

```typescript
// getBy: 즉시 찾기 (없으면 에러)
// queryBy: 즉시 찾기 (없으면 null, assertion용)
// findBy: 비동기 대기 (없으면 타임아웃)

test('데이터 로딩 후 목록이 나타난다', async () => {
  render(<UserList />);
  const item = await screen.findByText('영민');  // DOM에 나타날 때까지 대기
  expect(item).toBeInTheDocument();
});
```

---

### Part C — Mocking

#### `vi.fn()` — 함수 목킹

```typescript
import { vi } from 'vitest';

const mockFn = vi.fn();
mockFn('인자');

expect(mockFn).toHaveBeenCalledWith('인자');
expect(mockFn).toHaveBeenCalledTimes(1);

// 반환값 지정
mockFn.mockReturnValue(42);
mockFn.mockResolvedValue({ data: [] }); // async
```

#### `vi.mock()` — 모듈 전체 목킹

```typescript
// api.ts의 fetchUsers를 목킹
vi.mock('./api', () => ({
  fetchUsers: vi.fn().mockResolvedValue([
    { id: 1, name: '영민' },
  ]),
}));

test('유저 목록을 렌더링한다', async () => {
  render(<UserList />);
  expect(await screen.findByText('영민')).toBeInTheDocument();
});
```

#### MSW (Mock Service Worker) — API 목킹

```typescript
// src/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users', () => {
    return HttpResponse.json([{ id: 1, name: '영민' }]);
  }),
];

// vitest.setup.ts
import { setupServer } from 'msw/node';
import { handlers } from './src/mocks/handlers';

const server = setupServer(...handlers);
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

MSW는 실제 네트워크 레이어를 인터셉트하므로, fetch 구현체와 무관하게 동작.

#### 타이머 목킹

```typescript
test('3초 후 알림이 사라진다', () => {
  vi.useFakeTimers();
  render(<Toast />);
  vi.advanceTimersByTime(3000);
  expect(screen.queryByRole('alert')).not.toBeInTheDocument();
  vi.useRealTimers();
});
```

---

### Part D — Next.js 통합

```typescript
// Next.js 의존성 목킹
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    prefetch: vi.fn(),
  }),
  usePathname: () => '/dashboard',
  useSearchParams: () => new URLSearchParams(),
}));

vi.mock('next/headers', () => ({
  cookies: () => ({ get: vi.fn() }),
}));
```

**클라이언트 컴포넌트 테스트** (위와 같이 목킹 후 `render()` 사용)

**서버 컴포넌트 테스트** (비동기 함수로 처리)
```typescript
// 서버 컴포넌트는 async function → await로 결과를 직접 검증
test('서버 컴포넌트 데이터 로딩', async () => {
  const result = await MyServerComponent({ id: 1 });
  // JSX 결과 또는 데이터를 직접 검증
});
```

**.env.test** — 테스트 전용 환경 변수
```env
# .env.test
DATABASE_URL=postgresql://localhost:5432/test_db
NEXT_PUBLIC_API_URL=http://localhost:3000
```

---

### Part E — 도구 및 CI/CD

```bash
# 대화형 UI (브라우저에서 테스트 결과 시각화)
npx vitest --ui

# 커버리지 리포트 (v8 또는 istanbul)
npx vitest --coverage
# → coverage/ 디렉토리에 HTML 리포트 생성
```

```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test -- --reporter=verbose
      - run: npm run test:coverage
```

---

## Pitfalls

- `globals: true` 없이 `describe/test/expect`를 import 없이 쓰면 에러 → `vitest.config.ts`에 명시
- 서버 컴포넌트는 `render()`가 아닌 직접 호출로 테스트 (`await ServerComp()`)
- `userEvent`는 비동기이므로 `await` 필수 — `fireEvent`와 혼용 시 타이밍 버그
- MSW 핸들러는 `afterEach(() => server.resetHandlers())`로 격리 — 누적되면 테스트 오염
- Next.js의 `next/navigation`은 `vi.mock`으로 반드시 목킹 — mock 없이 import하면 에러

---

## Related

- [[_MOC]] — FE 전체 지도
- [[코드-품질-패키지]] — Vitest가 포함된 코드 품질 도구 전체 목록
- [[../../FE/nextjs/_MOC]] — Next.js 서버/클라이언트 컴포넌트 구조

## Sources

- [Vitest 공식 문서](https://vitest.dev/)
- [Testing Library 쿼리 우선순위](https://testing-library.com/docs/queries/about#priority)
- [MSW 공식 문서](https://mswjs.io/)
