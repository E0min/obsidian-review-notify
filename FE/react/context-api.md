---
title: Context API
aliases: [Context API, createContext, useContext, Provider, 컨텍스트 API]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/react, status/budding]
notion-url: ""
related:
  - "[[_MOC]]"
  - "[[상태관리]]"
  - "[[useReducer]]"
source: ["Notion: JavaScript"]
migrated-from: "Notion: Context API"
---

# Context API

> TL;DR: `createContext` → `Provider`로 감싸서 값 제공 → `useContext`로 어디서든 소비. prop drilling 없이 트리 전체에 값을 내려줄 수 있지만, 값이 바뀌면 구독한 **모든** 컴포넌트가 리렌더된다.

---

## What

React 컴포넌트 트리 안에서 prop을 단계별로 전달하지 않고 데이터를 공유하는 내장 메커니즘. 외부 라이브러리 없이 테마, 언어(i18n), 인증 사용자 정보 같은 **전역적이지만 자주 바뀌지 않는 값**에 적합하다.

---

## How

### 기본 3단계

```typescript
// 1. Context 생성
const ThemeContext = createContext<'light' | 'dark'>('light'); // 기본값

// 2. Provider로 값 공급
function App() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  return (
    <ThemeContext.Provider value={theme}>
      <ChildComponent />
    </ThemeContext.Provider>
  );
}

// 3. useContext로 소비 (어디서든, Provider 안에만 있으면 됨)
function ChildComponent() {
  const theme = useContext(ThemeContext);
  return <div className={theme}>...</div>;
}
```

### 실전 — ThemeContext 토글

```typescript
// ThemeContext.tsx
import { createContext, useContext, useState, ReactNode } from 'react';

type Theme = 'light' | 'dark';

interface ThemeContextType {
  theme: Theme;
  toggle: () => void;
}

// 타입 안전한 context: null 초기값 + 커스텀 훅에서 null 가드
const ThemeContext = createContext<ThemeContextType | null>(null);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>('light');

  return (
    <ThemeContext.Provider value={{ theme, toggle: () => setTheme((t) => (t === 'light' ? 'dark' : 'light')) }}>
      {children}
    </ThemeContext.Provider>
  );
}

// null 가드를 커스텀 훅 안으로 캡슐화 (사용처에서 null 체크 불필요)
export function useTheme(): ThemeContextType {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useTheme must be used within <ThemeProvider>');
  return ctx;
}

// 사용
function Header() {
  const { theme, toggle } = useTheme();
  return <button onClick={toggle}>현재: {theme}</button>;
}
```

### Context 여러 개 조합

```typescript
// 관심사별로 Context 분리 → 불필요한 리렌더 방지
function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <LocaleProvider>
          <Router />
        </LocaleProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}
```

### 값 최적화 — useMemo로 리렌더 방지

```typescript
function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  // 매 렌더마다 새 객체를 만들면 하위 전체 리렌더 → useMemo로 안정화
  const value = useMemo(() => ({ user, setUser }), [user]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
```

---

## Why it matters

**Prop drilling 문제**:

```
App
 └─ Layout → Header → UserAvatar  (user 필요)
                └─ Nav → LoginButton  (user 필요)
```

`user`를 App → Layout → Header → UserAvatar로 4단계 전달해야 하는 대신, Context를 쓰면 `UserAvatar`와 `LoginButton`이 직접 `useContext(AuthContext)`로 가져온다.

---

## Pitfalls

- **잦은 업데이트 금지**: Context value가 바뀌면 `useContext`를 호출한 **모든 컴포넌트가 리렌더**됨. 폼 입력, 마우스 위치, 타이머처럼 자주 바뀌는 값은 Zustand/Jotai 사용
- **기본값 함정**: `createContext(defaultValue)` 기본값은 Provider **없이** 소비할 때만 사용됨. Provider를 쓰면 기본값은 무시됨 → `null` 초기화 + 커스텀 훅 null 가드 패턴 권장
- **Provider 위치**: Provider가 소비 컴포넌트보다 상위에 있어야 함. 같은 레벨이나 하위에 두면 Context 못 찾음
- **Context 과분리**: Context를 너무 잘게 쪼개면 Provider 중첩 지옥. 실제로 함께 바뀌는 값은 하나의 Context로 묶기

---

## Related

- [[_MOC]] — React 전체 지도
- [[상태관리]] — Zustand/Jotai/RTK와 Context 비교·선택 가이드
- [[useReducer]] — Context + useReducer 조합으로 Redux-like 패턴 구현

## Sources

- [React 공식 문서 — createContext](https://react.dev/reference/react/createContext)
- [React 공식 문서 — useContext](https://react.dev/reference/react/useContext)
