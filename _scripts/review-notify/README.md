# Obsidian 복습 알림 → Discord

매일 아침 9시, vault의 `confidence` + `last-reviewed` 필드를 스캔해 복습 주기가 지난 노트를 Discord 채널로 푸시합니다.

## 복습 주기 (간격 반복)

| confidence | 주기 |
|---|---|
| 1 | 3일 |
| 2 | 7일 |
| 3 | 14일 |
| 4 | 30일 |
| 5 | 60일 |

## 설치

```bash
# 1. webhook URL을 .env에 저장 (.env.sample 참고)
cp .env.sample .env
echo 'DISCORD_WEBHOOK_URL=<여기에 URL 붙여넣기>' > .env
chmod 600 .env

# 2. dry-run으로 메시지 확인 (Discord 전송 X)
source .env && python3 notify.py --dry-run

# 3. 실제로 한 번 전송
source .env && python3 notify.py

# 4. launchd에 등록 (매일 9시 자동 실행)
cp com.user.obsidian-review-notify.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.user.obsidian-review-notify.plist

# 동작 확인 (즉시 실행)
launchctl start com.user.obsidian-review-notify
tail notify.log notify.err.log

# 중지하려면
launchctl unload ~/Library/LaunchAgents/com.user.obsidian-review-notify.plist
```

## 로그

- `notify.log` — 정상 출력
- `notify.err.log` — 에러

## 환경변수

| 변수 | 기본값 |
|---|---|
| `DISCORD_WEBHOOK_URL` | (필수) |
| `VAULT_PATH` | `/Users/leeyoungmin/obsidian/Dev` |
| `CATEGORIES` | `FE,BE,CS,AI-Native,Product,DESIGN,CodingTest` |

## 변경

- 스캔 카테고리·복습 주기는 `notify.py` 상단 상수에서 조정
