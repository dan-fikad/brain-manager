import importlib.util
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "merge_daily_note.py"
SPEC = importlib.util.spec_from_file_location("merge_daily_note", SCRIPT)
merge_daily_note = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["merge_daily_note"] = merge_daily_note
SPEC.loader.exec_module(merge_daily_note)


class MergeDailyNoteTest(unittest.TestCase):
    def test_kst_dates_use_asia_seoul(self):
        dates = merge_daily_note.kst_dates(datetime(2026, 5, 26, 15, 30, tzinfo=timezone.utc))

        self.assertEqual(dates["today"], "2026-05-27")
        self.assertEqual(dates["yesterday"], "2026-05-26")
        self.assertEqual(dates["today_path"], "fikad-brain/2026-05-27.md")
        self.assertEqual(dates["obsidian_today_path"], "2026-05-27.md")

    def test_new_note_uses_template_and_sanitizes_tasks(self):
        note = merge_daily_note.merge_daily_note(
            existing_markdown="",
            yesterday={
                "hooksnap": [
                    {
                        "topic": "TG-123 랜딩 v2",
                        "summary": "https://example.com 공개 홈과 인증 흐름을 확인했다",
                    }
                ]
            },
            today={"ops": ["DAI-11 routine 전환 - 첫 자동화 단위를 정한다"]},
            materials="- Jira: TG Done 조회",
            workflow_update="- Linear 일부 조회 실패를 기록했다.",
            skill_update="- 데이터 누락 가능성을 다음 실행에서 줄인다.",
        )

        self.assertIn("### DS", note)
        self.assertIn("**hooksnap**\n- 랜딩 v2 - 공개 홈과 인증 흐름 확인", note)
        self.assertIn("**ops**\n- routine 전환 - 첫 자동화 단위 선정", note)
        self.assertIn("### 김아영", note)
        self.assertIn("### Skill Update", note)
        self.assertNotIn("TG-123", note.split("##### 오늘 할 일", 1)[1].split("##### 오늘의 workflow update", 1)[0])
        self.assertNotIn("https://example.com", note)

    def test_existing_note_replaces_tasks_and_preserves_personal_sections(self):
        existing = """### DS

##### 어제 한 일
**etc**
- 오래된 항목 - 제거된다

##### 오늘 할 일
**ops**
- 예전 할 일 - 제거된다

##### 오늘의 workflow update
- 기존 업데이트

---

### Materials
- 기존 자료

### 김아영

##### 오늘 그녀가 나를 따뜻하게 대한 장면
- 기존 개인 메모

### Skill Update
- 기존 스킬 메모
"""

        note = merge_daily_note.merge_daily_note(
            existing_markdown=existing,
            yesterday={"hooksnap": ["랜딩 v2 검증 - 배포 화면을 다듬었다"]},
            today={"meeting": ["고객 미팅 - 액션 아이템을 정리한다"]},
            materials="- 새 자료",
            workflow_update="- 새 업데이트",
            skill_update="- 새 스킬 메모",
        )

        self.assertNotIn("오래된 항목", note)
        self.assertNotIn("예전 할 일", note)
        self.assertIn("**hooksnap**\n- 랜딩 v2 검증 - 배포 화면 개선", note)
        self.assertIn("**meeting**\n- 고객 미팅 - 액션 아이템 정리", note)
        self.assertIn("- 기존 개인 메모", note)
        self.assertIn("- 기존 자료", note)
        self.assertIn("- 새 자료", note)
        self.assertIn("- 기존 업데이트", note)
        self.assertIn("- 새 업데이트", note)
        self.assertIn("- 기존 스킬 메모", note)
        self.assertIn("- 새 스킬 메모", note)

    def test_missing_existing_subsections_are_inserted(self):
        existing = """### Materials
- 상단 자료

### DS

##### 오늘 할 일
**ops**
- 유지되지 않을 오늘 항목

### 김아영

##### 오늘 내가 그녀에게 고마웠던 것
- 기존 감사 메모
"""

        note = merge_daily_note.merge_daily_note(
            existing_markdown=existing,
            yesterday={"etc": ["학습 - 자료를 정리했다"]},
            today={"ops": ["정리 - 후속 작업을 진행한다"]},
        )

        self.assertIn("##### 어제 한 일", note)
        self.assertIn("**etc**\n- 학습 - 자료 정리", note)
        self.assertIn("**ops**\n- 정리 - 후속 작업 진행", note)
        self.assertIn("- 상단 자료", note)
        self.assertIn("- 기존 감사 메모", note)


if __name__ == "__main__":
    unittest.main()
