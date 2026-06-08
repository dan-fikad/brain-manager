# Codex Migration

작성일: 2026-04-27

이 문서는 `brain-manager`를 Claude Code 중심 운영에서 Codex 중심 운영으로 옮기기 위한 현재 상태와 남은 작업을 기록한다.

## 현재 완료된 항목

- Codex CLI 설치 확인: `codex-cli 0.125.0`
- Codex project trust 확인: `/Users/kimilsik/brain-manager`는 `~/.codex/config.toml`에서 trusted project로 등록되어 있음
- repo 운영 지침 추가: `AGENTS.md`
- Jira MCP 확인: `mcp-atlassian` 등록됨
- Linear MCP 추가 및 OAuth 로그인 완료: `linear-server` (`https://mcp.linear.app/mcp`)

## Codex 실행

```bash
codex -C /Users/kimilsik/brain-manager
```

MCP 상태 확인:

```bash
codex mcp list
```

Linear OAuth 재로그인이 필요할 때:

```bash
codex mcp login linear-server
```

## MCP 상태

| 도구 | Codex 상태 | 비고 |
| --- | --- | --- |
| Jira | 등록됨 | `mcp-atlassian`, stdio, `uvx mcp-atlassian` |
| Linear | 등록됨 | `linear-server`, HTTP OAuth 로그인 완료 |
| Notion | 미등록 | repo 운영상 필요. 사용할 MCP 서버 또는 Codex app connector 선택 필요 |
| Slack | 미등록 | repo 운영상 필요. 사용할 MCP 서버 또는 Codex app connector 선택 필요 |
| Obsidian | 미등록 | 현재는 로컬 vault 파일 직접 편집으로 운영 가능 |

## 보안 정리 필요

`~/.codex/config.toml`에 Jira MCP 환경변수가 저장되어 있다. Codex 설정 출력은 값을 마스킹하지만, 파일 자체에는 민감 정보가 남을 수 있다.

권장 작업:

1. Jira API token을 rotate한다.
2. shell profile, password manager, 또는 1Password CLI 등으로 토큰을 외부화한다.
3. `mcp-atlassian` 설정은 가능하면 평문 토큰 대신 실행 환경에서 주입되도록 바꾼다.

이 작업은 토큰 교체와 로그인 영향이 있으므로, 실제 rotate 시점에 별도 작업으로 진행한다.

## Claude Code 레거시

남아 있는 Claude Code 파일:

- `CLAUDE.md`
- `.claude/settings.local.json`

현재는 삭제하지 않는다. Codex 전환이 안정화된 뒤 아래 중 하나를 선택한다.

- `CLAUDE.md`를 보존하되 `AGENTS.md`가 기준임을 명시한다.
- Claude Code를 더 쓰지 않으면 `.claude/`를 삭제한다.
- Claude와 Codex를 병행하면 두 파일의 핵심 운영 규칙을 동기화한다.

## Smoke Test

Codex 새 세션에서 아래를 확인한다.

- `AGENTS.md` 지침을 읽고 한국어로 응답하는지 확인
- `codex mcp list`에서 `mcp-atlassian`, `linear-server`가 보이는지 확인
- Jira TG/SCRUM 검색 가능 여부 확인
- Linear issue 조회 가능 여부 확인
- 오늘 날짜의 데일리 노트(`fikad-brain/YYYY-MM-DD.md`)를 읽고 요약 가능 여부 확인
- Notion/Slack 작업은 아직 미등록 상태임을 보고하고, 사용 가능한 connector가 생기면 연결
