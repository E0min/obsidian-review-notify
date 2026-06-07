---
title: State로 사용자 입력 관리하기
aliases: [controlled component, onChange, form state, 폼 상태 관리]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/react, status/budding]
notion-url: https://www.notion.so/8d2c7ccfec7845b99b930cac0dcb1fe4
related:
  - "[[_MOC]]"
  - "[[state]]"
  - "[[이벤트-처리]]"
source: ["Notion: React"]
migrated-from: "Notion: State로 사용자 입력 관리하기"
---

# State로 사용자 입력 관리하기

> TL;DR: input에 `value={state}` + `onChange={handler}`를 설정하는 controlled component 패턴. 여러 입력은 객체 state + `e.target.name`으로 하나의 핸들러로 통합 처리.

## What

input/select/textarea의 값을 state로 관리하는 controlled component 패턴.

## Why it matters

`value` 없는 uncontrolled component는 state와 UI가 불일치할 수 있다. controlled 패턴으로 단일 진실 공급원을 유지해야 폼 유효성 검사, 초기화, 제출 처리가 안정적으로 동작한다.

## How

**단일 입력**:
```javascript
const [name, setName] = useState("이름");
<input value={name} onChange={(e) => setName(e.target.value)} />
```

**여러 입력 최적화** — 객체 state + name 속성 활용:
```javascript
const [form, setForm] = useState({
    name: "", birth: "", country: "", introduce: ""
});

const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
};

<input name="name" value={form.name} onChange={handleChange} />
<input name="birth" value={form.birth} onChange={handleChange} />
<select name="country" value={form.country} onChange={handleChange}>
    <option value="한국">한국</option>
</select>
```

`e.target.name`으로 어떤 입력인지 구분, 스프레드로 나머지 유지.

## Pitfalls

- `value` 속성 없으면 uncontrolled component → state와 UI 불일치 가능
- `onChange` 누락 시 읽기 전용 필드가 됨

## Related

- [[_MOC]]
- [[state]]
- [[이벤트-처리]]

## Sources

- Notion: State로 사용자 입력 관리하기
