# Daily Note Source Policy

## GitHub Repositories

Query only these repositories by default when collecting yesterday's merged PRs:

- `fika-dev/hooksnap`

If the user names another repository, include it for that run and record it in Materials.

Only include PRs that are clearly the user's work or HookSnap work. Ignore PRs authored by others unless the user explicitly asks to include team-level work.

## Category Mapping

Use these categories in this order:

1. `hooksnap`
2. `ops`
3. `meeting`
4. `hr`
5. `etc`

Classification rules:

- `hooksnap`: HookSnap product, landing, templates, analytics, thumbnail generation, pricing, auth, SEO tools, conversion, and related TG work.
- `meeting`: calendar events, meeting notes, customer calls, investor/partner meetings, internal alignment, and action items derived from meeting logs.
- `ops`: routine management, workflow automation, Slack/Jira/Linear hygiene, deployment/process cleanup, public API/MCP strategy, and business operations.
- `hr`: recruiting, interviews, candidate follow-up, mentoring tied to hiring, and HR documents.
- `etc`: personal work explicitly present in daily-routine-dan Linear, user-requested GitHub repos, or the prior note carryover.

When an item plausibly fits multiple categories, choose the category that best matches the user's execution context. For example, HookSnap launch operations belong in `hooksnap`; general workflow automation belongs in `ops`.

## Relevance Filter

The daily note is a shareable status note for the user's own work. Include an item only when it is supported by at least one of these default sources:

- Linear workspace `daily-routine-dan`
- Jira project `TG` / HookSnap board
- GitHub repository `fika-dev/hooksnap`
- Previous daily note carryover
- User-provided meeting/context material

Do not include SCRUM, gen-shorts, 피카클립, Notion-derived work, or team PRs from other authors by default. If the user explicitly names one of these sources for the run, include only the requested scope and record it in Materials.

Exclude internal hygiene from `어제 한 일` and `오늘 할 일` task lines, including stale backlog cleanup, duplicate ticket cleanup, status-only ticket grooming, and broad "Linear/Jira 정리" items. If tracking this matters for provenance, mention it briefly in `오늘의 workflow update` instead of DS task lines.

## Staleness Filter

`오늘 할 일` must not blindly include old Todo/backlog items. Check timestamps and current evidence before selecting candidates.

- Completed work is valid when completion/merge happened in yesterday's KST window.
- Linear Todo/In Progress is fresh when created or updated within the last 14 days, carried over from the immediate previous note with matching current context, or linked to a Jira/GitHub item updated within the last 14 days.
- Linear Todo older than 14 days with no recent update or corroborating source is stale. Exclude it from DS task lines; record the exclusion in Materials/workflow update if useful.
- Jira rough ideas/backlog Task candidates are fresh when updated within the last 14 days or directly connected to yesterday's completed work. Avoid stale Epics and stale rough ideas unless the user explicitly names them.
- GitHub open PRs or old branches are fresh only when updated within the last 14 days or tied to current tickets. Merged PRs are used for `어제 한 일` only when merged in yesterday's KST window.
- If all available candidates are stale, write a small `오늘의 workflow update` note about the stale source gap and keep `오늘 할 일` focused on fresh carryover or confirmed Jira candidates.

Task line summaries must use title-style noun phrases, not sentence endings:

- Good: `배포 화면 업데이트`, `템플릿 기반 생성 품질 보강`, `SEO 콘텐츠 파이프라인 개선`
- Avoid: `배포 화면을 다듬었다`, `템플릿 기반 생성 품질을 보강했다`, `항목을 정리했다`

## Source Priority

- `어제 한 일`: Jira Done and Linear Done first, then merged PRs, then completed meetings.
- `오늘 할 일`: Linear In Progress and Todo first, then previous-note carryover, then Jira rough ideas/backlog candidates.
- Notion: query only when the user explicitly asks for Notion or provides a Notion link.
- Slack: use for daily scrum context only when the connector is available and the user request requires it.

Record source gaps in `오늘의 workflow update` or `Skill Update`, for example:

- `Calendar connector가 없어 오늘 예정 미팅은 확인하지 못했다.`
- `GitHub 인증이 없어 merged PR 조회는 건너뛰었다.`
