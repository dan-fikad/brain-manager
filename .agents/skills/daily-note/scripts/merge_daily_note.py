#!/usr/bin/env python3
"""Merge generated daily-note sections into an Obsidian Markdown note."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


CATEGORIES = ("hooksnap", "ops", "meeting", "hr", "etc")
TICKET_RE = re.compile(r"\b(?:TG|SCRUM|DAI|HOOK|HS|FIKA)-\d+\b", re.IGNORECASE)
URL_RE = re.compile(r"https?://\S+")
HEADING_RE = re.compile(r"(?m)^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
TITLE_STYLE_SUFFIXES = (
    ("다듬었다", "개선"),
    ("다듬는다", "개선"),
    ("보강했다", "보강"),
    ("보강한다", "보강"),
    ("개선했다", "개선"),
    ("개선한다", "개선"),
    ("업데이트했다", "업데이트"),
    ("업데이트한다", "업데이트"),
    ("확인했다", "확인"),
    ("확인한다", "확인"),
    ("검증했다", "검증"),
    ("검증한다", "검증"),
    ("정리했다", "정리"),
    ("정리한다", "정리"),
    ("정했다", "선정"),
    ("정한다", "선정"),
    ("선정했다", "선정"),
    ("선정한다", "선정"),
    ("확정했다", "확정"),
    ("확정한다", "확정"),
    ("구현했다", "구현"),
    ("구현한다", "구현"),
    ("연결했다", "연결"),
    ("연결한다", "연결"),
    ("반영했다", "반영"),
    ("반영한다", "반영"),
    ("진행했다", "진행"),
    ("진행한다", "진행"),
)


@dataclass(frozen=True)
class Heading:
    level: int
    title: str
    start: int
    line_end: int


@dataclass(frozen=True)
class Section:
    heading: Heading
    content_start: int
    content_end: int


def kst_dates(now_utc: datetime | None = None) -> dict[str, str]:
    """Return today/yesterday and vault-relative note paths in KST."""
    if now_utc is None:
        now_utc = datetime.now(timezone.utc)
    elif now_utc.tzinfo is None:
        now_utc = now_utc.replace(tzinfo=timezone.utc)

    today = now_utc.astimezone(ZoneInfo("Asia/Seoul")).date()
    yesterday = today.fromordinal(today.toordinal() - 1)
    return {
        "today": today.isoformat(),
        "yesterday": yesterday.isoformat(),
        "today_path": f"fikad-brain/{today.isoformat()}.md",
        "yesterday_path": f"fikad-brain/{yesterday.isoformat()}.md",
        "obsidian_today_path": f"{today.isoformat()}.md",
        "obsidian_yesterday_path": f"{yesterday.isoformat()}.md",
    }


def normalize_title(title: str) -> str:
    return re.sub(r"\s+", " ", title.strip())


def iter_headings(markdown: str) -> list[Heading]:
    headings: list[Heading] = []
    for match in HEADING_RE.finditer(markdown):
        line_end = markdown.find("\n", match.start())
        if line_end == -1:
            line_end = len(markdown)
        headings.append(
            Heading(
                level=len(match.group(1)),
                title=normalize_title(match.group(2)),
                start=match.start(),
                line_end=line_end,
            )
        )
    return headings


def find_section(markdown: str, title: str, level: int | None = None) -> Section | None:
    title = normalize_title(title)
    headings = iter_headings(markdown)
    for index, heading in enumerate(headings):
        if heading.title != title:
            continue
        if level is not None and heading.level != level:
            continue

        content_start = heading.line_end + 1 if heading.line_end < len(markdown) else len(markdown)
        content_end = len(markdown)
        for next_heading in headings[index + 1 :]:
            if next_heading.level <= heading.level:
                content_end = next_heading.start
                break
        return Section(heading=heading, content_start=content_start, content_end=content_end)
    return None


def replace_section_content(markdown: str, title: str, new_content: str, level: int | None = None) -> str:
    section = find_section(markdown, title, level)
    if section is None:
        raise ValueError(f"section not found: {title}")
    content = normalize_block(new_content)
    return markdown[: section.content_start] + content + "\n\n" + markdown[section.content_end:].lstrip("\n")


def insert_after_section(markdown: str, after_title: str, heading: str, level: int = 5) -> str:
    section = find_section(markdown, after_title)
    if section is None:
        raise ValueError(f"section not found: {after_title}")
    prefix = markdown[: section.content_end].rstrip()
    suffix = markdown[section.content_end:].lstrip("\n")
    inserted = f"\n\n{'#' * level} {heading}\n\n"
    return prefix + inserted + suffix


def insert_at_section_start(markdown: str, parent_title: str, heading: str, level: int = 5) -> str:
    section = find_section(markdown, parent_title)
    if section is None:
        raise ValueError(f"parent section not found: {parent_title}")
    inserted = f"{'#' * level} {heading}\n\n"
    return markdown[: section.content_start] + inserted + markdown[section.content_start:]


def ensure_daily_sections(markdown: str) -> str:
    if find_section(markdown, "DS", 3) is None:
        markdown = "### DS\n\n---\n\n" + markdown.lstrip()
    if find_section(markdown, "어제 한 일", 5) is None:
        markdown = insert_at_section_start(markdown, "DS", "어제 한 일", 5)
    if find_section(markdown, "오늘 할 일", 5) is None:
        markdown = insert_after_section(markdown, "어제 한 일", "오늘 할 일", 5)
    if find_section(markdown, "오늘의 workflow update", 5) is None:
        markdown = insert_after_section(markdown, "오늘 할 일", "오늘의 workflow update", 5)
    return markdown


def normalize_block(text: str) -> str:
    lines = [line.rstrip() for line in text.strip().splitlines()]
    return "\n".join(lines).strip()


def sanitize_inline(text: str) -> str:
    text = URL_RE.sub("", text)
    text = TICKET_RE.sub("", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    text = re.sub(r"^\s*[-:|/]+\s*", "", text)
    return text.strip(" -")


def title_style(text: str) -> str:
    text = text.rstrip(" .。")
    for suffix, noun in TITLE_STYLE_SUFFIXES:
        if not text.endswith(suffix):
            continue
        stem = text[: -len(suffix)].rstrip()
        stem = re.sub(r"(?:을|를)\s*$", "", stem).rstrip()
        return f"{stem} {noun}".strip()
    return text


def sanitize_task_markdown(markdown: str) -> str:
    sanitized_lines: list[str] = []
    for line in markdown.strip().splitlines():
        stripped = line.strip()
        if stripped.startswith("-"):
            prefix = re.match(r"^(\s*-\s*)", line)
            item = stripped[1:].strip()
            bullet = prefix.group(1) if prefix else "- "
            sanitized_lines.append(f"{bullet}{title_style(sanitize_inline(item))}".rstrip())
        else:
            sanitized_lines.append(line.rstrip())
    return "\n".join(sanitized_lines).strip()


def load_json_map(value: str) -> dict[str, Any]:
    path = Path(value)
    raw = path.read_text(encoding="utf-8") if path.exists() else value
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("daily-note JSON input must be an object keyed by category")
    return data


def item_to_line(item: Any) -> str:
    if isinstance(item, dict):
        topic = title_style(sanitize_inline(str(item.get("topic", ""))))
        summary = title_style(sanitize_inline(str(item.get("summary", ""))))
        if topic and summary:
            return f"- {topic} - {summary}"
        if topic:
            return f"- {topic}"
        if summary:
            return f"- {summary}"
        return ""

    text = title_style(sanitize_inline(str(item)))
    if not text:
        return ""
    return f"- {text}"


def format_category_items(data: dict[str, Any] | str | None, empty_text: str = "확인된 항목 없음") -> str:
    if data is None:
        return f"**etc**\n- {empty_text}"
    if isinstance(data, str):
        text = sanitize_task_markdown(data)
        return text if text else f"**etc**\n- {empty_text}"

    blocks: list[str] = []
    ordered_categories = list(CATEGORIES) + [key for key in data.keys() if key not in CATEGORIES]
    for category in ordered_categories:
        raw_items = data.get(category)
        if raw_items is None:
            continue
        if isinstance(raw_items, str):
            raw_items = [raw_items]
        if not isinstance(raw_items, list):
            raw_items = [raw_items]

        lines = [item_to_line(item) for item in raw_items]
        lines = [line for line in lines if line]
        if lines:
            blocks.append(f"**{category}**\n" + "\n".join(lines))

    return "\n\n".join(blocks) if blocks else f"**etc**\n- {empty_text}"


def append_unique_lines(existing: str, addition: str) -> str:
    existing = normalize_block(existing)
    addition = normalize_block(addition)
    if not addition:
        return existing
    if not existing:
        return addition

    existing_lines = existing.splitlines()
    seen = {line.strip() for line in existing_lines if line.strip()}
    for line in addition.splitlines():
        stripped = line.strip()
        if stripped and stripped not in seen:
            existing_lines.append(line.rstrip())
            seen.add(stripped)
    return "\n".join(existing_lines).strip()


def ensure_top_section(markdown: str, title: str, level: int = 3) -> str:
    if find_section(markdown, title, level) is not None:
        return markdown
    if markdown and not markdown.endswith("\n"):
        markdown += "\n"
    return markdown.rstrip() + f"\n\n{'#' * level} {title}\n"


def append_to_section(markdown: str, title: str, addition: str, level: int = 3) -> str:
    if not normalize_block(addition):
        return markdown
    markdown = ensure_top_section(markdown, title, level)
    section = find_section(markdown, title, level)
    if section is None:
        raise ValueError(f"section not found after insertion: {title}")
    merged = append_unique_lines(markdown[section.content_start : section.content_end], addition)
    return replace_section_content(markdown, title, merged, level)


def build_template(
    yesterday: str,
    today: str,
    materials: str = "",
    workflow_update: str = "",
    skill_update: str = "",
) -> str:
    materials = normalize_block(materials) or "(참고 링크, 자료)"
    workflow_update = normalize_block(workflow_update) or "(일을 진행하면서 느낀 점, 프로세스 개선 아이디어)"
    skill_update = normalize_block(skill_update) or "(워크플로 자동화 아이디어, 스킬 개선 사항)"
    return normalize_block(
        f"""
