---
title: Props로 데이터 전달하기
aliases: [props, 프롭스, defaultProps, children props]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/react, status/budding]
notion-url: https://www.notion.so/aa1cf7da444641fa8684e556e15a8de4
related:
  - "[[_MOC]]"
  - "[[state]]"
  - "[[이벤트-처리]]"
source: ["Notion: React"]
migrated-from: "Notion: Props로 데이터 전달하기"
---

# Props로 데이터 전달하기

> TL;DR: Props는 부모 → 자식 단방향 데이터 전달 메커니즘. 구조분해 할당, spread 연산자, children, defaultProps를 조합해 유연하게 활용한다.

## What

부모 컴포넌트가 자식 컴포넌트에 데이터를 전달하는 메커니즘. 함수의 인자와 유사.

## Why it matters

컴포넌트를 재사용 가능한 단위로 분리하기 위한 핵심 개념. props 없이는 모든 값을 하드코딩해야 한다.

## How

**방법 1 - 점 표기법**:
```javascript
export default function Button(props) {
    return <button style={{color: props.color}}>{props.text}</button>;
}
// 부모에서: <Button text="메일" color="red" />
```

**방법 2 - 구조분해 할당**:
```javascript
export default function Button({text, color}) {
    return <button style={{color}}>{text}</button>;
}
```

**Spread 연산자로 전달**:
```javascript
const buttonProps = { text: "메일", color: "red" };
<Button {...buttonProps} />
```

**children props** (HTML/컴포넌트 전달):
```javascript
export default function Button({text, color, children}) {
    return <button style={{color}}>{text}{children}</button>;
}
// 부모에서:
<Button text="카페"><div>야하하</div></Button>
```

**defaultProps**: props 누락 시 기본값
```javascript
Button.defaultProps = { color: "white" };
```

## Pitfalls

- `props.color.toUpperCase()` 처럼 메서드 호출 시 color가 undefined면 에러 → defaultProps 설정
- props는 읽기 전용 (자식에서 직접 수정 불가)

## Related

- [[_MOC]]
- [[state]]
- [[이벤트-처리]]
- [[props로-state-전달]]

## Sources

- Notion: Props로 데이터 전달하기
