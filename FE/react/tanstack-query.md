---
title: TanStack Query (React Query) — 서버 상태 관리
aliases: [TanStack Query, React Query, useQuery, useMutation, server state, 서버 상태]
type: concept
status: budding
created: 2026-05-25
updated: 2026-05-25
tags: [fe/react, status/budding]
notion-url: ""
related:
  - "[[_MOC]]"
  - "[[상태관리]]"
  - "[[상태-분류]]"
  - "[[../../FE/nextjs/앱라우터-데이터페칭]]"
source: []
migrated-from: ""
---

# TanStack Query (React Query) — 서버 상태 관리

> TL;DR: API 데이터를 useState+useEffect로 관리하는 패턴의 완전한 대체재. 캐싱·백그라운드 refetch·로딩/에러 상태·낙관적 업데이트를 자동 처리한다.

---

## What

서버에서 가져오는 데이터(Server State)는 **비동기, 공유, stale 가능**하다는 3가지 특성 때문에 클라이언트 상태(useState)와 다르게 다뤄야 한다.

TanStack Query는 이 문제를 해결하는 **서버 상태 전용 캐시 레이어**:

```
API 응답 → TanStack Query Cache → 컴포넌트
```

---

## 설치 및 기본 세팅

```typescript
// providers.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,   // 1분 — 이 시간 안에는 refetch 안 함
      retry: 2,                // 실패 시 2회 재시도
    },
  },
});

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

---

## useQuery — 데이터 조회

```typescript
import { useQuery } from '@tanstack/react-query';

interface User {
  id: string;
  name: string;
  email: string;
}

async function fetchUser(userId: string): Promise<User> {
  const res = await fetch(`/api/users/${userId}`);
  if (!res.ok) throw new Error('User fetch failed');
  return res.json();
}

function UserProfile({ userId }: { userId: string }) {
  const {
    data: user,
    isLoading,
    isError,
    error,
    isFetching,  // 백그라운드 refetch 중
    refetch,
  } = useQuery({
    queryKey: ['user', userId],         // 캐시 키 (변경 시 refetch)
    queryFn: () => fetchUser(userId),
    staleTime: 5 * 60 * 1000,          // 5분
    enabled: !!userId,                  // userId 없으면 실행 안 함
  });

  if (isLoading) return <Spinner />;
  if (isError) return <div>에러: {error.message}</div>;

  return (
    <div>
      {isFetching && <small>업데이트 중...</small>}
      <h1>{user.name}</h1>
    </div>
  );
}
```

### queryKey 설계 원칙

```typescript
// 계층형 키 — 캐시 무효화 범위 조절 가능
['users']                        // 모든 user 쿼리
['users', userId]                // 특정 user
['users', userId, 'posts']       // 특정 user의 posts

// 필터 포함 — 필터 바뀌면 자동 refetch
['users', { status: 'active', page: 2 }]
```

---

## useMutation — 데이터 변경 (POST/PUT/DELETE)

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';

async function updateUser(data: { id: string; name: string }) {
  const res = await fetch(`/api/users/${data.id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
  return res.json();
}

