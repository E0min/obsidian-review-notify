---
title: React App 구동원리
aliases: [React 구동, main.jsx, ReactDOM, 렌더링 진입점]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/react, status/budding]
notion-url: https://www.notion.so/9882ca43fd4c4ba6a3b66b1486172c2b
related:
  - "[[_MOC]]"
  - "[[state]]"
source: ["Notion: React"]
migrated-from: "Notion: React App 구동원리"
---

# React App 구동원리

> TL;DR: Vite 기반 React 앱은 `index.html` → `main.jsx` → `ReactDOM.createRoot` → `.render(<App />)` 순서로 진입해 id=root 요소에 동적으로 마운트된다.

## What

Vite 기반 React 앱이 어떻게 구동되는지의 진입점 흐름.

## Why it matters

진입점 구조를 이해해야 라우팅, 전역 Provider 설정, StrictMode 관리 등 앱 최상단 설정을 올바르게 구성할 수 있다.

## How

1. `index.html` → `<script type="module" src="/src/main.jsx">` 로딩
2. `main.jsx`에서 `ReactDOM.createRoot(document.getElementById('root'))` — id=root 요소에 React 마운트
3. `.render(<App />)` — App 컴포넌트 렌더링

```javascript
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
```

`index.html`에는 실제 HTML 태그 없음 → JS가 동적으로 생성.

ESLint 설정: `"no-unused-vars": "off"`, `"react/prop-types": "off"` 추가 권장.

## Pitfalls

- 개발자 도구에서 HTML 태그 안 보이는 건 정상 → JS 동적 생성
- `createRoot` → React 18+. 구버전은 `ReactDOM.render()`

## Related

- [[_MOC]]
- [[state]]
- [[react-앱-만들기]]

## Sources

- Notion: React App 구동원리
