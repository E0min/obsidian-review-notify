---
title: Redux Toolkit 심화
aliases: [Redux Toolkit, RTK, createSlice, createAsyncThunk, RTK Query, redux]
type: concept
status: budding
created: 2026-05-25
updated: 2026-05-25
tags: [fe/react, status/budding]
notion-url: ""
related:
  - "[[_MOC]]"
  - "[[상태관리]]"
  - "[[상태-분류]]"
  - "[[zustand-심화]]"
source: []
migrated-from: ""
---

# Redux Toolkit 심화

> TL;DR: RTK는 Redux의 공식 모던 버전 — `createSlice`로 action/reducer를 한 곳에, `createAsyncThunk`로 비동기 처리, `RTK Query`로 서버 상태까지. 보일러플레이트를 80% 줄인다.

---

## What

순수 Redux의 문제점:
- action type 상수, action creator, reducer 3개를 분리해서 작성
- switch문 reducer가 거대해짐
- 비동기 처리에 redux-thunk/saga 추가 세팅 필요
- Immer 없이 불변성 수동 유지

RTK는 이 모든 것을 내장으로 해결.

---

## 기본 구조

### 1. createSlice — Action + Reducer 통합

```typescript
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface CounterState {
  value: number;
  step: number;
}

const counterSlice = createSlice({
  name: 'counter',              // action type prefix: 'counter/increment'
  initialState: { value: 0, step: 1 } as CounterState,
  reducers: {
    increment: (state) => {
      state.value += state.step; // Immer 내장 — 직접 뮤테이션 가능
    },
    decrement: (state) => {
      state.value -= state.step;
    },
    incrementByAmount: (state, action: PayloadAction<number>) => {
      state.value += action.payload;
    },
    setStep: (state, action: PayloadAction<number>) => {
      state.step = action.payload;
    },
    reset: () => ({ value: 0, step: 1 }), // 전체 교체
  },
});

// 자동 생성된 action creator들
export const { increment, decrement, incrementByAmount, setStep, reset } = counterSlice.actions;
export default counterSlice.reducer;
```

### 2. configureStore — Store 설정

```typescript
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from './counter.slice';
import userReducer from './user.slice';

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    user: userReducer,
  },
  // devtools: 자동 활성화 (개발 모드)
  // middleware: 기본으로 thunk 포함
});

// 타입 추출
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### 3. 컴포넌트에서 사용

```typescript
import { useSelector, useDispatch } from 'react-redux';
import { increment, incrementByAmount } from './counter.slice';
import type { RootState, AppDispatch } from './store';

// 타입 안전한 훅 (권장)
export const useAppSelector = useSelector.withTypes<RootState>();
export const useAppDispatch = () => useDispatch<AppDispatch>();

function Counter() {
  const value = useAppSelector((state) => state.counter.value);
  const dispatch = useAppDispatch();

  return (
    <>
      <span>{value}</span>
      <button onClick={() => dispatch(increment())}>+</button>
      <button onClick={() => dispatch(incrementByAmount(5))}>+5</button>
    </>
  );
}
```

---

## createAsyncThunk — 비동기 처리

```typescript
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';

// 비동기 thunk 생성
export const fetchUser = createAsyncThunk(
  'user/fetchById',                           // action type prefix
  async (userId: string, thunkAPI) => {
    try {
      const res = await fetch(`/api/users/${userId}`);
      if (!res.ok) return thunkAPI.rejectWithValue('User not found');
      return await res.json() as User;        // fulfillment payload
    } catch (err) {
      return thunkAPI.rejectWithValue((err as Error).message);
    }
  }
);

interface UserState {
  user: User | null;
  loading: 'idle' | 'pending' | 'succeeded' | 'failed';
  error: string | null;
}

const userSlice = createSlice({
  name: 'user',
  initialState: { user: null, loading: 'idle', error: null } as UserState,
  reducers: {
    clearUser: (state) => { state.user = null; },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUser.pending, (state) => {
        state.loading = 'pending';
        state.error = null;
      })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.loading = 'succeeded';
        state.user = action.payload;
      })
      .addCase(fetchUser.rejected, (state, action) => {
        state.loading = 'failed';
        state.error = action.payload as string;
      });
  },
});
```

```typescript
// 컴포넌트에서
function UserProfile({ userId }: { userId: string }) {
  const dispatch = useAppDispatch();
  const { user, loading, error } = useAppSelector((s) => s.user);

  useEffect(() => {
    dispatch(fetchUser(userId));
  }, [userId, dispatch]);

  if (loading === 'pending') return <Spinner />;
  if (loading === 'failed') return <div>{error}</div>;
  return user ? <div>{user.name}</div> : null;
}
```

---

## RTK Query — 서버 상태 관리

TanStack Query와 같은 역할을 Redux 생태계에서 담당:

```typescript
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const userApi = createApi({
  reducerPath: 'userApi',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  tagTypes: ['User', 'Post'],              // 캐시 무효화 태그
  endpoints: (builder) => ({
    // Query (조회)
    getUser: builder.query<User, string>({
      query: (id) => `/users/${id}`,
      providesTags: (result, err, id) => [{ type: 'User', id }],
    }),
    getUsers: builder.query<User[], void>({
      query: () => '/users',
      providesTags: ['User'],
    }),
    // Mutation (변경)
    updateUser: builder.mutation<User, Partial<User> & { id: string }>({
      query: ({ id, ...body }) => ({
        url: `/users/${id}`,
        method: 'PUT',
        body,
      }),
      invalidatesTags: (result, err, { id }) => [{ type: 'User', id }], // 캐시 무효화
    }),
    deleteUser: builder.mutation<void, string>({
      query: (id) => ({ url: `/users/${id}`, method: 'DELETE' }),
      invalidatesTags: ['User'],
    }),
  }),
});

