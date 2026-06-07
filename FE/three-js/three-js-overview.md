---
title: Three.js 입문 시리즈 Overview
aliases: [Three.js, 쓰리js, WebGL, 3D 웹, R3F, React Three Fiber]
type: concept
status: budding
created: 2026-05-25
updated: 2026-05-25
tags: [fe/three-js, status/budding]
notion-url: ""
related:
  - "[[_MOC]]"
  - "[[../d3-visualization/force-simulation]]"
source: ["Notion: Computer DB"]
migrated-from: "Notion: Three.js 시리즈 (1강~18강)"
---

# Three.js 입문 시리즈 Overview

> TL;DR: Three.js는 WebGL 추상화 라이브러리. Scene + Camera + Renderer 3요소로 시작해, Geometry → Lighting → Texture → 3D Model → Animation → Physics → React Three Fiber 순으로 확장한다.

---

## What

Three.js는 브라우저에서 WebGL을 직접 다루지 않고 3D 씬을 구성할 수 있도록 추상화한 JavaScript 라이브러리. React와 통합은 **React Three Fiber (R3F)** 를 통해 컴포넌트 방식으로 씬을 구성한다.

---

## 핵심 개념 맵 (18강 구조)

### 기초 — 3D 씬 구성

| 강 | 주제 | 핵심 API |
|----|------|---------|
| 1강 | 소개 + 환경설정 | `npm install three`, Vite 세팅 |
| 2강 | 기본 구성요소 | `Scene`, `Camera`, `WebGLRenderer` |
| 3강 | Geometry | `BoxGeometry`, `SphereGeometry`, `BufferGeometry` |
| 4강 | Lighting & Shadows | `AmbientLight`, `DirectionalLight`, `PointLight`, shadow map |
| 5강 | Camera & OrbitControls | `PerspectiveCamera` vs `OrthographicCamera`, `OrbitControls` |

### 재질 & 자산

| 강 | 주제 | 핵심 API |
|----|------|---------|
| 6강 | Texture | `TextureLoader`, UV mapping, `MeshStandardMaterial` |
| 7강 | 3D 모델 로드 | `GLTFLoader`, `FBXLoader`, `OBJLoader` |
| 8강 | Animation | `AnimationMixer`, `AnimationClip`, `clock.getDelta()` |

### 심화

| 강 | 주제 | 핵심 API |
|----|------|---------|
| 9강 | 물리엔진 | Cannon.js `World`, `Body`, `Shape`, 씬-물리 동기화 |
| 10강 | Particle | `Points`, `PointsMaterial`, `BufferAttribute` |
| 11강 | Vite + React + Three.js | `@react-three/fiber` 설치, `Canvas` 컴포넌트 |
| 12강 | 인터랙티브 웹앱 | Raycaster, mouse events, GSAP 연동 |
| 13강 | 3D 게임 | Cannon.js + R3F `@react-three/cannon` |
| 15강 | 멀티플레이 | Socket.io + Three.js 실시간 상태 동기화 |
| 16강 | 최적화 | LOD (Level of Detail), frustum culling, instancing |
| 17강 | 포트폴리오 웹사이트 | scroll-based animation, 3D 배경 통합 |
| 18강 | 배포 | Vercel/Netlify, 번들 최적화, draco 압축 |

---

## How — 최소 씬 구성

```javascript
import * as THREE from 'three';

// 1. 씬 생성
const scene = new THREE.Scene();

// 2. 카메라 (FOV, 종횡비, near, far)
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

// 3. 렌더러
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// 4. Mesh = Geometry + Material
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x6666ff });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

// 5. 조명
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 5, 5);
scene.add(light);

// 6. 애니메이션 루프
function animate() {
  requestAnimationFrame(animate);
  cube.rotation.y += 0.01;
  renderer.render(scene, camera);
}
animate();
```

### React Three Fiber (R3F) 방식

```jsx
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';

function Box() {
  return (
    <mesh rotation={[0, Math.PI / 4, 0]}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="royalblue" />
    </mesh>
  );
}

export default function App() {
  return (
    <Canvas>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 5, 5]} />
      <Box />
      <OrbitControls />
    </Canvas>
  );
}
```

---

## GLTF 모델 로드

```javascript
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const loader = new GLTFLoader();
loader.load('/models/character.glb', (gltf) => {
  scene.add(gltf.scene);
  
  // 애니메이션 재생
  const mixer = new THREE.AnimationMixer(gltf.scene);
  const action = mixer.clipAction(gltf.animations[0]);
  action.play();
});

// 렌더 루프에서 mixer.update(delta) 호출 필수
```

---

## 성능 최적화 포인트 (16강)

```javascript
// LOD — 거리에 따라 detail 수준 변경
const lod = new THREE.LOD();
lod.addLevel(highDetailMesh, 0);   // 0~50 근접
lod.addLevel(medDetailMesh, 50);   // 50~200
lod.addLevel(lowDetailMesh, 200);  // 200+ 원거리

// Instancing — 같은 오브젝트 수천 개를 하나의 draw call로
const instancedMesh = new THREE.InstancedMesh(geometry, material, 1000);

// Draco 압축 — GLTF 파일 크기 90% 감소
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
const dracoLoader = new DRACOLoader();
gltfLoader.setDRACOLoader(dracoLoader);
```

---

## Pitfalls

- **requestAnimationFrame 누락**: 씬이 한 번만 렌더링되고 멈춤 — 루프 필수
- **카메라 위치 미설정**: 기본 position (0,0,0), 오브젝트와 겹쳐 아무것도 안 보임 → `camera.position.z = 5` 먼저
- **조명 없이 MeshStandardMaterial**: 완전히 검정으로 렌더링 — `AmbientLight` 최소 추가
- **GLB vs GLTF**: `.glb`는 바이너리 단일 파일 (텍스처 포함), 실전엔 GLB 선호
- **애니메이션 루프에서 mixer.update 빠짐**: 3D 모델 애니메이션이 정지 상태
- **R3F와 vanilla Three 혼용**: R3F는 자체 렌더 루프 관리 → `useFrame` 훅 사용, 직접 `renderer.render()` 호출 X

---

## Related

- [[../d3-visualization/force-simulation]] — 2D 그래프 시각화 (D3 force layout)
- [[../../Projects/mindgraph/_INDEX]] — Three.js 실전 적용 프로젝트

## Sources

- [Three.js 공식 문서](https://threejs.org/docs/)
- [React Three Fiber 공식](https://docs.pmnd.rs/react-three-fiber)
- [Drei — R3F 유틸리티](https://github.com/pmndrs/drei)
- Notion 강의 시리즈 (1강~18강)
