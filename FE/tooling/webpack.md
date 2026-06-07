---
title: Webpack — 번들러 핵심
aliases: [webpack, bundler, 번들러, tree shaking, code splitting, cache busting]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/tooling, status/budding]
notion-url: ""
related:
  - "[[_MOC]]"
  - "[[코드-품질-패키지]]"
  - "[[../performance/_MOC]]"
source: ["Notion: Webpack 강의 시리즈 (1~12강)"]
migrated-from: "Notion: Webpack 강의 시리즈"
---

# Webpack — 번들러 핵심

> TL;DR: Webpack은 JS 모듈 의존성 그래프를 따라 파일들을 하나(또는 여러 청크)로 묶는 번들러. Tree Shaking·Code Splitting·Cache Busting이 프로덕션 최적화의 핵심 세 축이다.

---

## What — 왜 번들러가 필요한가

브라우저는 수백 개의 모듈 파일을 각각 HTTP 요청으로 로드할 수 없다. Webpack은 엔트리 포인트에서 시작해 `import`/`require` 의존성을 따라가며 **의존성 그래프**를 생성하고, 이를 최적화된 번들 파일로 변환한다.

```
src/index.js (entry)
  └── import App.js
        └── import utils.js
        └── import styles.css  ← loader로 처리
  └── import lodash            ← node_modules
        │
        ▼ 번들링
dist/main.[contenthash].js  (하나 또는 여러 청크)
```

### Webpack이 해결하는 문제

| 문제 | Webpack 해결책 |
|------|---------------|
| 수백 개 HTTP 요청 | 파일들을 하나(또는 청크)로 합침 |
| CSS/이미지의 JS 처리 | Loaders (`css-loader`, `file-loader`) |
| 사용 안 하는 코드 포함 | Tree Shaking |
| 초기 로드 용량 | Code Splitting + Lazy Loading |
| 캐시 무효화 어려움 | Content Hash (Cache Busting) |

---

## How

### webpack.config.js 기본 구조

```javascript
// webpack.config.js
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  // 1. Entry — 의존성 그래프 시작점
  entry: './src/index.js',

  // 2. Output — 번들 파일 저장 위치
  output: {
    filename: '[name].[contenthash].js', // contenthash로 캐시 버스팅
    path: path.resolve(__dirname, 'dist'),
    clean: true, // 매 빌드마다 dist 정리
  },

  // 3. Mode — 'development' | 'production' | 'none'
  mode: 'development',

  // 4. DevServer
  devServer: {
    port: 3000,
    hot: true,           // HMR (Hot Module Replacement)
    open: true,
    historyApiFallback: true, // SPA에서 새로고침 404 방지
  },

  // 5. Module/Rules — Loaders (변환기)
  module: {
    rules: [
      {
        test: /\.jsx?$/,                  // .js, .jsx 파일
        use: 'babel-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'], // 오른쪽 → 왼쪽 순서 실행
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        type: 'asset/resource',            // Webpack 5 내장 (file-loader 대체)
      },
    ],
  },

  // 6. Plugins — 번들 단위 처리
  plugins: [
    new HtmlWebpackPlugin({ template: './src/index.html' }),
  ],

  // 7. Resolve — import 확장자 생략
  resolve: {
    extensions: ['.js', '.jsx', '.ts', '.tsx'],
  },
};
```

---

### 개발/프로덕션 환경 분리 (`webpack-merge`)

```bash
npm install -D webpack-merge
```

```javascript
// webpack.common.js — 공통 설정
module.exports = {
  entry: './src/index.js',
  resolve: { extensions: ['.js', '.jsx'] },
  module: {
    rules: [{ test: /\.jsx?$/, use: 'babel-loader', exclude: /node_modules/ }],
  },
  plugins: [new HtmlWebpackPlugin({ template: './src/index.html' })],
};
```

```javascript
// webpack.dev.js
const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');

module.exports = merge(common, {
  mode: 'development',
  devtool: 'inline-source-map',  // 소스맵 (빠른 빌드, 큰 파일)
  devServer: { port: 3000, hot: true },
  output: {
    filename: '[name].js',         // 개발 환경: contenthash 불필요
  },
});
```

```javascript
// webpack.prod.js
const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = merge(common, {
  mode: 'production',
  devtool: 'source-map',           // 소스맵 (느리지만 작음)
  output: {
    filename: '[name].[contenthash].js', // 캐시 버스팅
    path: path.resolve(__dirname, 'dist'),
    clean: true,
  },
  plugins: [
    new MiniCssExtractPlugin({ filename: '[name].[contenthash].css' }),
  ],
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [MiniCssExtractPlugin.loader, 'css-loader'], // style-loader 대신 파일로 추출
      },
    ],
  },
});
```

