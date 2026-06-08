---
name: daily-standup-post
description: Generate the daily standup post for Ilsik. Two-track mental model — Jira TG = auto pipeline (opsx:explore/spec push, opsx:cron pulls and ships), Linear daily-routine-dan = manual hands-on work. Pulls yesterday's shipped work + today's plan from merged PRs (fika-dev/hooksnap), hooksnap release notes, Jira TG state (Rough Ideas → Ready for Automation → In Progress → Deploy Verification → Awaiting Human Ops → Done), Linear, Obsidian daily notes. Writes a curated standup at `fikad-brain/standup-YYYY-MM-DD.md` with two H1 sections (`# 어제 한 일`, `# 오늘 할 일`). 오늘 할 일 splits into `**project-hooksnap (auto)**` (top 3 Jira tickets opsx will ship — user just observes) and `**manual**` (Linear/hands-on: meetings, reviews, decisions, env var ops). `# for you` bottom half adds Jira pipeline snapshot (queue counts, stuck flags, 7d throughput) and steering decisions block (manual promote/demote candidates, env var asks blocking opsx). Use when user asks to draft, prepare, or generate the daily standup, daily scrum post, or DS post for today.
---

# Daily Standup Post

## Purpose

Produce a curated, low-noise standup draft + Jira pipeline control-tower view. The draft lives in its own file (`standup-YYYY-MM-DD.md`) so the existing daily-note workflow (`fikad-brain/YYYY-MM-DD.md` with `### DS` template) stays untouched.

Signal extraction, not dumping. Each Slack-share section answers: *would skipping this be a problem for the team?* If not, cut it. The `# for you` half answers: *what's the state of my auto pipeline, where do I need to intervene?*

## Mental Model — Two Tracks

| Track | Source | Pushed by | Pulled by | User's role |
|-------|--------|-----------|-----------|-------------|
| **Jira TG** (auto) | Jira `project = TG` | opsx:explore (semi-auto), opsx:spec (full auto) | opsx:cron loops (implement, monitor, merge, post-deploy) | **Observe + steer.** Promote rough ideas to Ready for Automation. Resolve env-var blockers (Awaiting Human Ops). Manually demote misfires. |
| **Linear** (manual) | Linear `daily-routine-dan` workspace | User | User | **Execute by hand.** Meetings, code review of opsx PRs, design decisions, content drafts, ops/HR/SNS. |

Standup must show both tracks distinctly:
- **Jira track in `오늘 할 일`** → `**project-hooksnap (auto)**` category. Top 3 tickets opsx will likely ship today. User just reports them in standup; doesn't touch.
- **Linear track in `오늘 할 일`** → `**manual**` category. Top 3 hands-on items. User actually executes.

Jira track in `어제 한 일` = whatever opsx merged + Ilsik-authored PRs. Linear track in `어제 한 일` = whatever user shipped/closed by hand.

## Inputs (Sources)

Query all in parallel when possible. Date math is KST (UTC+9).

### 1. GitHub — fika-dev/hooksnap merged PRs

```bash
gh pr list --repo fika-dev/hooksnap --state merged \
  --search "merged:>=YYYY-MM-DD author:dan-fikad" \
  --json number,title,mergedAt,author,labels,url --limit 50
```

Yesterday window: KST yesterday 00:00 → today 00:00. Mon = previous Fri 00:00 → Mon 00:00 (weekend rule).

### 2. GitHub — hooksnap release notes

- Read `~/fikad/product-iteration/hooksnap/.release-notes/YYYY-MM-DD.md` for yesterday's release.
- `gh release list --repo fika-dev/hooksnap --limit 5` for tag releases.

### 3. Jira TG — pipeline state (6 JQL queries)

The opsx:cron workflow moves tickets through this state machine:

```
Rough Ideas  →  (opsx:explore/spec)  →  Backlog  →  Ready for Automation
       ↓                                                    ↓
  (rough idea backlog)                            (opsx implement loop picks)
                                                            ↓
                                                       In Progress (PR open)
                                                            ↓
                                                  (opsx merge loop)
                                                            ↓
                                                   Deploy Verification
                                                            ↓
                                                  (opsx post-deploy loop)
                                                            ↓
                                          Done  /  Awaiting Human Ops (env vars, etc.)
```

Run all 6 queries to fill `# for you > Jira pipeline snapshot`:

```jql
# Q1 — Top rough ideas (input to opsx:spec next)
project = TG AND status = "Rough Ideas" ORDER BY priority DESC, created ASC

# Q2 — Spec-in-flight (currently being auto-spec'd)
project = TG AND status = "Rough Ideas" AND labels in ("spec-in-progress", "enriched", "spec-ready")

# Q3 — Auto-implement queue (what opsx implement loop will pick)
project = TG AND status = "Ready for Automation" ORDER BY priority DESC, created ASC

# Q4 — In-flight (PR open, may be passing/failing CI)
project = TG AND status = "In Progress" ORDER BY updated DESC

# Q5 — Stuck states (need user intervention)
project = TG AND status in ("Deploy Verification", "Awaiting Human Ops") ORDER BY updated ASC

# Q6 — Throughput (7-day)
project = TG AND status = Done AND resolved >= -7d ORDER BY resolved DESC
```

TG = Ilsik sole owner regardless of assignee (memory `project_tg_sole_owner`).

### 4. Linear — daily-routine-dan workspace (team `c45a1d0c-63ad-4b98-a2e0-66b9a944a38a`)

- Yesterday Done: issues moved to Done in yesterday window.
- Today candidates: In Progress + Todo, ordered by priority and label (HookSnap > Meeting > HR > Ops > SNS > Bug > Improvement > Feature > others).
- Linear holds **manual** work only. Don't conflate with Jira TG.

### 5. Obsidian (`fikad-brain/`)

- `fikad-brain/<yesterday>.md` "오늘 할 일" — cross-check coverage (memory `feedback_daily_note_crosscheck`).
- Today's note if exists — pull category hints.
- `fikad-brain/meeting/` — recent meeting notes (last 2 days).

### 6. Hooksnap repo context (optional)

For Awaiting Human Ops tickets, scan `~/fikad/product-iteration/hooksnap/.claude/opsx-context.md` to recall env-var conventions, Vercel/Render commands.

## Date Rules (KST)

- All "yesterday" windows are KST. Today's date passed in via context (`Today's date is YYYY-MM-DD`).
- **Weekend rule** (memory `feedback_daily_weekend_rule`):
  - Mon → yesterday window covers Fri (last weekday).
  - Sat/Sun → do not pull Fri work again; if user runs skill on weekend, ask whether they want Fri-recap or Mon-prep.
- **Empty-yesterday fallback**: if logical yesterday has zero tasks (no merged PRs, no Done tickets, no daily note "오늘 한 일" entries), search backwards day-by-day for the most recent day with tasks. Use that day's tasks as "어제 한 일" and flag the fallback in `# for you`. **Hard limit: 3 days back from logical yesterday.** If no work found within 3 days, write `휴무` and stop (do not search further). Counting: logical yesterday = day 0; day -1, -2, -3 are checked; day -4 and beyond are out of scope.
- Run `date -u -v+9H +%Y-%m-%d` (macOS) to sanity-check KST if uncertain.

## Output File