// 자동 생성된 훅
export const {
  useGetUserQuery,
  useGetUsersQuery,
  useUpdateUserMutation,
  useDeleteUserMutation,
} = userApi;
```

```typescript
// store에 등록
export const store = configureStore({
  reducer: {
    counter: counterReducer,
    [userApi.reducerPath]: userApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(userApi.middleware),
});
```

```typescript
// 컴포넌트에서
function UserList() {
  const { data: users, isLoading, error } = useGetUsersQuery();
  const [updateUser, { isLoading: isUpdating }] = useUpdateUserMutation();

  return (
    <ul>
      {users?.map((user) => (
        <li key={user.id}>
          {user.name}
          <button
            onClick={() => updateUser({ id: user.id, name: 'Updated' })}
            disabled={isUpdating}
          >
            수정
          </button>
        </li>
      ))}
    </ul>
  );
}
```

---

## Normalized State — 정규화된 상태

```typescript
import { createEntityAdapter } from '@reduxjs/toolkit';

const usersAdapter = createEntityAdapter<User>({
  sortComparer: (a, b) => a.name.localeCompare(b.name),
});

const usersSlice = createSlice({
  name: 'users',
  initialState: usersAdapter.getInitialState(),
  reducers: {
    addUser: usersAdapter.addOne,
    addUsers: usersAdapter.addMany,
    updateUser: usersAdapter.updateOne,
    removeUser: usersAdapter.removeOne,
    upsertUser: usersAdapter.upsertOne,  // 있으면 업데이트, 없으면 추가
  },
});

// 자동 생성된 selector
const { selectAll, selectById, selectIds, selectTotal } = usersAdapter.getSelectors(
  (state: RootState) => state.users
);

// 컴포넌트
const allUsers = useAppSelector(selectAll);
const user = useAppSelector((state) => selectById(state, userId));
```

---

## middleware — 커스텀 미들웨어

```typescript
// 로깅 미들웨어
const loggingMiddleware = (store: MiddlewareAPI) => (next: Dispatch) => (action: AnyAction) => {
  console.log('dispatching', action);
  const result = next(action);
  console.log('next state', store.getState());
  return result;
};

export const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(loggingMiddleware),
});
```

---

## RTK 선택 기준

```
RTK를 써야 하는 상황:
  - 대규모 팀 (5명+), 상태 변경 추적·감사 필요
  - DevTools로 타임 트래블 디버깅 필수
  - 이미 Redux 코드베이스가 있어서 마이그레이션
  - 복잡한 정규화된 상태 (중복 없는 entity 관리)

RTK보다 Zustand/Jotai가 나은 상황:
  - 스타트업/1인 개발
  - 빠른 세팅이 필요한 중소규모 앱
  - Provider/action/reducer 개념 학습 부담을 줄이고 싶을 때
```

---

## Pitfalls

- **Provider 빠뜨리기**: `<Provider store={store}>` 없으면 `useSelector` 에러
- **Immer 직접 뮤테이션과 반환 동시**: `state.value = 1; return state;` → Immer 혼란 — 둘 중 하나만
- **RTK Query와 createAsyncThunk 중복**: 같은 엔드포인트에 둘 다 사용 → RTK Query가 있으면 thunk 불필요
- **selector 메모이제이션 누락**: 복잡한 파생 selector에 `createSelector` (reselect) 미사용 → 매 렌더마다 재계산

---

## Related

- [[상태관리]] — 라이브러리 비교 허브
- [[상태-분류]] — RTK를 언제 선택할 것인가
- [[tanstack-query]] — RTK Query 대신 쓸 수 있는 서버 상태 대안

## Sources

- [Redux Toolkit 공식 문서](https://redux-toolkit.js.org/)
- [RTK Query 공식 문서](https://redux-toolkit.js.org/rtk-query/overview)
- [Redux Style Guide](https://redux.js.org/style-guide/)
