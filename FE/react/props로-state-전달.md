---
title: Props로 State 전달하기
aliases: [state lifting, 상태 끌어올리기, 리렌더링 최적화]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/react, status/budding]
notion-url: https://www.notion.so/e0c0a62166ad45e7975abe6a4e15b7ec
related:
  - "[[_MOC]]"
  - "[[state]]"
  - "[[useRef]]"
source: ["Notion: React"]
migrated-from: "Notion: Props로 State 전달하기"
---

# Props로 State 전달하기

> TL;DR: 부모의 state를 자식에게 props로 내려주는 패턴. 독립적인 state는 각 컴포넌트로 분리해 불필요한 리렌더링을 방지한다.

## What

부모의 state를 자식에게 props로 전달하는 패턴 + 리렌더링 최적화 방법.

## Why it matters

state를 어느 레벨에서 관리하느냐에 따라 불필요한 리렌더링이 발생할 수 있다. 컴포넌트 분리 설계의 핵심 패턴.

## How

```javascript
const Bulb = ({ light }) => (
    <div>
        {light === "ON" ? <h1 style={{backgroundColor:"orange"}}>켜짐</h1>
                       : <h1 style={{backgroundColor:"grey"}}>꺼짐</h1>}
    </div>
);

function App() {
    const [light, setLight] = useState("OFF");
    return (
        <>
            <Bulb light={light}/>
            <button onClick={() => setLight(light === "ON" ? "OFF" : "ON")}>
                {light}
            </button>
        </>
    );
}
```

**리렌더링 최적화** — 독립적인 state는 별도 컴포넌트로 분리:
```javascript
// 나쁨: 하나의 App에 모든 state → count 변경 시 Bulb도 리렌더링
// 좋음: Bulb 컴포넌트 안에서 light state 관리, Counter 컴포넌트에서 count 관리
// App은 조합만 담당
```

## Pitfalls

- `props` 전달 값을 일반 변수로 하면 React가 상태변화 감지 못함 → 반드시 state
- 부모 리렌더링 시 자식도 리렌더링 → 불필요한 리렌더링 방지 위해 상태를 적절한 레벨에서 관리

## Related

- [[_MOC]]
- [[state]]
- [[props]]
- [[useRef]]

## Sources

- Notion: Props로 State 전달하기
