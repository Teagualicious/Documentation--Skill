#!/usr/bin/env python3
"""Create a deterministic, content-safe repository inventory.

The inventory identifies orientation files, likely entry points, source and test files,
deployment/configuration artifacts, and sensitive paths. It never emits file contents and
does not open files whose paths are considered sensitive.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

SCHEMA_VERSION = "1.0.0"

DEFAULT_EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "vendor",
    "bower_components",
    "dist",
    "build",
    "out",
    "target",
    "coverage",
    "htmlcov",
    ".next",
    ".nuxt",
    ".cache",
    ".pytest_cache",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".gradle",
    "Pods",
    "DerivedData",
}

IGNORED_FILES = {".DS_Store", "Thumbs.db", "desktop.ini"}

DEPENDENCY_FILENAMES = {
    "package.json",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "bun.lock",
    "bun.lockb",
    "pyproject.toml",
    "poetry.lock",
    "uv.lock",
    "Pipfile",
    "Pipfile.lock",
    "requirements.txt",
    "setup.py",
    "setup.cfg",
    "Cargo.toml",
    "Cargo.lock",
    "go.mod",
    "go.sum",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "settings.gradle",
    "settings.gradle.kts",
    "Gemfile",
    "Gemfile.lock",
    "composer.json",
    "composer.lock",
    "mix.exs",
    "mix.lock",
    "pubspec.yaml",
    "Package.swift",
}

DEPLOYMENT_FILENAMES = {
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "compose.yml",
    "compose.yaml",
    "Procfile",
    "vercel.json",
    "netlify.toml",
    "render.yaml",
    "serverless.yml",
    "serverless.yaml",
    "azure-pipelines.yml",
    "cloudbuild.yaml",
    "app.yaml",
    "fly.toml",
}

CONFIG_FILENAMES = {
    "Makefile",
    "Taskfile.yml",
    "Taskfile.yaml",
    "tox.ini",
    "pytest.ini",
    "mypy.ini",
    "ruff.toml",
    ".editorconfig",
    ".pre-commit-config.yaml",
    "tsconfig.json",
    "jsconfig.json",
    "vite.config.js",
    "vite.config.ts",
    "next.config.js",
    "next.config.mjs",
    "next.config.ts",
    "webpack.config.js",
    "eslint.config.js",
    "eslint.config.mjs",
}

ENTRYPOINT_FILENAMES = {
    "main.py",
    "app.py",
    "server.py",
    "manage.py",
    "wsgi.py",
    "asgi.py",
    "__main__.py",
    "main.go",
    "main.rs",
    "Program.cs",
    "index.js",
    "index.ts",
    "server.js",
    "server.ts",
    "app.js",
    "app.ts",
    "main.js",
    "main.ts",
    "main.tsx",
    "main.jsx",
}

SOURCE_LANGUAGES = {
    ".py": "Python",
    ".pyi": "Python",
    ".js": "JavaScript",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".jsx": "JavaScript JSX",
    ".ts": "TypeScript",
    ".tsx": "TypeScript JSX",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".cs": "C#",
    ".fs": "F#",
    ".fsx": "F#",
    ".rb": "Ruby",
    ".php": "PHP",
    ".swift": "Swift",
    ".c": "C",
    ".h": "C/C++ Header",
    ".cc": "C++",
    ".cpp": "C++",
    ".cxx": "C++",
    ".hpp": "C++ Header",
    ".scala": "Scala",
    ".ex": "Elixir",
    ".exs": "Elixir",
    ".erl": "Erlang",
    ".hrl": "Erlang",
    ".lua": "Lua",
    ".r": "R",
    ".R": "R",
    ".jl": "Julia",
    ".dart": "Dart",
    ".vue": "Vue",
    ".svelte": "Svelte",
    ".sh": "Shell",
    ".bash": "Shell",
    ".zsh": "Shell",
    ".fish": "Fish",
    ".ps1": "PowerShell",
    ".sql": "SQL",
    ".vim": "Vim script",
    ".sol": "Solidity",
}

DOCUMENT_EXTENSIONS = {".md", ".mdx", ".rst", ".adoc", ".txt"}
DATA_EXTENSIONS = {".csv", ".tsv", ".parquet", ".avro", ".ndjson", ".jsonl", ".sql"}
CONFIG_EXTENSIONS = {".toml", ".yaml", ".yml", ".ini", ".cfg", ".conf", ".properties", ".xml"}
ASSET_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".bmp", ".tif", ".tiff",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".mp3", ".wav", ".ogg", ".mp4", ".mov", ".avi", ".webm",
    ".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar",
}

SENSITIVE_EXACT_NAMES = {
    ".env",
    ".npmrc",
    ".pypirc",
    ".netrc",
    "id_rsa",
    "id_ed25519",
    "credentials.json",
    "secrets.json",
    "service-account.json",
    "service_account.json",
}
SENSITIVE_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".jks", ".keystore", ".kdbx"}
SENSITIVE_SEGMENTS = {".secrets", "secrets", "credentials", "private-keys", "private_keys"}

TEST_DIR_NAMES = {"test", "tests", "spec", "specs", "__tests__"}
DEPLOYMENT_DIR_NAMES = {".github", ".gitlab", "deploy", "deployment", "k8s", "kubernetes", "helm", "terraform", "infra", "infrastructure"}
DOC_DIR_NAMES = {"doc", "docs", "documentation"}


def _posix(path: Path) -> str:
    return path.as_posix()


def _path_parts(relative_path: str) -> tuple[str, ...]:
    return PurePosixPath(relative_path).parts


def _matches_custom_exclusion(relative_path: str, patterns: Iterable[str]) -> bool:
    parts = _path_parts(relative_path)
    for pattern in patterns:
        if pattern in parts or fnmatch.fnmatch(relative_path, pattern):
            return True
    return False


def sensitive_path_reason(relative_path: str) -> str | None:
    """Return a path-only sensitivity reason without opening the file."""

    path = PurePosixPath(relative_path)
    name = path.name
    lower_name = name.lower()
    lower_parts = {part.lower() for part in path.parts[:-1]}

    if lower_name in {value.lower() for value in SENSITIVE_EXACT_NAMES}:
        return "sensitive filename"
    if lower_name.startswith(".env.") and not lower_name.endswith((".example", ".sample", ".template")):
        return "environment values file"
    if any(lower_name.endswith(suffix) for suffix in SENSITIVE_SUFFIXES):
        return "credential or private-key file extension"
    if lower_parts & SENSITIVE_SEGMENTS:
        return "sensitive directory name"
    if "credential" in lower_name or ("secret" in lower_name and not lower_name.endswith((".example", ".sample", ".template"))):
        return "credential or secret-like filename"
    return None


def detect_binary(path: Path, sample_size: int = 8192) -> bool:
    """Detect likely binary data without returning or retaining file contents."""

    with path.open("rb") as handle:
        sample = handle.read(sample_size)
    if not sample:
        return False
    if b"\x00" in sample:
        return True
    text_bytes = bytes(range(32, 127)) + b"\n\r\t\b\f"
    non_text = sample.translate(None, text_bytes)
    return len(non_text) / len(sample) > 0.30


def is_test_path(relative_path: str) -> bool:
    path = PurePosixPath(relative_path)
    name = path.name.lower()
    parts = {part.lower() for part in path.parts[:-1]}
    return bool(parts & TEST_DIR_NAMES) or name.startswith("test_") or name.endswith(("_test.py", ".test.js", ".test.ts", ".spec.js", ".spec.ts", ".test.tsx", ".spec.tsx"))


def is_deployment_path(relative_path: str) -> bool:
    path = PurePosixPath(relative_path)
    parts = {part.lower() for part in path.parts[:-1]}
    name = path.name
    lower = name.lower()
    if name in DEPLOYMENT_FILENAMES:
        return True
    if ".github" in parts and "workflows" in parts and path.suffix.lower() in {".yml", ".yaml"}:
        return True
    if parts & DEPLOYMENT_DIR_NAMES:
        return True
    return lower.startswith(("dockerfile", "docker-compose", "compose.")) or path.suffix.lower() == ".tf"


def is_documentation_path(relative_path: str) -> bool:
    path = PurePosixPath(relative_path)
    parts = {part.lower() for part in path.parts[:-1]}
    lower_name = path.name.lower()
    if len(path.parts) == 1 and path.suffix.lower() in DOCUMENT_EXTENSIONS:
        return True
    if lower_name.startswith(("readme", "changelog", "contributing", "architecture", "security", "support", "license")):
        return True
    return bool(parts & DOC_DIR_NAMES) and path.suffix.lower() in DOCUMENT_EXTENSIONS


def is_dependency_manifest(name: str) -> bool:
    if name in DEPENDENCY_FILENAMES:
        return True
    lower = name.lower()
    return lower.startswith("requirements") and lower.endswith(".txt")


def is_config_path(relative_path: str) -> bool:
    path = PurePosixPath(relative_path)
    name = path.name
    lower = name.lower()
    if name in CONFIG_FILENAMES:
        return True
    if lower.endswith((".example", ".sample", ".template")) and ".env" in lower:
        return True
    if "config" in lower and path.suffix.lower() in CONFIG_EXTENSIONS | {".json", ".js", ".ts", ".mjs"}:
        return True
    return path.suffix.lower() in CONFIG_EXTENSIONS and len(path.parts) <= 3


def is_entry_point(relative_path: str) -> bool:
    path = PurePosixPath(relative_path)
    if path.name in ENTRYPOINT_FILENAMES:
        return True
    parts = path.parts
    return len(parts) >= 3 and parts[-3] == "cmd" and path.name == "main.go"


def classify_file(relative_path: str) -> tuple[str, int, str | None, str]:
    """Return category, analysis priority, language, and classification reason."""

    path = PurePosixPath(relative_path)
    name = path.name
    suffix = path.suffix
    lower_suffix = suffix.lower()
    language = SOURCE_LANGUAGES.get(suffix) or SOURCE_LANGUAGES.get(lower_suffix)

    if is_documentation_path(relative_path):
        return "documentation", 1, None, "orientation documentation"
    if is_dependency_manifest(name):
        return "dependency_manifest", 1, None, "dependency or build manifest"
    if is_deployment_path(relative_path):
        return "deployment", 1, language, "deployment or infrastructure definition"
    if is_entry_point(relative_path):
        return "source", 1, language, "likely application entry point"
    if is_test_path(relative_path):
        return "test", 2, language, "test path or test filename"
    if is_config_path(relative_path):
        return "configuration", 1, language, "project configuration"
    if language:
        return "source", 2, language, "recognized source-code extension"
    if lower_suffix in DATA_EXTENSIONS or lower_suffix in {".json", ".json5"}:
        return "data", 3, None, "data or structured-content extension"
    if lower_suffix in ASSET_EXTENSIONS:
        return "asset", 3, None, "asset or binary-document extension"
    if lower_suffix in DOCUMENT_EXTENSIONS:
        return "documentation", 2, None, "text documentation"
    return "unknown", 3, None, "unclassified file"


def inventory_repository(
    root: Path,
    *,
    max_file_bytes: int = 2_000_000,
    max_files: int = 50_000,
    custom_exclusions: Iterable[str] = (),
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Inventory a repository without returning file contents."""

    root = root.expanduser().resolve()
    if not root.exists():
        raise ValueError(f"path does not exist: {root}")
    if not root.is_dir():
        raise ValueError(f"path is not a directory: {root}")
    if max_file_bytes < 0:
        raise ValueError("max_file_bytes must be non-negative")
    if max_files < 1:
        raise ValueError("max_files must be at least 1")

    custom = tuple(custom_exclusions)
    files: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    skipped_directories: list[dict[str, str]] = []
    top_level_directories: set[str] = set()
    reached_limit = False

    for current_root, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        current = Path(current_root)
        relative_current = current.relative_to(root)

        retained_dirs: list[str] = []
        for dirname in sorted(dirnames, key=str.casefold):
            candidate = current / dirname
            relative = _posix(candidate.relative_to(root))
            if candidate.is_symlink():
                skipped_directories.append({"path": relative, "reason": "symbolic-link directory not followed"})
            elif dirname in DEFAULT_EXCLUDED_DIRS:
                skipped_directories.append({"path": relative, "reason": "default excluded directory"})
            elif _matches_custom_exclusion(relative, custom):
                skipped_directories.append({"path": relative, "reason": "custom exclusion"})
            else:
                retained_dirs.append(dirname)
                if relative_current == Path("."):
                    top_level_directories.add(dirname)
        dirnames[:] = retained_dirs

        for filename in sorted(filenames, key=str.casefold):
            if len(files) >= max_files:
                reached_limit = True
                break

            path = current / filename
            relative = _posix(path.relative_to(root))

            if filename in IGNORED_FILES:
                skipped.append({"path": relative, "reason": "ignored operating-system metadata"})
                continue
            if _matches_custom_exclusion(relative, custom):
                skipped.append({"path": relative, "reason": "custom exclusion"})
                continue
            if path.is_symlink():
                skipped.append({"path": relative, "reason": "symbolic-link file not followed"})
                continue

            try:
                stat = path.stat()
            except OSError as exc:
                skipped.append({"path": relative, "reason": f"unable to stat file: {exc.__class__.__name__}"})
                continue

            category, priority, language, classification_reason = classify_file(relative)
            sensitive_reason = sensitive_path_reason(relative)
            oversized = stat.st_size > max_file_bytes
            binary: bool | None = None
            readable = False
            eligibility_reason = "eligible for targeted analysis"

            if sensitive_reason:
                eligibility_reason = f"not read: {sensitive_reason}"
            elif oversized:
                eligibility_reason = f"not read: exceeds max_file_bytes ({max_file_bytes})"
            else:
                try:
                    binary = detect_binary(path)
                    readable = not binary
                    if binary:
                        eligibility_reason = "not read as text: binary sample detected"
                except OSError as exc:
                    eligibility_reason = f"not read: {exc.__class__.__name__}"

            files.append(
                {
                    "path": relative,
                    "size_bytes": stat.st_size,
                    "extension": path.suffix.lower(),
                    "category": category,
                    "analysis_priority": priority,
                    "language": language,
                    "entry_point": is_entry_point(relative),
                    "binary": binary,
                    "sensitive_path": bool(sensitive_reason),
                    "sensitive_reason": sensitive_reason,
                    "analysis_eligible": readable,
                    "eligibility_reason": eligibility_reason,
                    "classification_reason": classification_reason,
                }
            )

        if reached_limit:
            break

    files.sort(key=lambda item: item["path"].casefold())
    skipped.sort(key=lambda item: item["path"].casefold())
    skipped_directories.sort(key=lambda item: item["path"].casefold())

    category_counts = Counter(item["category"] for item in files)
    priority_counts = Counter(str(item["analysis_priority"]) for item in files)
    language_counts = Counter(item["language"] for item in files if item["language"])

    def paths_for(*, category: str | None = None, entry_point: bool | None = None, priority: int | None = None) -> list[str]:
        result = []
        for item in files:
            if category is not None and item["category"] != category:
                continue
            if entry_point is not None and item["entry_point"] is not entry_point:
                continue
            if priority is not None and item["analysis_priority"] != priority:
                continue
            if item["sensitive_path"]:
                continue
            result.append(item["path"])
        return result

    manifest_paths = paths_for(category="dependency_manifest")
    package_roots = sorted({str(PurePosixPath(path).parent) for path in manifest_paths}, key=str.casefold)

    limitations: list[str] = []
    if reached_limit:
        limitations.append(f"Inventory stopped after max_files={max_files}.")
    if any(item["sensitive_path"] for item in files):
        limitations.append("Sensitive paths were recorded from filenames only and were not opened.")
    if any(item["size_bytes"] > max_file_bytes for item in files):
        limitations.append("Oversized files were inventoried by metadata but not sampled.")
    if skipped_directories:
        limitations.append("Excluded or symbolic-link directories were not traversed.")

    generated = generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    return {
        "schema_version": SCHEMA_VERSION,
        "root": str(root),
        "generated_at": generated,
        "options": {
            "max_file_bytes": max_file_bytes,
            "max_files": max_files,
            "custom_exclusions": list(custom),
            "follow_symlinks": False,
            "emit_file_contents": False,
        },
        "summary": {
            "total_files": len(files),
            "total_bytes": sum(item["size_bytes"] for item in files),
            "analysis_eligible_files": sum(bool(item["analysis_eligible"]) for item in files),
            "sensitive_paths": sum(bool(item["sensitive_path"]) for item in files),
            "binary_files": sum(item["binary"] is True for item in files),
            "oversized_files": sum(item["size_bytes"] > max_file_bytes for item in files),
            "skipped_files": len(skipped),
            "skipped_directories": len(skipped_directories),
            "category_counts": dict(sorted(category_counts.items())),
            "priority_counts": dict(sorted(priority_counts.items())),
            "language_counts": dict(sorted(language_counts.items())),
        },
        "orientation": {
            "read_first": paths_for(priority=1),
            "documentation": paths_for(category="documentation"),
            "dependency_manifests": manifest_paths,
            "deployment": paths_for(category="deployment"),
            "configuration": paths_for(category="configuration"),
            "entry_points": paths_for(entry_point=True),
            "tests": paths_for(category="test"),
            "package_roots": package_roots,
            "likely_monorepo": len([root for root in package_roots if root != "."]) > 1,
            "top_level_directories": sorted(top_level_directories, key=str.casefold),
        },
        "files": files,
        "skipped_files": skipped,
        "skipped_directories": skipped_directories,
        "analysis_limitations": limitations,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Repository or project directory")
    parser.add_argument("--output", type=Path, help="Write JSON to this path instead of stdout")
    parser.add_argument("--max-file-bytes", type=int, default=2_000_000)
    parser.add_argument("--max-files", type=int, default=50_000)
    parser.add_argument("--exclude", action="append", default=[], help="Directory name or relative glob to exclude; repeatable")
    parser.add_argument("--generated-at", help="Override generated_at for reproducible tests")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON")
    parser.add_argument("--fail-on-sensitive", action="store_true", help="Return exit code 3 when sensitive paths are found")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        inventory = inventory_repository(
            args.path,
            max_file_bytes=args.max_file_bytes,
            max_files=args.max_files,
            custom_exclusions=args.exclude,
            generated_at=args.generated_at,
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    indent = None if args.compact else 2
    serialized = json.dumps(inventory, indent=indent, sort_keys=False) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
        print(f"Repository inventory written to {args.output}.")
    else:
        sys.stdout.write(serialized)

    if args.fail_on_sensitive and inventory["summary"]["sensitive_paths"]:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