function EditUserForm({ userId }: { userId: string }) {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: updateUser,
    onSuccess: (updatedUser) => {
      // 캐시 무효화 → 자동 refetch
      queryClient.invalidateQueries({ queryKey: ['user', userId] });
    },
    onError: (error) => {
      console.error('업데이트 실패:', error);
    },
  });

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      mutation.mutate({ id: userId, name: 'New Name' });
    }}>
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? '저장 중...' : '저장'}
      </button>
    </form>
  );
}
```

---

## Optimistic Update — 낙관적 업데이트

서버 응답 전에 UI를 미리 변경해서 즉각적인 피드백 제공:

```typescript
const mutation = useMutation({
  mutationFn: toggleTodo,
  onMutate: async (todoId) => {
    // 1. 진행 중인 refetch 취소 (낙관적 업데이트가 덮어쓰이지 않도록)
    await queryClient.cancelQueries({ queryKey: ['todos'] });

    // 2. 이전 값 스냅샷 (롤백용)
    const previousTodos = queryClient.getQueryData(['todos']);

    // 3. 낙관적으로 캐시 업데이트
    queryClient.setQueryData(['todos'], (old: Todo[]) =>
      old.map((todo) =>
        todo.id === todoId ? { ...todo, done: !todo.done } : todo
      )
    );

    return { previousTodos }; // context로 전달
  },
  onError: (err, todoId, context) => {
    // 4. 실패 시 롤백
    queryClient.setQueryData(['todos'], context?.previousTodos);
  },
  onSettled: () => {
    // 5. 성공/실패 관계없이 최종 서버 상태로 동기화
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});
```

---

## 캐시 조작

```typescript
const queryClient = useQueryClient();

// 수동 데이터 세팅 (API 응답으로 미리 채우기)
queryClient.setQueryData(['user', userId], updatedUser);

// 캐시 읽기
const user = queryClient.getQueryData(['user', userId]);

// 특정 쿼리 무효화 (stale 표시 → 다음 접근 시 refetch)
queryClient.invalidateQueries({ queryKey: ['user', userId] });

// 특정 prefix 전체 무효화
queryClient.invalidateQueries({ queryKey: ['users'] }); // ['users', *] 전체

// 강제 refetch
queryClient.refetchQueries({ queryKey: ['user', userId] });

// 캐시에서 제거
queryClient.removeQueries({ queryKey: ['user', userId] });
```

---

## Infinite Query — 무한 스크롤

```typescript
import { useInfiniteQuery } from '@tanstack/react-query';

function PostList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: ['posts'],
    queryFn: ({ pageParam = 0 }) => fetchPosts({ cursor: pageParam, limit: 20 }),
    getNextPageParam: (lastPage) => lastPage.nextCursor ?? undefined,
    initialPageParam: 0,
  });

  const posts = data?.pages.flatMap((page) => page.posts) ?? [];

  return (
    <div>
      {posts.map((post) => <PostCard key={post.id} post={post} />)}
      <button
        onClick={() => fetchNextPage()}
        disabled={!hasNextPage || isFetchingNextPage}
      >
        {isFetchingNextPage ? '로딩 중...' : '더 보기'}
      </button>
    </div>
  );
}
```

---

## Prefetch — 미리 데이터 로드

```typescript
// 호버 시 미리 fetch → 클릭 시 즉시 표시
function UserLink({ userId }: { userId: string }) {
  const queryClient = useQueryClient();

  return (
    <a
      href={`/users/${userId}`}
      onMouseEnter={() => {
        queryClient.prefetchQuery({
          queryKey: ['user', userId],
          queryFn: () => fetchUser(userId),
          staleTime: 10 * 1000,
        });
      }}
    >
      유저 프로필
    </a>
  );
}
```

---

## Next.js App Router 통합 — Server-side Prefetch

```typescript
// page.tsx (서버 컴포넌트)
import { dehydrate, HydrationBoundary, QueryClient } from '@tanstack/react-query';

export default async function Page({ params }: { params: { id: string } }) {
  const queryClient = new QueryClient();

  // 서버에서 미리 fetch → 클라이언트 hydration
  await queryClient.prefetchQuery({
    queryKey: ['user', params.id],
    queryFn: () => fetchUser(params.id),
  });

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <UserProfile userId={params.id} /> {/* 클라이언트 컴포넌트 */}
    </HydrationBoundary>
  );
}
```

---

## staleTime vs gcTime

```
staleTime: 데이터가 "신선"한 시간
  → 이 시간 안에는 refetch 안 함 (캐시 그대로 사용)
  → 기본: 0 (항상 stale)

gcTime (구 cacheTime): 캐시가 메모리에 유지되는 시간
  → 쿼리를 구독하는 컴포넌트가 없어진 후 이 시간 뒤 가비지 컬렉션
  → 기본: 5분

예시:
- staleTime: 5분 → 5분 안에 같은 페이지 재방문 시 즉시 표시 (refetch 없음)
- staleTime: 0, gcTime: 0 → 컴포넌트 마운트마다 무조건 fetch
- staleTime: Infinity → 수동 invalidate 전까지 절대 refetch 안 함 (정적 데이터)
```

---

## useState + useEffect vs TanStack Query

```typescript
// ❌ 수동 서버 상태 관리 — 50줄
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    setLoading(true);
    fetchUser(userId)
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [userId]);

  // 캐싱? 없음. refetch? 없음. 중복 요청 제거? 없음. 백그라운드 갱신? 없음.
  // ...
}

// ✅ TanStack Query — 10줄
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });
  // 캐싱, 중복 제거, 백그라운드 갱신, 재시도 모두 자동
  // ...
}
```

---

## Pitfalls

- **queryKey를 string 하나로**: `['users']` vs `'users'` → string key는 배열로 wrap됨, 일관성 위해 항상 배열
- **mutate와 mutateAsync 혼동**: `mutate`는 void 반환, `mutateAsync`는 Promise 반환 (await 가능)
- **staleTime 0 (기본값)**: 매 렌더마다 background refetch → `staleTime: 5 * 60 * 1000` 권장
- **enabled 없이 optional 파라미터**: `queryFn`에서 undefined 파라미터 → `enabled: !!param`으로 guard
- **중복 QueryClient**: 앱당 하나만 — 컴포넌트 안에서 `new QueryClient()` 금지

---

## Related

- [[상태-분류]] — 언제 TanStack Query vs 다른 상태 관리
- [[상태관리]] — 라이브러리 비교 허브
- [[../../FE/nextjs/앱라우터-데이터페칭]] — Next.js App Router에서 서버 fetch

## Sources

- [TanStack Query 공식 문서](https://tanstack.com/query/latest)
- [TkDodo — Practical React Query 시리즈](https://tkdodo.eu/blog/practical-react-query)
- [TkDodo — Inside React Query](https://tkdodo.eu/blog/inside-react-query)
