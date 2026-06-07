---
title: Context API
aliases: [Context, useContext, createContext, props drilling]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/react, status/budding]
notion-url: https://www.notion.so/575df72ed4de4624b02f2d5e5d03aa00
related:
  - "[[_MOC]]"
  - "[[state]]"
  - "[[useReducer]]"
source: ["Notion: React"]
migrated-from: "Notion: Context API"
---

# Context API

> TL;DR: 컴포넌트 트리 어디서든 데이터를 직접 꺼내 쓸 수 있게 해주는 전역 상태 공유 API. Props drilling 문제를 해결한다.

## What

컴포넌트 트리 전체에 전역 데이터를 제공하는 API. Props drilling 해결.

## Why it matters

깊은 컴포넌트 계층에서 사용자 인증, 테마, 언어 설정 등을 중간 컴포넌트를 거치지 않고 직접 전달. 중간 컴포넌트들이 자신과 무관한 props를 단순히 전달만 하는 drilling 문제를 없앤다.

## How

```javascript
// 1. Context 생성 (컴포넌트 외부에 선언)
const ThemeContext = createContext();

// 2. Provider로 감싸기
export function ThemeProvider({ children }) {
    const [theme, setTheme] = useState('light');
    const toggleTheme = () => setTheme(prev => prev === 'light' ? 'dark' : 'light');

    return (
        <ThemeContext.Provider value={{ theme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
}

// 3. 하위 컴포넌트에서 사용
function ThemeButton() {
    const { theme, toggleTheme } = useContext(ThemeContext);
    return <button onClick={toggleTheme}>{theme}</button>;
}

// 4. App에서 Provider 적용
<ThemeProvider><ThemeButton /></ThemeProvider>
```

## Pitfalls

- Context는 컴포넌트 **외부**에 생성 → 컴포넌트 내부에 선언하면 리렌더링마다 재생성됨
- Context 값이 변경되면 `useContext`를 구독하는 **모든** 컴포넌트가 리렌더링됨 → 자주 바뀌는 값에는 부적합
- 자주 변하는 데이터(장바구니, 실시간 데이터 등)에는 Redux / Zustand 등이 더 적합
- `createContext(defaultValue)` 의 기본값은 Provider 없이 사용할 때만 적용됨

## Related

- [[state]] — 로컬 상태 관리
- [[useReducer]] — 복잡한 상태 로직, Context와 함께 자주 사용
- [[_MOC]]

## Sources

- [React 공식 문서 — createContext](https://react.dev/reference/react/createContext)
- [React 공식 문서 — useContext](https://react.dev/reference/react/useContext)
- Notion: React