### DS

##### 어제 한 일
{normalize_block(yesterday)}

##### 오늘 할 일
{normalize_block(today)}

##### 오늘의 workflow update
{workflow_update}

---

### Materials
{materials}

### 김아영

##### 오늘 그녀가 나를 따뜻하게 대한 장면

##### 오늘 그녀가 나를 생각해준 장면

##### 오늘 그녀의 부드러움이 관계에 준 가치

##### 오늘 내가 그녀에게 고마웠던 것

### Skill Update
{skill_update}
"""
    ) + "\n"


def merge_daily_note(
    existing_markdown: str,
    yesterday: dict[str, Any] | str | None,
    today: dict[str, Any] | str | None,
    materials: str = "",
    workflow_update: str = "",
    skill_update: str = "",
) -> str:
    yesterday_md = format_category_items(yesterday)
    today_md = format_category_items(today)

    if not normalize_block(existing_markdown):
        return build_template(yesterday_md, today_md, materials, workflow_update, skill_update)

    markdown = ensure_daily_sections(existing_markdown)
    markdown = replace_section_content(markdown, "어제 한 일", yesterday_md, 5)
    markdown = replace_section_content(markdown, "오늘 할 일", today_md, 5)
    markdown = append_to_section(markdown, "오늘의 workflow update", workflow_update, 5)
    markdown = append_to_section(markdown, "Materials", materials, 3)
    markdown = append_to_section(markdown, "Skill Update", skill_update, 3)
    return markdown.rstrip() + "\n"


def read_optional_text(path_or_text: str | None) -> str:
    if not path_or_text:
        return ""
    path = Path(path_or_text)
    if path.exists():
        return path.read_text(encoding="utf-8")
    return path_or_text


def read_existing(path: str | None) -> str:
    if path:
        file_path = Path(path)
        if file_path.exists():
            return file_path.read_text(encoding="utf-8")
        return ""
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print-kst-dates", action="store_true", help="Print KST date context as JSON and exit")
    parser.add_argument("--now-utc", help="ISO timestamp used with --print-kst-dates for testing")
    parser.add_argument("--existing-file", help="Existing Markdown note. Missing files are treated as empty notes.")
    parser.add_argument("--yesterday-json", help="JSON string or JSON file path keyed by category")
    parser.add_argument("--today-json", help="JSON string or JSON file path keyed by category")
    parser.add_argument("--yesterday-file", help="Reviewed Markdown for yesterday's work")
    parser.add_argument("--today-file", help="Reviewed Markdown for today's tasks")
    parser.add_argument("--materials-file", help="Markdown lines to append to Materials")
    parser.add_argument("--materials", help="Markdown lines to append to Materials")
    parser.add_argument("--workflow-update-file", help="Markdown lines to append to today's workflow update")
    parser.add_argument("--workflow-update", help="Markdown lines to append to today's workflow update")
    parser.add_argument("--skill-update-file", help="Markdown lines to append to Skill Update")
    parser.add_argument("--skill-update", help="Markdown lines to append to Skill Update")
    parser.add_argument("--output", help="Write merged Markdown to this file instead of stdout")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.print_kst_dates:
        now = datetime.fromisoformat(args.now_utc) if args.now_utc else None
        print(json.dumps(kst_dates(now), ensure_ascii=False, indent=2))
        return 0

    yesterday: dict[str, Any] | str | None = None
    today: dict[str, Any] | str | None = None
    if args.yesterday_json:
        yesterday = load_json_map(args.yesterday_json)
    elif args.yesterday_file:
        yesterday = read_optional_text(args.yesterday_file)
    if args.today_json:
        today = load_json_map(args.today_json)
    elif args.today_file:
        today = read_optional_text(args.today_file)

    materials = read_optional_text(args.materials_file) or read_optional_text(args.materials)
    workflow_update = read_optional_text(args.workflow_update_file) or read_optional_text(args.workflow_update)
    skill_update = read_optional_text(args.skill_update_file) or read_optional_text(args.skill_update)

    merged = merge_daily_note(
        existing_markdown=read_existing(args.existing_file),
        yesterday=yesterday,
        today=today,
        materials=materials,
        workflow_update=workflow_update,
        skill_update=skill_update,
    )

    if args.output:
        Path(args.output).write_text(merged, encoding="utf-8")
    else:
        sys.stdout.write(merged)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
