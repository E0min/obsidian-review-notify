---
title: Zustand 심화
aliases: [Zustand, zustand, 주스탄드, zustand deep dive, zustand middleware]
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
  - "[[jotai-심화]]"
source: []
migrated-from: ""
---

# Zustand 심화

> TL;DR: Zustand는 Redux의 단순 버전 — 보일러플레이트 없이 store를 함수로 정의하고, 선택적 구독으로 불필요한 리렌더를 막는다. `persist`, `devtools`, `immer` 미들웨어로 기능 확장.

---

## What

React Context 없이 전역 상태를 관리하는 경량 라이브러리. `create()` 하나로 store를 정의하고, `useStore(selector)` 패턴으로 필요한 슬라이스만 구독한다.

**선택 이유**: Redux 대비 99% 적은 코드, Context 대비 선택적 구독으로 성능 우위.

---

## 기본 사용법

```typescript
import { create } from 'zustand';

interface CounterStore {
  count: number;
  increment: () => void;
  decrement: () => void;
  reset: () => void;
}

const useCounterStore = create<CounterStore>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}));

// 컴포넌트에서 사용
function Counter() {
  const count = useCounterStore((state) => state.count);         // count만 구독
  const increment = useCounterStore((state) => state.increment); // 액션은 안정적 참조

  return <button onClick={increment}>{count}</button>;
}
```

---

## 선택적 구독 — 성능 최적화 핵심

```typescript
// ❌ 전체 구독 — store 변경 시 항상 리렌더
const store = useUserStore();

// ✅ 선택적 구독 — count만 변할 때만 리렌더
const count = useUserStore((state) => state.count);

// ✅ 여러 값 — 객체 반환 시 얕은 비교 사용
import { shallow } from 'zustand/shallow';
const { name, email } = useUserStore(
  (state) => ({ name: state.name, email: state.email }),
  shallow  // 얕은 비교 (기본 referential equality 대신)
);
```

**원리**: selector가 반환하는 값이 `Object.is`로 이전 값과 같으면 리렌더 안 함.

---

## set과 get

```typescript
const useStore = create<Store>((set, get) => ({
  count: 0,
  user: null,

  // set: 상태 업데이트 (불변성 자동 처리)
  increment: () => set((state) => ({ count: state.count + 1 })),

  // get: 다른 상태 읽기 (액션 안에서)
  logCount: () => {
    const current = get().count;
    console.log('현재 count:', current);
  },

  // 여러 필드 동시 업데이트 (자동 merge)
  setUser: (user) => set({ user, lastUpdated: Date.now() }),

  // replace 모드 — merge 없이 전체 교체
  resetAll: () => set({ count: 0, user: null }, true), // 두 번째 인자 true
}));
```

---

## 미들웨어

### devtools — Redux DevTools 연동

```typescript
import { devtools } from 'zustand/middleware';

const useStore = create<Store>()(
  devtools(
    (set) => ({
      count: 0,
      increment: () => set({ count: 1 }, false, 'counter/increment'), // action name
    }),
    { name: 'CounterStore' } // DevTools에 표시될 이름
  )
);
```

### persist — localStorage/sessionStorage 영속화

```typescript
import { persist, createJSONStorage } from 'zustand/middleware';

interface AuthStore {
  user: User | null;
  token: string | null;
  setAuth: (user: User, token: string) => void;
  logout: () => void;
}

const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      setAuth: (user, token) => set({ user, token }),
      logout: () => set({ user: null, token: null }),
    }),
    {
      name: 'auth-storage',           // localStorage key
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({       // 저장할 필드만 선택
        token: state.token,           // user 객체는 저장 안 함 (재로그인 시 refetch)
      }),
    }
  )
);
```

### immer — 불변성 없이 뮤테이션 스타일 작성

