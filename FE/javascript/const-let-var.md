---
title: const / let / var — 변수 선언의 차이
aliases: [const, let, var, 변수 선언, 재할당, 참조 불변성]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/javascript, status/budding]
related:
  - "[[_MOC]]"
  - "[[원시타입-객체타입]]"
source: []
migrated-from: ""
---

# const / let / var — 변수 선언의 차이

> TL;DR: `const`는 **재할당 금지**지, 불변(immutable)이 아니다. 객체·배열 내부는 얼마든지 변경 가능. 기본은 `const`, 값 자체가 바뀌어야 할 때만 `let`.

---

## What

| 키워드 | 재할당 | 재선언 | 스코프 | 호이스팅 |
|--------|--------|--------|--------|----------|
| `var` | ✅ | ✅ | 함수 스코프 | 선언만 호이스팅 (`undefined`) |
| `let` | ✅ | ❌ | 블록 스코프 | TDZ (접근 시 ReferenceError) |
| `const` | ❌ | ❌ | 블록 스코프 | TDZ (접근 시 ReferenceError) |

---

## Why it matters

### `const`가 막는 것 — 재할당

"이 변수가 가리키는 **상자 자체**를 다른 상자로 바꾸는 것"을 막는다.

```javascript
const answer = [];
answer = [1, 2, 3]; // ❌ TypeError: Assignment to constant variable
```

### `const`가 막지 않는 것 — 내부 변경

상자의 **내용물**(프로퍼티, 요소)을 바꾸는 건 자유롭다.

```javascript
const answer = [];
answer.push(1);       // ✅ [1]
answer.push(2);       // ✅ [1, 2]

const user = { name: '홍길동' };
user.name = '김철수'; // ✅ { name: '김철수' }
user.age = 30;        // ✅ { name: '김철수', age: 30 }
```

> **원리**: 변수에는 객체/배열의 **참조값(메모리 주소)**이 저장된다. `const`는 그 주소가 바뀌는 것만 막을 뿐, 그 주소가 가리키는 내부 데이터는 건드리지 않는다. → [[원시타입-객체타입]]

---

## How — 선언 선택 기준

```
기본값: const
  │
  └─ 값 자체가 바뀌어야 하는가?
       ├─ Yes → let  (카운터, for 루프 변수, 누적 결과 등)
       └─ No  → const (객체, 배열, 함수, 바뀔 필요 없는 값)
```

**`let`을 써야 하는 전형적인 케이스:**

```javascript
// 1. 반복문 카운터
for (let i = 0; i < 10; i++) { ... }

// 2. 누적 값 (기본형)
let sum = 0;
for (const num of numbers) sum += num;

// 3. 조건에 따라 값이 결정되는 변수
let message;
if (isLoggedIn) {
  message = '환영합니다';
} else {
  message = '로그인이 필요합니다';
}
```

**`const`로 충분한 케이스 (헷갈리는 것):**

```javascript
// 배열에 push/pop 해도 const OK
const stack = [];
stack.push(item);
stack.pop();

// 객체 프로퍼티 수정해도 const OK
const config = { debug: false };
config.debug = true;

// 함수도 const
const greet = (name) => `안녕, ${name}`;
```

---

## Pitfalls

### `var`를 쓰면 안 되는 이유

```javascript
// 함수 스코프 → 블록 밖으로 유출
for (var i = 0; i < 3; i++) {}
console.log(i); // 3 (블록을 벗어나도 살아있음)

// 재선언 허용 → 실수를 잡아주지 않음
var x = 1;
var x = 2; // 에러 없음 — 의도치 않은 덮어쓰기 위험
```

### 완전한 불변이 필요하면 `Object.freeze()`

```javascript
const config = Object.freeze({ apiUrl: 'https://api.example.com' });
config.apiUrl = '다른 URL'; // ❌ 조용히 무시됨 (strict mode에서는 TypeError)
```

> `Object.freeze()`는 얕은 동결(shallow freeze). 중첩 객체까지 완전히 동결하려면 재귀 처리 필요.

### TDZ (Temporal Dead Zone)

```javascript
console.log(a); // ❌ ReferenceError: Cannot access 'a' before initialization
const a = 1;

// var는 호이스팅되어 undefined 출력 (버그 감지 어려움)
console.log(b); // undefined
var b = 1;
```

---

## Related

- [[_MOC]] — JavaScript 전체 지도
- [[원시타입-객체타입]] — 참조값과 값 복사의 원리 (const가 내부를 못 막는 근본 이유)

## Sources

- [MDN — const](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Statements/const)
- [MDN — let](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Statements/let)
