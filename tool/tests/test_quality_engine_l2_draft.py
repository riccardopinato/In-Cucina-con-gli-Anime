"""L2 pilot: isolated, source-locked doc repair and no unauthorized writes."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from quality_engine_l2_draft import (
    FIXED_ALLOWLIST, MAX_CHANGED_LINES, apply, plan, transform, validate_policy,
)

SHA = "a" * 40
REPO = "riccardopinato/In-Cucina-con-gli-Anime"
ALLOWED = sorted(FIXED_ALLOWLIST)
CONFIG = {
    "schemaVersion": 1, "enabled": True, "riskTier": "LOW_FORMAT_ONLY",
    "draftOnly": True, "autoMerge": False, "autoPublish": False,
    "allowedRule": "MD_BLANK_LINE_WHITESPACE",
    "eligiblePaths": ALLOWED,
}


def fixture(root: Path, content: bytes = b"Title\n \t\nBody\n") -> None:
    for p in ALLOWED:
        file = root / p
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(content)


class L2DraftRepairTests(unittest.TestCase):
    def test_planning_never_writes_and_only_allows_three_docs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture(root)
            outside = root / "authoring/recipes.json"
            outside.parent.mkdir(parents=True)
            outside.write_text('{"content": "KEEP"}', encoding="utf-8")
            before = {name: (root / name).read_bytes() for name in ALLOWED}
            policy = copy.deepcopy(CONFIG)
            result = plan(root, policy, source_sha=SHA, repository=REPO)
            self.assertEqual(result["counts"]["files"], 3)
            self.assertEqual(result["counts"]["lines"], 3)
            self.assertEqual(result["counts"]["bytesRemoved"], 6)
            self.assertEqual(result["contentCertification"], "NOT_CERTIFIED")
            self.assertEqual(result["humanApprovals"], 0)
            self.assertTrue(result["draftPrOnly"])
            self.assertFalse(result["autoMergeEnabled"])
            self.assertEqual(result["sourceSha"], SHA)
            self.assertEqual(result["changes"][0]["changedLineNumbers"], [2])
            self.assertEqual({name: (root / name).read_bytes() for name in ALLOWED}, before)
            self.assertEqual(outside.read_text(), '{"content": "KEEP"}')
            self.assertNotIn("Title", json.dumps(result))
            self.assertEqual(policy, CONFIG)

    def test_apply_limited_to_documents_with_checked_preimages(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture(root, b"Hello\r\n \t\r\nA  \r\n~~~js\r\n\t\r\n~~~\r\n")
            p = plan(root, CONFIG, source_sha=SHA, repository=REPO)
            changed = apply(root, CONFIG, p, source_sha=SHA, repository=REPO)
            self.assertEqual(changed, ALLOWED)
            for name in ALLOWED:
                self.assertEqual((root / name).read_bytes(),
                                 b"Hello\r\n\r\nA  \r\n~~~js\r\n\t\r\n~~~\r\n")
            after = plan(root, CONFIG, source_sha=SHA, repository=REPO)
            self.assertEqual(after["counts"]["files"], 0)

    def test_markdown_hardbreak_and_code_fence_preserved(self):
        before = b"Paragraph  \n~~~python\n \t\n~~~\n \t\nSome text\n"
        after, lines, removed = transform(before)
        self.assertEqual(after, b"Paragraph  \n~~~python\n \t\n~~~\n\nSome text\n")
        self.assertEqual(lines, (5,))
        self.assertEqual(removed, 2)
        data = b"intro\n  \n \n"
        out, lines, removed = transform(data)
        self.assertEqual(out, b"intro\n\n\n")
        self.assertEqual(lines, (2, 3))
        self.assertEqual(removed, 3)

    def test_fence_with_trailing_text_does_not_close_code_block(self):
        source = (b"Opening\n"
                  b"```python\n"
                  b"```not-a-closing-fence\n"
                  b"  \t\n"
                  b"```\n"
                  b"  \n"
                  b"Ending\n")
        fixed, lines, removed = transform(source)
        self.assertEqual(lines, (6,))
        self.assertEqual(removed, 2)
        self.assertIn(b"```not-a-closing-fence\n  \t\n```", fixed)
        self.assertIn(b"```\n\nEnding\n", fixed)

    def test_symlinked_parent_directory_rejected_before_write(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            other = root / "lib"
            other.mkdir()
            for allowed in ALLOWED:
                (other / Path(allowed).name).write_bytes(b"Header\n \n")
            (root / "docs").symlink_to(other, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "Symlinked parent"):
                plan(root, CONFIG, source_sha=SHA, repository=REPO)
            with self.assertRaisesRegex(ValueError, "Symlinked parent"):
                apply(root, CONFIG, {}, source_sha=SHA, repository=REPO)
            for allowed in ALLOWED:
                self.assertEqual((other / Path(allowed).name).read_bytes(),
                                 b"Header\n \n")

    def test_no_changes_is_clean_noop(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture(root, b"Correct markdown\n\nAnd text  \n")
            p = plan(root, CONFIG, source_sha=SHA, repository=REPO)
            self.assertEqual(p["changes"], [])
            self.assertEqual(apply(root, CONFIG, p, source_sha=SHA,
                                   repository=REPO), [])
            self.assertEqual((root / ALLOWED[0]).read_bytes(),
                             b"Correct markdown\n\nAnd text  \n")

    def test_tampered_plan_or_source_sha_or_policy_rejected_without_writes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture(root)
            p = plan(root, CONFIG, source_sha=SHA, repository=REPO)
            before = (root / ALLOWED[0]).read_bytes()
            bad = copy.deepcopy(p)
            bad["changes"][0]["path"] = "lib/main.dart"
            with self.assertRaisesRegex(ValueError, "Plan drift"):
                apply(root, CONFIG, bad, source_sha=SHA, repository=REPO)
            with self.assertRaisesRegex(ValueError, "Plan drift"):
                apply(root, CONFIG, p, source_sha="b"*40, repository=REPO)
            corrupted = copy.deepcopy(CONFIG)
            corrupted["autoMerge"] = True
            with self.assertRaisesRegex(ValueError, "safe draft"):
                apply(root, corrupted, p, source_sha=SHA, repository=REPO)
            self.assertEqual((root / ALLOWED[0]).read_bytes(), before)

    def test_changed_source_after_plan_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture(root)
            old = plan(root, CONFIG, source_sha=SHA, repository=REPO)
            file = root / ALLOWED[0]
            file.write_bytes(b"Modified\n\t\n")
            with self.assertRaisesRegex(ValueError, "Plan drift"):
                apply(root, CONFIG, old, source_sha=SHA, repository=REPO)
            self.assertEqual(file.read_bytes(), b"Modified\n\t\n")

    def test_unsafe_configuration_and_wrong_repository_rejected(self):
        for update in (
            {"enabled": False}, {"draftOnly": False}, {"autoPublish": True},
            {"autoMerge": True}, {"riskTier": "SECURITY"}, {"allowedRule": "PY_SHELL_TRUE"},
            {"eligiblePaths": ["lib/main.dart"]},
            {"eligiblePaths": [ALLOWED[0], ALLOWED[0]]},
            {"eligiblePaths": ["../docs/R1_QUALITY_ENGINE_V2_PILOT.md"]},
        ):
            cfg = {**CONFIG, **update}
            with self.assertRaises(ValueError, msg=str(update)):
                validate_policy(cfg)
        with tempfile.TemporaryDirectory() as temp:
            fixture(Path(temp))
            with self.assertRaisesRegex(ValueError, "one explicitly authorized"):
                plan(Path(temp), CONFIG, source_sha=SHA, repository="other/repo")
            with self.assertRaisesRegex(ValueError, "source SHA"):
                plan(Path(temp), CONFIG, source_sha="bad", repository=REPO)

    def test_symlink_is_rejected_even_if_target_stays_in_root(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture(root)
            target = root / ALLOWED[0]
            target.unlink()
            target.symlink_to(root / ALLOWED[1])
            with self.assertRaisesRegex(ValueError, "regular file"):
                plan(root, CONFIG, source_sha=SHA, repository=REPO)

    def test_byte_and_line_budget_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "bounded budget"):
            transform(b" \n" * (MAX_CHANGED_LINES + 1))
        with self.assertRaises(UnicodeDecodeError):
            transform(b"\xff\n")

    def test_writer_workflow_has_strict_triggers_and_pr_only(self):
        file = Path(".github/workflows/quality-engine-l2-draft.yml")
        wf = file.read_text(encoding="utf-8")
        self.assertIn("name: Quality Engine L2 — safe draft-only repair pilot", wf)
        self.assertIn("pull-requests: write", wf)
        self.assertIn("contents: write", wf)
        self.assertIn("gh pr create --draft", wf)
        self.assertIn("github.repository == 'riccardopinato/In-Cucina-con-gli-Anime'", wf)
        self.assertIn("persist-credentials: false", wf)
        self.assertNotIn("pull_request_target:", wf)
        self.assertNotIn("gh pr merge", wf)
        self.assertIn("quality_engine_l2_draft.py", wf)


if __name__ == "__main__":
    unittest.main()
