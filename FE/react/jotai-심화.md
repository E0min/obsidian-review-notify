---
title: Jotai 심화
aliases: [Jotai, jotai, 조타이, atom, atomFamily, derived atom]
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
  - "[[zustand-심화]]"
source: []
migrated-from: ""
---

# Jotai 심화

> TL;DR: Jotai는 atom 단위로 상태를 쪼개어 각 atom을 구독한 컴포넌트만 리렌더한다. Recoil의 정신적 계승자지만 더 단순하며, 파생 atom과 비동기 atom으로 복잡한 상태 조합을 선언적으로 표현한다.

---

## What

Jotai의 핵심 철학: **상태를 작게 쪼갠다 (bottom-up)**. 큰 store 하나 대신, 필요한 단위만큼 atom을 만들고 파생시켜 연결한다.

```
Zustand: 하나의 큰 store → selector로 조각 구독
Jotai:   작은 atom들 → 파생 atom으로 조합
```

---

## 기본 atom

```typescript
import { atom, useAtom, useAtomValue, useSetAtom } from 'jotai';

// 기본 atom — 읽기/쓰기 가능
const countAtom = atom(0);
const nameAtom = atom('영민');
const userAtom = atom<User | null>(null);

// 컴포넌트에서 사용
function Counter() {
  const [count, setCount] = useAtom(countAtom);       // [value, setter]
  const name = useAtomValue(nameAtom);                // 읽기 전용
  const setUser = useSetAtom(userAtom);               // 쓰기 전용 (구독 안 함)

  return (
    <button onClick={() => setCount((c) => c + 1)}>
      {name}: {count}
    </button>
  );
}
```

**`useAtomValue` vs `useSetAtom`**:
- `useAtomValue`: 값만 읽음 → atom 변경 시 리렌더
- `useSetAtom`: setter만 → atom 변경해도 이 컴포넌트는 **리렌더 안 함** (성능 최적화 핵심)

---

## 파생 atom (Derived Atom)

### 읽기 전용 파생

```typescript
const todosAtom = atom<Todo[]>([]);

// 파생 — todos에서 계산
const completedTodosAtom = atom((get) => get(todosAtom).filter((t) => t.done));
const pendingCountAtom = atom((get) => get(todosAtom).filter((t) => !t.done).length);

// 여러 atom 조합
const userAtom = atom<User | null>(null);
const isAdminAtom = atom((get) => get(userAtom)?.role === 'admin');

// 컴포넌트에서
const completedTodos = useAtomValue(completedTodosAtom); // 읽기만
```

### 읽기/쓰기 파생

```typescript
const temperatureAtom = atom(0); // 섭씨

// 읽기(파씨 변환) + 쓰기(파씨로 세팅)
const fahrenheitAtom = atom(
  (get) => get(temperatureAtom) * 9 / 5 + 32,           // getter
  (get, set, fahrenheit: number) => {                    // setter
    set(temperatureAtom, (fahrenheit - 32) * 5 / 9);
  }
);

function TemperatureConverter() {
  const [celsius, setCelsius] = useAtom(temperatureAtom);
  const [fahrenheit, setFahrenheit] = useAtom(fahrenheitAtom);

  return (
    <>
      <input value={celsius} onChange={(e) => setCelsius(Number(e.target.value))} />
      <input value={fahrenheit} onChange={(e) => setFahrenheit(Number(e.target.value))} />
    </>
  );
}
```

---

## 비동기 atom

```typescript
// 비동기 fetch atom
const userAtom = atom(async () => {
  const res = await fetch('/api/user');
  return res.json() as Promise<User>;
});

// Suspense와 함께 사용
function UserInfo() {
  const user = useAtomValue(userAtom); // Suspense가 로딩 처리
  return <div>{user.name}</div>;
}

// 상위 컴포넌트
function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <UserInfo />
    </Suspense>
  );
}
```

### loadable — Suspense 없이 비동기 처리

```typescript
import { loadable } from 'jotai/utils';

const userLoadableAtom = loadable(userAtom);

function UserInfo() {
  const userLoadable = useAtomValue(userLoadableAtom);

  if (userLoadable.state === 'loading') return <Spinner />;
  if (userLoadable.state === 'hasError') return <div>에러 발생</div>;
  return <div>{userLoadable.data.name}</div>;
}
```

