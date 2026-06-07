#!/usr/bin/env python3
"""
옵시디언 vault 스캔 → 간격 반복 기반 복습 필요 노트 추출 → Discord webhook 전송.

복습 주기 (confidence 기준):
  1 → 3일,  2 → 7일,  3 → 14일,  4 → 30일,  5 → 60일

환경 변수:
  DISCORD_WEBHOOK_URL : 필수
  VAULT_PATH          : 기본 /Users/leeyoungmin/obsidian/Dev
  CATEGORIES          : 콤마 구분, 기본 "FE,BE,CS,AI-Native,Product,DESIGN,CodingTest"
"""

import json
import os
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

VAULT_PATH = Path(os.environ.get("VAULT_PATH", "/Users/leeyoungmin/obsidian/Dev"))
CATEGORIES = os.environ.get(
    "CATEGORIES", "FE,BE,CS,AI-Native,Product,DESIGN,CodingTest"
).split(",")
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

REVIEW_INTERVAL_DAYS = {1: 3, 2: 7, 3: 14, 4: 30, 5: 60}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict:
    """간이 YAML 프론트매터 파서 (의존성 X). key: value 한 줄짜리만 처리."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fields = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.startswith(" ") or line.startswith("-"):
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if value == "" or value == "[]":
            continue
        fields[key] = value
    return fields


def parse_date(s: str):
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None


def scan_vault():
    today = date.today()
    needs_review = []
    for category in CATEGORIES:
        folder = VAULT_PATH / category
        if not folder.exists():
            continue
        for md in folder.rglob("*.md"):
            if md.name.startswith("_"):
                continue
            try:
                text = md.read_text(encoding="utf-8")
            except Exception:
                continue
            fm = parse_frontmatter(text)
            confidence_raw = fm.get("confidence")
            last_reviewed_raw = fm.get("last-reviewed")
            if not confidence_raw or not last_reviewed_raw:
                continue
            try:
                confidence = int(confidence_raw)
            except ValueError:
                continue
            last_reviewed = parse_date(last_reviewed_raw)
            if not last_reviewed:
                continue
            interval = REVIEW_INTERVAL_DAYS.get(confidence)
            if interval is None:
                continue
            days_elapsed = (today - last_reviewed).days
            if days_elapsed > interval:
                needs_review.append(
                    {
                        "path": md.relative_to(VAULT_PATH).as_posix(),
                        "title": fm.get("title") or md.stem,
                        "confidence": confidence,
                        "last_reviewed": last_reviewed_raw,
                        "days_elapsed": days_elapsed,
                        "interval": interval,
                    }
                )
    needs_review.sort(key=lambda x: (x["confidence"], x["days_elapsed"] * -1))
    return needs_review


def build_message(notes: list) -> dict:
    today_str = date.today().isoformat()
    if not notes:
        return {
            "username": "Obsidian 복습 알림",
            "content": f"**{today_str}** 오늘 복습할 노트 없음. 모두 최신 ✅",
        }

    lines = [f"**{today_str} 복습 필요 ({len(notes)}건)**", ""]
    for n in notes[:20]:
        lines.append(
            f"`c={n['confidence']}` · {n['days_elapsed']}일 경과 "
            f"(주기 {n['interval']}일) — **{n['title']}**\n"
            f"  └ `{n['path']}`"
        )
    if len(notes) > 20:
        lines.append(f"... 외 {len(notes) - 20}건")
    return {
        "username": "Obsidian 복습 알림",
        "content": "\n".join(lines),
    }


def send_discord(payload: dict):
    """macOS 기본 curl 사용 — python.org Python의 인증서 문제 회피."""
    if not WEBHOOK_URL:
        print("ERROR: DISCORD_WEBHOOK_URL 환경변수 미설정", file=sys.stderr)
        sys.exit(1)
    data = json.dumps(payload, ensure_ascii=False)
    result = subprocess.run(
        [
            "/usr/bin/curl",
            "-sS",
            "-X", "POST",
            "-H", "Content-Type: application/json; charset=utf-8",
            "--data-binary", data,
            "--max-time", "15",
            WEBHOOK_URL,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"curl 실패: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"Discord OK (curl exit 0). 응답: {result.stdout[:200] or '(빈 응답 = 204)'}")


def main():
    notes = scan_vault()
    payload = build_message(notes)
    if "--dry-run" in sys.argv:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    send_discord(payload)


if __name__ == "__main__":
    main()
