---
title: HTML/CSS 기초 (박스 모델·트랜지션·시맨틱·접근성)
aliases: [HTML/CSS, html css 기초, css 박스 모델, 웹 접근성, 시맨틱 태그, accessibility]
type: concept
status: budding
created: 2024-08-26
updated: 2026-05-25
tags: [fe/css-styling, fe/html, status/budding, a11y]
notion-url: https://www.notion.so/7d52ff1e83874cd6a265fec57b493bab
related:
  - "[[_MOC]]"
  - "[[../browser/passive-event-listener]]"
  - "[[../../CS/network/웹서비스-운영-과정]]"
source: ["Notion: HTML/CSS (구름 EXP 미션)"]
migrated-from: "Notion: HTML/CSS"
---

# HTML/CSS 기초 — 박스 모델·트랜지션·시맨틱·접근성

> TL;DR: HTML/CSS의 4가지 핵심: ①CSS 박스 모델, ②전환·호버 효과, ③시맨틱 태그, ④접근성 속성(WCAG). 시맨틱 + ARIA + 충분한 명도 대비가 모든 사용자가 쓸 수 있는 웹의 기본.

---

## 1. CSS 박스 모델

모든 요소는 4개 영역의 박스: **content → padding → border → margin**.

```css
.container {
    display: flex;
    background-color: rgb(31, 185, 75);
    margin: 20px;            /* 바깥 여백 */
    padding: 100px;          /* 안쪽 여백 */
}

.box {
    width: 100px;
    height: 100px;
    box-sizing: border-box;  /* width에 padding+border 포함 */
    border: 20px solid black;
    margin: auto;            /* 좌우 자동 가운데 정렬 */
}
```

핵심 포인트:
- `box-sizing: border-box` — width에 border/padding 포함, 직관적 계산
- `margin: auto` — flex/block 컨텍스트에서 가운데 정렬 도구
- `margin` 상쇄(collapse): 인접한 두 block 요소의 vertical margin은 더 큰 값 하나로 합쳐짐

---

## 2. 트랜지션과 호버 효과

```css
button {
    background-color: #3498db;
    transition: background-color 0.3s ease;  /* 변화 부드럽게 */
}

button:hover {
    animation: rainbow 2s infinite;
}

@keyframes rainbow {
    0%   { background-color: red; }
    16%  { background-color: orange; }
    32%  { background-color: yellow; }
    48%  { background-color: green; }
    64%  { background-color: blue; }
    80%  { background-color: indigo; }
    100% { background-color: violet; }
}
```

- `transition: <property> <duration> <timing-function>` — 단순 보간
- `@keyframes` + `animation` — 다단계 / 무한 반복
- 호버 인터랙션은 `:focus`에도 동일 스타일 적용해 키보드 사용자 배려

---

## 3. 시맨틱 태그 — 의미 있는 HTML

`div`/`span` 대신 의미가 담긴 태그를 쓰면 브라우저·스크린 리더·검색 엔진이 페이지 구조를 더 잘 이해한다.

```html
<header>
    <nav aria-label="Main Navigation">
        <ul>
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
        </ul>
    </nav>
</header>

<main>
    <section id="home">
        <h1>Welcome</h1>
        <p>Intro</p>
    </section>

    <section id="blog" aria-labelledby="blog-title">
        <h2 id="blog-title">Latest Posts</h2>
        <article>
            <h3>Article Title</h3>
            <p>...</p>
            <button aria-label="Read more about accessible web">Read More</button>
        </article>
    </section>
</main>

<footer>copyright</footer>
```

주요 시맨틱 태그: `header`, `nav`, `main`, `section`, `article`, `aside`, `footer`, `figure`, `time`.

---

## 4. 접근성 (Accessibility, a11y)

장애를 가진 사용자도 쉽게 이용할 수 있도록 콘텐츠를 설계하는 방식. WCAG 가이드라인 준수.

### HTML 접근성 속성

#### `alt` — 이미지 대체 텍스트
```html
<img src="logo.png" alt="회사 로고">
```
- 이미지 로딩 실패·시각장애 사용자 스크린 리더를 위한 텍스트

#### `aria-*` — 동적 콘텐츠 보조 정보
```html
<button aria-label="메뉴 열기">☰</button>
<section aria-labelledby="blog-title">...</section>
```
- `aria-label`, `aria-labelledby`, `aria-hidden`, `aria-expanded` 등

#### `role` — 요소의 역할 명시
```html
<div role="button" tabindex="0">Click me</div>
```
- 가능하면 시맨틱 태그(`<button>`) 사용, role은 보완

#### `tabindex` — 키보드 탭 순서
```html
<a href="#" tabindex="0">자연스러운 순서</a>
<div tabindex="-1">포커스 가능하지만 탭으로 도달 안 됨</div>
```
- 양수 값 (`tabindex="1"` 등)은 권장하지 않음 — 자연 순서 깨짐

#### `label` + `for` — 양식 레이블 연결
```html
<label for="name">이름:</label>
<input type="text" id="name" name="name">
```

### CSS 접근성

#### 명도 대비 (WCAG)
- 본문 텍스트: 배경과 **4.5:1** 이상
- 대형 텍스트(18pt 이상): **3:1** 이상

```css
body {
    color: #000;
    background-color: #fff;  /* 21:1 — 완벽 */
}
```

#### 포커스 스타일 (절대 제거 금지)
```css
button:focus {
    outline: 3px solid #005fcc;
    outline-offset: 2px;
}

/* ❌ 절대 안 됨 */
*:focus { outline: none; }
```

#### 미디어 쿼리 — 반응형
```css
@media (min-width: 600px) {
    body { font-size: 18px; }
}

@media (prefers-reduced-motion: reduce) {
    * { animation: none !important; }  /* 모션 줄이기 옵션 사용자 */
}
```

---

## Pitfalls

- `div`/`span` 남용 → 스크린 리더가 페이지 구조 파악 불가. 시맨틱 우선.
- `outline: none`으로 포커스 스타일 제거 → 키보드 사용자 길 잃음.
- 명도 대비 검사 안 함 → 색약·약시 사용자 가독성 ↓. Chrome DevTools `Lighthouse` 또는 `axe`로 점검.
- `alt=""` 빈 문자열은 "장식 이미지"라는 의미. 의미 있는 이미지에 alt 빠뜨리면 잘못된 신호.
- `aria-*`를 시맨틱 대체로 쓰는 것 — `<button>` 대신 `<div role="button">`은 키보드 동작도 직접 구현해야 함.

---

## Related

- [[_MOC]]
- [[../browser/passive-event-listener]] — 스크롤 성능 + 이벤트 접근성
- [[../../CS/network/웹서비스-운영-과정]] — HTML/CSS가 어디서 그려지는지 큰 그림

## Sources

- [Notion 원본 — HTML/CSS (구름 EXP 미션)](https://www.notion.so/7d52ff1e83874cd6a265fec57b493bab)
- [MDN — How the Web works](https://developer.mozilla.org/ko/docs/Learn/Getting_started_with_the_web/How_the_Web_works)
- [WCAG 2.1 — W3C](https://www.w3.org/WAI/standards-guidelines/wcag/)