---

## atomFamily — 동적 atom 생성

같은 구조지만 ID별로 독립된 atom이 필요할 때:

```typescript
import { atomFamily } from 'jotai/utils';

// ID별 todo atom 생성
const todoAtomFamily = atomFamily((id: string) =>
  atom<Todo>({ id, text: '', done: false })
);

// 각 TodoItem이 자신의 atom만 구독
function TodoItem({ id }: { id: string }) {
  const [todo, setTodo] = useAtom(todoAtomFamily(id));

  return (
    <div>
      <input
        checked={todo.done}
        onChange={() => setTodo((t) => ({ ...t, done: !t.done }))}
        type="checkbox"
      />
      {todo.text}
    </div>
  );
}
```

---

## 유틸리티 atom

### atomWithStorage — localStorage 영속화

```typescript
import { atomWithStorage } from 'jotai/utils';

const themeAtom = atomWithStorage<'light' | 'dark'>('theme', 'light');
// localStorage 'theme' 키에 자동 저장/복원
```

### atomWithReset — 초기값으로 리셋

```typescript
import { atomWithReset, useResetAtom } from 'jotai/utils';

const formAtom = atomWithReset({ email: '', password: '' });

function LoginForm() {
  const [form, setForm] = useAtom(formAtom);
  const resetForm = useResetAtom(formAtom);

  return (
    <>
      <input value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
      <button onClick={resetForm}>초기화</button>
    </>
  );
}
```

### selectAtom — 파생 + 메모이제이션

```typescript
import { selectAtom } from 'jotai/utils';

const userAtom = atom<User>({ name: '영민', age: 28, role: 'admin' });

// 특정 필드만 구독 (얕은 비교)
const userNameAtom = selectAtom(userAtom, (user) => user.name);
// user.age가 바뀌어도 userNameAtom 구독 컴포넌트는 리렌더 안 함
```

---

## Provider 설정 (선택적)

```typescript
import { Provider, createStore } from 'jotai';

// Provider 없이도 동작 (전역 기본 store 사용)
// 격리된 store가 필요할 때 (테스트, 위젯 등)
const myStore = createStore();

function App() {
  return (
    <Provider store={myStore}>
      <Component />
    </Provider>
  );
}
```

테스트에서 atom 상태 격리:

```typescript
// test
const testStore = createStore();
testStore.set(countAtom, 10); // 초기 상태 세팅

render(
  <Provider store={testStore}>
    <Counter />
  </Provider>
);
```

---

## Jotai vs Zustand

| | Jotai | Zustand |
|--|-------|---------|
| 상태 단위 | atom (작게 분리) | store (한 객체) |
| 구독 | atom 단위 리렌더 | selector 기반 |
| 파생 상태 | 파생 atom (선언적) | selector 함수 |
| 비동기 | async atom + Suspense | 직접 async action |
| 타입 추론 | atom 타입에서 자동 | store interface 명시 |
| 적합 | 세밀한 리렌더 최적화, 복잡한 파생 관계 | 빠른 전역 상태 설정 |

---

## Pitfalls

- **atom을 컴포넌트 안에서 정의**: 렌더마다 새 atom 생성 → 항상 모듈 레벨에서 정의
- **비동기 atom의 에러 처리**: Suspense + ErrorBoundary 쌍으로, 또는 `loadable` 사용
- **atomFamily 메모리 누수**: 무한정 atom 생성 → `atomFamily`의 remove 메서드로 정리
- **Provider 중첩 버그**: 같은 atom이 다른 Provider scope에서 다른 값 — 의도적이지 않으면 최상위 Provider 하나만

---

## Related

- [[상태관리]] — 라이브러리 비교 허브
- [[상태-분류]] — atom 단위 상태 분류 기준
- [[zustand-심화]] — store 기반 대안

## Sources

- [Jotai 공식 문서](https://jotai.org/)
- [Jotai vs Zustand vs Recoil 비교](https://jotai.org/docs/basics/comparison)
