---
title: useReducer
aliases: [useReducer, reducer, dispatch, action, 리듀서]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/react, status/budding]
notion-url: https://www.notion.so/890bf40f7baa413a853aefea1ef3d5a2
related:
  - "[[_MOC]]"
  - "[[state]]"
  - "[[useReducer-vs-useState]]"
  - "[[상태관리]]"
  - "[[context-api]]"
source: ["Notion: React", "Notion: JavaScript"]
migrated-from: "Notion: useReducer"
---

# useReducer

> TL;DR: `(state, action) => newState` 순수 함수(reducer)로 상태 전이를 관리. 여러 하위 값이 얽힌 복잡한 상태 로직이나 "다음 상태가 이전 상태에 의존"하는 케이스에서 `useState`보다 명확하다.

## What

복잡한 상태 관리를 액션 기반으로 중앙화하는 훅. 상태와 업데이트 로직을 컴포넌트 밖 `reducer` 함수로 분리해서 상태 전이를 예측 가능하게 만든다.

```typescript
const [state, dispatch] = useReducer(reducer, initialState);
```

- `state` — 현재 상태
- `dispatch(action)` — reducer에 action을 전달해 새 상태 계산 트리거
- `reducer(state, action) => newState` — 순수 함수, 반드시 새 객체 반환

## How

### 카운터 예시

```typescript
type Action =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'reset' }
  | { type: 'incrementByAmount'; payload: number };

interface CounterState { count: number }

function counterReducer(state: CounterState, action: Action): CounterState {
  switch (action.type) {
    case 'increment':      return { count: state.count + 1 };
    case 'decrement':      return { count: state.count - 1 };
    case 'reset':          return { count: 0 };
    case 'incrementByAmount': return { count: state.count + action.payload };
    default: return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(counterReducer, { count: 0 });
  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+1</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-1</button>
      <button onClick={() => dispatch({ type: 'incrementByAmount', payload: 5 })}>+5</button>
      <button onClick={() => dispatch({ type: 'reset' })}>Reset</button>
    </div>
  );
}
```

### 폼 상태 관리 (복잡한 객체)

```typescript
interface FormState {
  name: string;
  email: string;
  isLoading: boolean;
  error: string | null;
}

type FormAction =
  | { type: 'setField'; field: 'name' | 'email'; value: string }
  | { type: 'submit' }
  | { type: 'success' }
  | { type: 'failure'; error: string };

function formReducer(state: FormState, action: FormAction): FormState {
  switch (action.type) {
    case 'setField':  return { ...state, [action.field]: action.value };
    case 'submit':    return { ...state, isLoading: true, error: null };
    case 'success':   return { ...state, isLoading: false };
    case 'failure':   return { ...state, isLoading: false, error: action.error };
    default: return state;
  }
}
```

### Context + useReducer 조합 (Redux-like 전역 상태)

```typescript
const StateContext = createContext<FormState | null>(null);
const DispatchContext = createContext<React.Dispatch<FormAction> | null>(null);

function FormProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(formReducer, initialState);
  return (
    <StateContext.Provider value={state}>
      <DispatchContext.Provider value={dispatch}>
        {children}
      </DispatchContext.Provider>
    </StateContext.Provider>
  );
}

// state와 dispatch를 분리 → dispatch만 필요한 컴포넌트는 state 변경 시 리렌더 없음
export const useFormState = () => useContext(StateContext)!;
export const useFormDispatch = () => useContext(DispatchContext)!;
```

## useState vs useReducer

| | `useState` | `useReducer` |
|--|------------|--------------|
| 적합한 상태 | 독립적인 단순 값 | 연관된 여러 값, 복잡한 전이 |
| 업데이트 로직 | 컴포넌트 안 | 컴포넌트 밖 (분리·재사용) |
| 테스트 | 컴포넌트 렌더 필요 | reducer 순수 함수만 테스트 가능 |
| 상태 필드 수 | 2개 이하 | 3개 이상 |
| 상태 추적 | 어려움 | action 로그로 명확 |

## Pitfalls

- **reducer에서 부수효과 금지**: API 호출, 타이머, 로컬스토리지 접근은 이벤트 핸들러나 `useEffect`에서
- **dispatch는 안정 참조**: React가 `dispatch`를 메모이즈하므로 useEffect 의존성 배열에 넣어도 무한 루프 없음
- **초기 상태 계산 비용**: 무거우면 세 번째 인자 `init` 함수 사용: `useReducer(reducer, arg, init)`
- **action 타입 오타**: TypeScript discriminated union으로 방지 (문자열 리터럴 타입 지정)

## Related

- [[state]] — useState 기본
- [[useReducer-vs-useState]] — 선택 기준 상세
- [[상태관리]] — Zustand/Jotai/RTK와 비교
- [[context-api]] — Context + useReducer 조합 패턴

## Sources

- [React 공식 문서 — useReducer](https://react.dev/reference/react/useReducer)
- [React 공식 문서 — useState vs useReducer](https://react.dev/learn/extracting-state-logic-into-a-reducer)
