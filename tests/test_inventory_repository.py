from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.inventory_repository import inventory_repository, sensitive_path_reason

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "inventory_repository.py"


class RepositoryInventoryTests(unittest.TestCase):
    def make_repository(self, root: Path) -> str:
        (root / "src").mkdir()
        (root / "tests").mkdir()
        (root / ".github" / "workflows").mkdir(parents=True)
        (root / "node_modules" / "ignored").mkdir(parents=True)
        (root / "dist").mkdir()
        (root / "assets").mkdir()
        (root / "README.md").write_text("# Sample\n", encoding="utf-8")
        (root / "pyproject.toml").write_text("[project]\nname='sample'\n", encoding="utf-8")
        (root / "src" / "main.py").write_text("print('ok')\n", encoding="utf-8")
        (root / "src" / "helper.py").write_text("VALUE = 1\n", encoding="utf-8")
        (root / "tests" / "test_main.py").write_text("def test_ok(): assert True\n", encoding="utf-8")
        (root / ".github" / "workflows" / "ci.yml").write_text("name: ci\n", encoding="utf-8")
        (root / "node_modules" / "ignored" / "index.js").write_text("secret vendor\n", encoding="utf-8")
        (root / "dist" / "bundle.js").write_text("generated\n", encoding="utf-8")
        secret = "SYNTHETIC_SHOULD_NOT_APPEAR"
        (root / ".env").write_text(f"TOKEN={secret}\n", encoding="utf-8")
        (root / ".env.example").write_text("TOKEN=replace-me\n", encoding="utf-8")
        (root / "assets" / "image.bin").write_bytes(b"\x00\x01\x02")
        (root / "large.txt").write_text("x" * 50, encoding="utf-8")
        return secret

    def test_inventory_classifies_and_excludes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_repository(root)
            result = inventory_repository(root, max_file_bytes=20, generated_at="2026-08-20T17:00:00Z")
            by_path = {item["path"]: item for item in result["files"]}

            self.assertEqual(by_path["README.md"]["category"], "documentation")
            self.assertEqual(by_path["pyproject.toml"]["category"], "dependency_manifest")
            self.assertTrue(by_path["src/main.py"]["entry_point"])
            self.assertEqual(by_path["tests/test_main.py"]["category"], "test")
            self.assertEqual(by_path[".github/workflows/ci.yml"]["category"], "deployment")
            self.assertNotIn("node_modules/ignored/index.js", by_path)
            self.assertNotIn("dist/bundle.js", by_path)
            self.assertIn("src/main.py", result["orientation"]["entry_points"])

    def test_sensitive_file_is_not_opened_or_emitted(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            secret = self.make_repository(root)
            result = inventory_repository(root, generated_at="2026-08-20T17:00:00Z")
            by_path = {item["path"]: item for item in result["files"]}
            env = by_path[".env"]
            self.assertTrue(env["sensitive_path"])
            self.assertFalse(env["analysis_eligible"])
            self.assertIsNone(env["binary"])
            self.assertNotIn(secret, json.dumps(result))
            self.assertFalse(by_path[".env.example"]["sensitive_path"])

    def test_binary_and_oversized_files_are_not_text_eligible(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_repository(root)
            result = inventory_repository(root, max_file_bytes=20, generated_at="2026-08-20T17:00:00Z")
            by_path = {item["path"]: item for item in result["files"]}
            self.assertTrue(by_path["assets/image.bin"]["binary"])
            self.assertFalse(by_path["assets/image.bin"]["analysis_eligible"])
            self.assertIsNone(by_path["large.txt"]["binary"])
            self.assertFalse(by_path["large.txt"]["analysis_eligible"])
            expected_oversized = sum(item["size_bytes"] > 20 for item in result["files"])
            self.assertEqual(result["summary"]["oversized_files"], expected_oversized)
            self.assertGreaterEqual(expected_oversized, 1)

    def test_paths_are_sorted_deterministically(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_repository(root)
            result = inventory_repository(root, generated_at="2026-08-20T17:00:00Z")
            paths = [item["path"] for item in result["files"]]
            self.assertEqual(paths, sorted(paths, key=str.casefold))

    def test_custom_exclusion(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_repository(root)
            result = inventory_repository(root, custom_exclusions=["tests"], generated_at="2026-08-20T17:00:00Z")
            self.assertNotIn("tests/test_main.py", {item["path"] for item in result["files"]})

    def test_sensitive_path_patterns(self) -> None:
        self.assertIsNotNone(sensitive_path_reason("credentials/service.json"))
        self.assertIsNotNone(sensitive_path_reason("certs/private.key"))
        self.assertIsNone(sensitive_path_reason(".env.example"))

    def test_cli_writes_json_and_can_fail_on_sensitive(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            root.mkdir()
            self.make_repository(root)
            output = Path(temp) / "inventory.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(root),
                    "--output",
                    str(output),
                    "--generated-at",
                    "2026-08-20T17:00:00Z",
                    "--fail-on-sensitive",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 3, completed.stderr)
            data = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(data["schema_version"], "1.0.0")
            self.assertGreater(data["summary"]["sensitive_paths"], 0)


if __name__ == "__main__":
    unittest.main()