```typescript
import { immer } from 'zustand/middleware/immer';

interface TodoStore {
  todos: { id: string; text: string; done: boolean }[];
  toggle: (id: string) => void;
  addTodo: (text: string) => void;
}

const useTodoStore = create<TodoStore>()(
  immer((set) => ({
    todos: [],
    toggle: (id) =>
      set((state) => {
        const todo = state.todos.find((t) => t.id === id);
        if (todo) todo.done = !todo.done; // 직접 뮤테이션 (immer가 불변으로 처리)
      }),
    addTodo: (text) =>
      set((state) => {
        state.todos.push({ id: crypto.randomUUID(), text, done: false });
      }),
  }))
);
```

### 미들웨어 조합

```typescript
const useStore = create<Store>()(
  devtools(
    persist(
      immer((set) => ({
        // ...
      })),
      { name: 'my-store' }
    ),
    { name: 'MyStore' }
  )
);
```

미들웨어 순서: 바깥 → 안. `devtools`가 가장 바깥에 오는 게 일반적.

---

## TypeScript 타입 패턴

```typescript
// 상태와 액션 분리
interface State {
  count: number;
  user: User | null;
}

interface Actions {
  increment: () => void;
  setUser: (user: User) => void;
  reset: () => void;
}

type Store = State & Actions;

const useStore = create<Store>()((set) => ({
  // State
  count: 0,
  user: null,

  // Actions
  increment: () => set((s) => ({ count: s.count + 1 })),
  setUser: (user) => set({ user }),
  reset: () => set({ count: 0, user: null }),
}));

// 타입에서 상태만 추출
type StoreState = ReturnType<typeof useStore.getState>;
```

---

## Slice 패턴 — 대규모 store 분리

```typescript
// counter.slice.ts
interface CounterSlice {
  count: number;
  increment: () => void;
}

const createCounterSlice = (set: SetState<Store>): CounterSlice => ({
  count: 0,
  increment: () => set((s) => ({ count: s.count + 1 })),
});

// user.slice.ts
interface UserSlice {
  user: User | null;
  setUser: (user: User) => void;
}

const createUserSlice = (set: SetState<Store>): UserSlice => ({
  user: null,
  setUser: (user) => set({ user }),
});

// store.ts — slice 합성
type Store = CounterSlice & UserSlice;

const useStore = create<Store>()((...a) => ({
  ...createCounterSlice(...a),
  ...createUserSlice(...a),
}));
```

---

## Store 외부에서 접근 (React 밖)

```typescript
// 컴포넌트 외부 (이벤트 핸들러, utility 함수 등)
const store = useStore.getState();
store.increment();

// 구독
const unsubscribe = useStore.subscribe(
  (state) => state.count, // selector
  (count) => console.log('count changed:', count) // listener
);
// 해제
unsubscribe();
```

---

## Zustand vs Context API

| | Zustand | Context |
|--|---------|---------|
| 보일러플레이트 | 최소 | createContext + Provider + custom hook |
| 선택적 구독 | ✅ selector | ❌ Provider 내 전체 리렌더 |
| 미들웨어 | persist, devtools, immer | 직접 구현 |
| 비동기 액션 | 그냥 async function | 별도 처리 |
| 적합 | 중간 규모 전역 상태 | 테마/언어 같은 정적 설정 |

---

## Pitfalls

- **selector 없이 전체 구독**: `const store = useStore()` → store 어디든 변경 시 리렌더
- **액션을 외부에서 직접 생성**: store 내부에서 정의하지 않으면 추적 어려움
- **persist 전체 저장**: 큰 객체를 통째로 localStorage에 → `partialize`로 필요한 필드만
- **미들웨어 없이 replace**: `set(newState, true)` 남발 → 다른 슬라이스 상태 날아감
- **서버 컴포넌트에서 사용**: Zustand는 클라이언트 전용 — `'use client'` 경계 안에서만

---

## Related

- [[상태관리]] — 라이브러리 비교 허브
- [[상태-분류]] — 어떤 상태를 전역으로 올릴 것인가 판단
- [[jotai-심화]] — atom 기반 대안

## Sources

- [Zustand 공식 문서](https://zustand.docs.pmnd.rs/)
- [Zustand GitHub — TypeScript 가이드](https://github.com/pmndrs/zustand)
- [TkDodo — Working with Zustand](https://tkdodo.eu/blog/working-with-zustand)
