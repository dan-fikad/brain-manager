---
name: daily-note
description: Create or update the user's Korean Obsidian daily note in `fikad-brain/YYYY-MM-DD.md` from Linear, Jira, GitHub PR, calendar, and prior-note context. Use when the user asks for a daily note, DS note, morning routine note, daily scrum draft, "오늘 데일리", "데일리 노트", or to collect yesterday's work and today's tasks.
---

# Daily Note

## Overview

Create a concise Korean daily note with `fikad-brain/` as the source of truth. Calculate the target date in KST, collect work context, write through `obsidian-cli`, and preserve personal sections already present in the note.

## Workflow

1. Calculate today and yesterday in `Asia/Seoul`.
   - Prefer `python3 .agents/skills/daily-note/scripts/merge_daily_note.py --print-kst-dates`.
   - Target note: `fikad-brain/YYYY-MM-DD.md`.
   - Obsidian path: `YYYY-MM-DD.md` in vault `fikad-brain`.
2. Read the previous daily note and extract `##### 오늘 할 일` for carryover.
3. Collect completed work for yesterday:
   - Linear workspace `daily-routine-dan`: Done issues completed in yesterday's KST window.
   - Jira project `TG` only: Done issues in yesterday's KST window.
   - GitHub merged PRs from the default repo list in `references/source-policy.md`.
   - Completed meetings from calendar only when a calendar connector or CLI is available.
4. Collect today's plan:
   - Linear Todo and In Progress first.
   - Before adding Linear/Jira/GitHub candidates, run a stale check using created/updated/completed/merged timestamps.
   - Add carryover from the previous note when no completed evidence exists.
   - Add at most three Jira candidate tasks from rough ideas/backlog.
   - Add today's meetings from calendar only when available.
5. Do not query Notion unless the user explicitly requested Notion or provided a Notion link.
6. Draft Korean sections:
   - `어제 한 일`: use merged PRs, Jira Done, Linear Done, and completed meetings.
   - `오늘 할 일`: prioritize Linear Todo/In Progress, then carryover and Jira candidates.
   - Exclude stale Todo/backlog candidates from `오늘 할 일` unless there is fresh evidence that the user is actively reviving them today.
   - Keep task lines as `- {주제} - {성과 요약}`.
   - Write task line summaries in title style, not full sentence style. Prefer noun endings such as `업데이트`, `개선`, `보강`, `정리`, `검증`, `확정`, `구현`, `연결`.
   - Do not end task lines with report-like verbs such as `했다`, `다듬었다`, `보강했다`, `확인했다`, `정리했다`.
   - Exclude internal hygiene items such as old backlog cleanup, ticket deduplication, stale QA cleanup, and "Linear/Jira 정리" from shared `어제 한 일` and `오늘 할 일` task lines.
   - Do not put ticket numbers or URLs in task lines.
7. Merge the note with `scripts/merge_daily_note.py`.
   - Existing notes: replace only `어제 한 일` and `오늘 할 일`; preserve Materials and personal sections, appending new Materials/updates only when provided.
   - Missing notes: create the AGENTS.md template with the generated sections.
8. Write the result with `obsidian-cli create ... overwrite`.

If any source fails, continue with available data. Record the missing source in `오늘의 workflow update` or `Skill Update` instead of blocking note creation.

## Stale Candidate Check

Use this check before adding any item to `오늘 할 일`.

- Completed evidence is not stale when it happened in yesterday's KST window: Jira/Linear Done, GitHub PRs merged yesterday, or completed meetings.
- Linear Todo/In Progress:
  - Include when it was created or updated in the last 14 days, appears in yesterday's carryover, or has a related Jira/GitHub/source item updated in the last 14 days.
  - Treat as stale when it is older than 14 days and has no recent update, no repeated carryover, and no current linked evidence. Do not include it just because it is still Todo.
  - If a stale item looks important, mention it in `오늘의 workflow update` or Materials as a review candidate instead of a DS task line.
- Jira rough ideas/backlog candidates:
  - Include only Task issues, not Epics, unless the epic is the user's explicit focus.
  - Prefer issues updated in the last 14 days, newly created planning candidates, or issues directly linked to yesterday's completed work.
  - Treat older rough ideas/backlog items as stale unless the prior note or a fresh PR/ticket update points to them.
- GitHub:
  - For `어제 한 일`, use PRs merged in yesterday's KST window.
  - For `오늘 할 일`, do not infer work from old open PRs unless they were updated in the last 14 days or explicitly appear in carryover/current tickets.
- Previous-note carryover:
  - Include carryover when it is from the immediately previous note and still matches fresh ticket/PR context.
  - If the same vague carryover repeats without evidence, move it to workflow review instead of keeping it in DS.

Record stale exclusions briefly in `오늘의 workflow update` or Materials, for example:

- `Linear Todo 1건은 생성/업데이트가 오래되어 오늘 할 일 후보에서 제외했다.`
- `Jira backlog 후보 중 오래된 Epic은 DS가 아니라 Materials에만 남겼다.`

## Source Policy

Read `references/source-policy.md` before classifying collected items or querying GitHub. It contains the default GitHub repos and category rules.

## Obsidian Commands

Use the installed Obsidian CLI, falling back to the macOS app binary when needed:

```bash
OBSIDIAN_CLI="$(command -v obsidian-cli || true)"
if [ -z "$OBSIDIAN_CLI" ]; then
  OBSIDIAN_CLI="/Applications/Obsidian.app/Contents/MacOS/obsidian-cli"
fi
```

Read the note if it exists:

```bash
"$OBSIDIAN_CLI" read vault=fikad-brain path="$TODAY.md"
```

Write the merged result:

```bash
"$OBSIDIAN_CLI" create vault=fikad-brain path="$TODAY.md" content="$(cat /tmp/daily-note.md)" overwrite
```

## Merge Script

Use `scripts/merge_daily_note.py` for deterministic Markdown merging:

```bash
python3 .agents/skills/daily-note/scripts/merge_daily_note.py \
  --existing-file /tmp/current-note.md \
  --yesterday-json /tmp/yesterday.json \
  --today-json /tmp/today.json \
  --materials-file /tmp/materials.md \
  --workflow-update-file /tmp/workflow.md \
  --skill-update-file /tmp/skill-update.md \
  --output /tmp/daily-note.md
```

The JSON inputs are category maps:

```json
{
  "hooksnap": [
    {"topic": "랜딩 v2 검증", "summary": "공개 홈과 인증 흐름 검증"}
  ],
  "ops": ["routine 전환 - 첫 자동화 단위 선정"]
}
```

Prefer JSON when possible so the script can enforce category order and remove ticket numbers/URLs from task lines. Use Markdown input files only for already-reviewed prose.

## Note Rules

- Write all note content in Korean.
- Use category titles exactly as bold Markdown: `**hooksnap**`, `**ops**`, `**meeting**`, `**hr**`, `**etc**`.
- Keep `어제 한 일` and `오늘 할 일` concise; group many tickets by product or operational theme.
- Treat the daily note as a shareable status note. Prefer externally meaningful product outcomes over implementation bookkeeping.
- Use concise title-style phrasing in task lines: `배포 화면 업데이트`, `템플릿 기반 생성 품질 보강`, `SEO 콘텐츠 파이프라인 개선`.
- Do not include private/internal maintenance as task lines, for example `오래된 QA/SEO 항목 정리`, `중복 티켓 완료 처리`, or `백로그 정리`.
- Do not infer the `김아영` section. Preserve existing text; leave unknown fields blank in new notes.
- Put ticket references, source names, and lookup failures in Materials, workflow update, or Skill Update, not in task lines.