```json
// package.json
{
  "scripts": {
    "dev": "webpack serve --config webpack.dev.js",
    "build": "webpack --config webpack.prod.js"
  }
}
```

---

### Tree Shaking — 사용 안 하는 코드 제거

```javascript
// utils.js — ES 모듈 필수 (CommonJS require는 Tree Shaking 불가)
export function add(a, b) { return a + b; }
export function unused() { return 'never used'; } // ← 번들에서 제거됨

// index.js
import { add } from './utils'; // add만 사용 → unused는 번들에서 제거
```

**Tree Shaking 동작 조건**:
1. `mode: 'production'` (Webpack이 자동으로 Terser minifier 적용)
2. **ES 모듈** (`import`/`export`) — CommonJS(`require`)는 Tree Shaking 불가
3. `package.json`에 `"sideEffects": false` 명시 (순수 모듈임을 선언)

```json
// 라이브러리 package.json
{
  "sideEffects": false          // 모든 파일 Tree Shaking 허용
  // 또는
  "sideEffects": ["*.css"]      // CSS 파일은 side effect 있음 (제외하지 말 것)
}
```

---

### Code Splitting — 청크 분리

#### 1. Entry Points (정적 분리)

```javascript
entry: {
  app: './src/index.js',
  admin: './src/admin.js',  // 어드민 페이지만 별도 번들
},
```

#### 2. Dynamic Import (동적 분리 + Lazy Loading)

```javascript
// 클릭 시 모달 컴포넌트를 그때 로드
button.addEventListener('click', async () => {
  const { default: Modal } = await import('./Modal.js');
  new Modal().open();
});

// React에서
const LazyPage = React.lazy(() => import('./pages/Dashboard'));
```

#### 3. SplitChunks — 벤더 코드 분리

```javascript
// webpack.prod.js
optimization: {
  splitChunks: {
    chunks: 'all',  // async + initial 청크 모두 분리
    // → node_modules는 vendors 청크로 자동 분리
    // react, lodash 등 자주 바뀌지 않는 코드 → 캐시 유지
  },
},
```

```
dist/
├── main.[hash].js           ← 앱 코드 (자주 바뀜)
├── vendors.[hash].js        ← node_modules (잘 안 바뀜 → 캐시 유지)
└── index.html
```

---

### Cache Busting — `contenthash`

```javascript
output: {
  filename: '[name].[contenthash].js',
  // contenthash: 파일 내용이 바뀔 때만 해시가 바뀜
  // → 내용이 같으면 브라우저가 캐시된 파일을 계속 사용
}
```

| 해시 유형 | 변경 시점 | 용도 |
|---------|---------|------|
| `[hash]` | 빌드마다 항상 | (사용 비권장) |
| `[chunkhash]` | 해당 청크 내용 변경 시 | 청크별 캐싱 |
| `[contenthash]` | 파일 내용 변경 시 | CSS·JS 모두 적합 (권장) |

---

## Pitfalls

- **Tree Shaking은 `mode: 'production'`에서만** 자동 적용. 개발 환경에서는 확인 불가.
- **CommonJS(`require`)는 Tree Shaking 안 됨** — lodash는 `import { get } from 'lodash-es'`(ES 버전)로 import해야 효과.
- **Loader 순서**: `use` 배열은 **오른쪽 → 왼쪽** 실행. `['style-loader', 'css-loader']`는 css-loader가 먼저, style-loader가 나중.
- **`clean: true`**: Webpack 5부터 내장. `CleanWebpackPlugin` 별도 설치 불필요.
- **Dynamic import와 Suspense**: React에서 `lazy()`는 반드시 `<Suspense fallback>` 래핑 필요.

---

## Related

- [[_MOC]] — FE 전체 지도
- [[코드-품질-패키지]] — Webpack이 포함된 빌드·품질 도구 전체 맥락
- [[../performance/_MOC]] — Core Web Vitals, 번들 최적화 전략

## Sources

- [Webpack 공식 문서](https://webpack.js.org/concepts/)
- [Webpack — Tree Shaking](https://webpack.js.org/guides/tree-shaking/)
- [Webpack — Code Splitting](https://webpack.js.org/guides/code-splitting/)
- [Webpack — Caching](https://webpack.js.org/guides/caching/)