Path: `fikad-brain/standup-YYYY-MM-DD.md` (today's date, KST).

Create via direct Write (sibling artifact to daily note, not a daily note replacement).

## Format

File is ONE markdown doc split into two halves by `---` divider:

1. **Top half = Slack-paste copy** (`# 어제 한 일` + `# 오늘 할 일`). User selects and pastes to `#1_daily-scrum`. NO reasoning, NO data dumps.
2. **Bottom half = control-tower view** (`# for you`). Reasoning per item + Jira pipeline snapshot + steering decisions + Reference.

Category labels use **bold emphasis**, not headings, so Slack paste stays clean.

```markdown
# 어제 한 일

**project-hooksnap (auto)**
- {Jira track — opsx-shipped + Ilsik-authored PRs. 1줄 압축. 한국어. 메모리 `feedback_daily_note_korean`. 티켓/PR 번호 금지 메모리 `feedback_daily_note_format`.}
- ...

**manual**
- {Linear track — hands-on work shipped/closed by user yesterday.}
- ...

**meetings**
- ...

# 오늘 할 일

**project-hooksnap (auto)**
- {Top 3 from Jira Ready for Automation + In Progress. User observes — opsx will ship.}
- ...

**manual**
- {Top 3 Linear items user actually executes today.}
- ...

**meetings**
- ...

**personal / etc**
- {비공유. 슬랙 붙여넣기 전 수동 제거.}

---

# for you

**어제 한 일 / project-hooksnap (auto)**
- 왜 이걸 골랐나: ...
- 대안 항목: ...
- 데이터 포인트: ...

**어제 한 일 / manual**
- ...

**오늘 할 일 / project-hooksnap (auto)**
- 왜 이걸 골랐나: ...
- 대안 항목: ...
- 데이터 포인트: ...

**오늘 할 일 / manual**
- ...

**Jira pipeline snapshot**
- Rough Ideas (top 5 by priority): TG-XXXX 제목, TG-YYYY 제목, ...
- Spec-in-flight (spec-in-progress / enriched / spec-ready): N건
- Ready for Automation (auto-implement queue): N건, top = TG-ZZZZ
- In Progress (PR open): N건, oldest age Xh
- Deploy Verification: N건, oldest Xh (>24h이면 🚨 flag)
- Awaiting Human Ops: N건, 필요한 인간 작업 = {env vars / Vercel config / DB migration}
- Throughput last 7d: N merged ({M Feature / X Bug / Y Improvement / Z content})

**steering decisions**
- Promote 후보: TG-AAAA (Rough Ideas, high priority, 설명 충분) → "Ready for Automation"으로 옮기면 오늘 ship 가능.
- Demote 후보: TG-BBBB (Backlog지만 release-blocked 라벨 누락) → 라벨 추가.
- Awaiting Human Ops 처리: TG-CCCC 환경변수 POLAR_KEY 미설정 → Vercel Production에 추가 필요.
- Stale Deploy Verification: TG-DDDD 24h 초과 → 수동 검증 또는 롤백 결정 필요.

### Reference
- (조회한 명령어, JQL, 결과 카운트)
```

### Rules for the format

- Never write `sharing`. Top half IS the sharing copy.
- Only `# 어제 한 일`, `# 오늘 할 일`, `# for you` use H1. No `## H2`. Categories = `**bold**` lines.
- Top half: NO reasoning, NO ticket keys in item body (memory `feedback_daily_note_format`).
- `# for you`: ticket keys ALLOWED in Jira pipeline snapshot, steering decisions, and Reference. These are control-tower data, not Slack copy.
- `personal / etc` lives in `# 오늘 할 일`, above `---`. Not in `# for you`.
- **No empty placeholders.** Don't write `(없음)` or empty bullets. Omit empty category lines. If `# 어제 한 일` has zero items AND fallback exhausted, write single line `휴무` under H1.
- `### Reference` (not `Materials`). Bottom of file.
- `# for you` blocks must always include: per-item reasoning (왜/대안/데이터) + Jira pipeline snapshot + steering decisions.

### Category Labels

Slack-copy categories (omit empty):

- `project-hooksnap (auto)` — Jira TG track. Merged PRs / opsx-shipped (어제) or Ready-for-Automation queue (오늘).
- `manual` — Linear daily-routine-dan track. Hands-on work.
- `meetings` — 미팅 + 미팅 노트 액션 아이템.
- `hr` — 채용/면접/멘토링 (manual sub-track).
- `ops` — 운영 (도구 셋업, 청구, 인프라 — manual sub-track).
- `sns` — 콘텐츠 초안/포스팅 (manual sub-track).
- `project-피카클립` — 피카클립 / gen-shorts.
- `etc` — 나머지.

Note: `hr`, `ops`, `sns` are subset of manual track but break out as separate categories when items are heavy enough to deserve own line. Otherwise fold into `manual`.

`personal / etc` (개인 항목) → `**personal / etc**` bold 라벨, `# 오늘 할 일` 하단(`---` 위)에만, 공유 X.

### 3-Item Cap — How to Cut

When a category has >3 candidates, rank by:

1. **Visibility to team** — others need to know / unblocks them.
2. **Decision needed** — discussion item for standup.
3. **Status change** — shipped / merged / closed (concrete delivery).
4. **Effort signal** — multi-day work hitting milestone.

Demote to `for you > 대안 항목`: routine maintenance, internal-only refactors, ops chores that landed silently, blog translations en masse.

**Auto track special rule**: when opsx ships 10+ PRs in a day (release-note style), group by Epic in the 3 sharing items. Each item = 1 Epic with sub-component list (e.g., "Living Templates 출시 — aesthetic_profile 스키마/aggregator/프롬프트 컴파일러 + Promote CTA").

### Item-line Rules (per memories)

- No ticket numbers, no URLs in Slack-copy body (`feedback_daily_note_format`). Ticket keys live in `# for you` only.
- Korean text (proper nouns/acronyms English OK) — `feedback_daily_note_korean`.
- Each Slack-copy line ≤ ~80 chars, single line, no nested bullets.
- "어제 한 일" = Done only (`feedback_daily_done_only`). Status != Done → skip.
- Sub-detail ≤ 3 lines if expansion needed (`feedback_daily_note_concise`). Prefer 1 line.
- Every "오늘 할 일 / manual" item must have a Linear ticket (`feedback_ensure_linear_tickets`). Auto-track items don't need Linear (they live in Jira).
- Cross-check yesterday's `오늘 할 일` from `fikad-brain/<yesterday>.md` — flag missed items in `for you > 대안 항목` (`feedback_daily_note_crosscheck`).
- Meetings: cancelled = drop; otherwise auto-complete (`feedback_meeting_auto_complete`).

## Workflow

1. **Resolve dates (KST).** Today from context. Compute yesterday window with weekend rule + empty-yesterday fallback (3-day lookback).

2. **Fan out source queries in parallel:**
   - `gh pr list` for hooksnap merged in yesterday window.
   - `gh pr list --state open --author dan-fikad` for open PRs (informs In Progress + Awaiting Review).
   - Read `~/fikad/product-iteration/hooksnap/.release-notes/<yesterday>.md`.
   - Jira MCP × 6 queries (Q1–Q6 above).
   - Linear MCP: Done yesterday + Todo/In Progress today.
   - Read `fikad-brain/<yesterday>.md` "오늘 할 일".
   - `ls fikad-brain/meeting/` for recent meeting notes.

3. **Categorize and split by track.**
   - Jira TG Done + Ilsik-authored merged PRs → `project-hooksnap (auto)` in `어제 한 일`.
   - Linear Done → `manual` (or `meetings`/`hr`/`ops`/`sns`) in `어제 한 일`.
   - Jira Ready-for-Automation + In Progress top 3 → `project-hooksnap (auto)` in `오늘 할 일`.
   - Linear Todo + carryover → `manual` (or `meetings`/`hr`/`ops`/`sns`) in `오늘 할 일`.
   - Dedupe across sources.

4. **Rank within category** using cut rules. Pick top 3. Demote rest to `대안 항목`.

5. **Build Jira pipeline snapshot.** Aggregate Q1–Q6 results:
   - Counts per status.
   - Top 5 Rough Ideas with ticket keys + summaries.
   - Stale flags: Deploy Verification >24h, Awaiting Human Ops with no comment in 24h, In Progress with failing CI.
   - 7-day throughput broken by label (Bug / Feature / Improvement / content).

6. **Derive steering decisions:**
   - High-priority Rough Idea + description ≥50 words → "promote 후보" (opsx:spec will pick next; surface to user for review).
   - Awaiting Human Ops → list required env vars / Vercel commands (read from ticket comments + `.claude/opsx-context.md`).
   - Stale Deploy Verification → flag for manual decision (verify-or-rollback).
   - Misfires (auto-shipped PR that user wants reverted) → none by default; user adds.

7. **Cross-check coverage** against yesterday's `오늘 할 일`. Missed items → `for you > 대안 항목` as "미완료 캐리오버".

8. **Compose** `# 어제 한 일` + `# 오늘 할 일` (Slack copy, no ticket keys in body), then `---`, then `# for you` with per-item reasoning + Jira pipeline snapshot + steering decisions + Reference.

9. **Personal/etc separator.** Move non-shareable items to `**personal / etc**` at bottom of `# 오늘 할 일`.

10. **Write** to `fikad-brain/standup-<today>.md`.

11. **Report** to user: file path + per-category counts + pipeline counts headline (e.g., "Rough Ideas 12 / Ready 3 / In Progress 5 / Stuck 1"). Offer next steps: edit, post to Slack, promote rough ideas, resolve env-var blockers.

## Discussion-Ready Reasoning

The `# for you` half exists because the user discusses the draft before posting. Write 왜/대안/데이터 honestly — borderline picks must be flagged as borderline. Jira pipeline snapshot must include stale-flag warnings, not just raw counts. Steering decisions must name specific tickets, not vague "consider reviewing rough ideas".

## Source MCP / CLI Hints

- GitHub: `gh` CLI authenticated. Prefer `--json`.
- Jira: MCP `mcp__mcp-atlassian__*` (when connected). TG project key. JQL via `jira_search`.
- Linear: MCP `mcp__linear-server__*` (when connected). Team ID `c45a1d0c-63ad-4b98-a2e0-66b9a944a38a`.
- Obsidian: direct file Read of `fikad-brain/<date>.md`.
- PostHog: skip unless user asks for usage-signal picks.
- Hooksnap repo: read `.claude/opsx-context.md` for env-var conventions.

## What This Skill Does NOT Do

- Does not post to Slack (user-triggered separately).
- Does not edit `fikad-brain/<today>.md` daily note.
- Does not promote/demote Jira tickets automatically — surfaces candidates in steering decisions, user decides.
- Does not create Linear tickets automatically — flags missing tickets in `for you` and asks user.
- Does not pull from gen-shorts / other repos — hooksnap scope only.
- Does not run opsx loops or trigger /loop — that's the user's separate workflow.
