---
title: Rest 매개변수와 Spread 연산자
aliases: [rest parameters, spread syntax, 나머지 매개변수]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/javascript, status/budding]
notion-url: https://www.notion.so/7395e59568c64b8fbeaf05f824ed6296
related:
  - "[[_MOC]]"
  - "[[구조분해할당]]"
source: ["Notion: JavaScript"]
migrated-from: "Notion: Rest 매개변수와 Spread 연산자"
---

# Rest 매개변수와 Spread 연산자

> TL;DR: `...` 문법은 위치에 따라 인수를 배열로 모으는 Rest와 배열/객체를 펼치는 Spread 두 가지로 동작한다.

## What

같은 `...` 기호지만 쓰이는 위치에 따라 역할이 반대다.

- **Rest 매개변수**: 함수 선언부에서 여러 인수를 하나의 배열로 **수집**
- **Spread 연산자**: 배열·객체를 개별 요소로 **펼침**

## Why it matters

가변 인수 함수를 깔끔하게 작성하고, 배열/객체의 불변 복사·결합을 한 줄로 처리할 수 있다.

## How

### Rest 매개변수

```javascript
// 모든 인수를 numbers 배열로 수집
function sum(...numbers) {
    return numbers.reduce((total, num) => total + num, 0);
}
sum(1, 2, 3);       // 6
sum(1, 2, 3, 4, 5); // 15

// 앞 매개변수와 함께 사용 — 나머지만 수집
function printUserInfo(name, age, ...hobbies) {
    console.log(name, age);
    console.log('취미:', hobbies); // 배열
}
printUserInfo('영민', 28, '독서', '코딩', '등산');
```

### Spread — 배열 결합

```javascript
const numbers1 = [1, 2, 3];
const numbers2 = [4, 5, 6];

// 원본 배열을 변경하지 않고 새 배열 생성
const combined = [...numbers1, ...numbers2]; // [1, 2, 3, 4, 5, 6]
```

### Spread — 함수 인수 전달

```javascript
const numbers = [1, 2, 3];
// 배열 요소를 개별 인수로 전달
console.log(Math.max(...numbers)); // 3
sum(...numbers);                   // 6
```

### Spread — 객체 복사 및 확장

```javascript
const user = { name: '영민', age: 28 };

// 불변 업데이트: 원본 유지, 변경된 새 객체 생성
const updatedUser = { ...user, location: 'Seoul', age: 29 };
// { name: '영민', age: 29, location: 'Seoul' }
```

## Pitfalls

- **Rest는 반드시 마지막 매개변수**여야 한다. `function fn(...rest, name)` 은 `SyntaxError`.
- Spread로 객체를 복사하면 **얕은 복사(shallow copy)**만 된다. 중첩 객체는 여전히 같은 참조를 공유한다.

```javascript
const original = { a: 1, nested: { b: 2 } };
const copy = { ...original };

copy.nested.b = 99;
console.log(original.nested.b); // 99 — 중첩 객체는 공유됨!
```

## Related

- [[_MOC]]
- [[구조분해할당]] — 구조분해할당과 함께 쓰이는 경우가 많음

## Sources

- [Notion 원본](https://www.notion.so/7395e59568c64b8fbeaf05f824ed6296)
