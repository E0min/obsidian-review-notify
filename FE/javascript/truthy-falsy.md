---
title: Truthy와 Falsy
aliases: [truthy, falsy, 불린 변환]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/javascript, status/budding]
notion-url: https://www.notion.so/fec04108375e411fafea112cf798756c
related:
  - "[[_MOC]]"
  - "[[단락-평가]]"
source: ["Notion: JavaScript"]
migrated-from: "Notion: Truthy와 Falsy"
---

# Truthy와 Falsy

> TL;DR: 자바스크립트에서 불린 문맥에 사용될 때 false로 평가되는 Falsy 값 8개를 제외한 모든 값은 Truthy다.

## What

자바스크립트는 조건문처럼 불린(Boolean)이 필요한 문맥에서 값을 자동으로 `true` 또는 `false`로 변환한다.

- **Falsy 값 (총 8개)**: `false`, `0`, `-0`, `0n` (BigInt 0), `""` (빈 문자열), `null`, `undefined`, `NaN`
- **Truthy 값**: falsy가 아닌 모든 것. 빈 객체 `{}`, 빈 배열 `[]`, 함수도 truthy다.

## Why it matters

조건 체크를 간결하게 작성할 수 있고, `||` 연산자를 이용한 기본값 패턴이 JS 전반에서 널리 쓰인다. 단, 의도치 않은 falsy 처리로 버그가 생기기 쉬우므로 정확히 이해해야 한다.

## How

```javascript
// 조건문에서 if(data) 패턴
let data = "";
if (data) {
    console.log("실행 안됨");
} else {
    console.log("데이터가 없습니다."); // 이 줄 실행됨
}

// || 연산자로 기본값 설정
let myName = userName || "익명 사용자";
```

빈 배열과 빈 객체는 truthy임에 주의:

```javascript
if ([]) console.log("빈 배열도 truthy");  // 실행됨
if ({}) console.log("빈 객체도 truthy");  // 실행됨
```

## Pitfalls

- `0`이나 `""` 같은 **유효한 값도 falsy**로 처리된다. 예를 들어 수량이 0인 경우를 처리해야 할 때 `if (count)` 로 쓰면 0을 걸러버린다.
- 이런 경우엔 `??` (nullish coalescing 연산자)를 사용해 `null` / `undefined`만 걸러야 한다.

```javascript
// 잘못된 패턴: 0이 입력되면 "기본값"이 할당됨
let count = inputCount || 10;

// 올바른 패턴: null/undefined일 때만 기본값 적용
let count = inputCount ?? 10;
```

## Related

- [[_MOC]]
- [[단락-평가]] — Truthy/Falsy를 기반으로 동작하는 단락 평가 패턴

## Sources

- [Notion 원본](https://www.notion.so/fec04108375e411fafea112cf798756c)
