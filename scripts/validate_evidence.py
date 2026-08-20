#!/usr/bin/env python3
"""Validate Project Documentation Builder evidence and manifest files.

The validator intentionally uses only the Python standard library. JSON Schema files
remain the formal contracts; this module adds high-value semantic checks such as
unique IDs and evidence requirements that depend on verification state.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

VERIFICATION_STATES = {"confirmed", "inferred", "unknown", "conflict"}
IMPLEMENTATION_STATES = {"current", "intended", "planned", "deprecated", "unknown"}
QUESTION_STATES = {"open", "answered", "deferred", "not_applicable"}
SOURCE_TYPES = {
    "github_repository",
    "local_repository",
    "source_archive",
    "low_code_export",
    "description",
    "hybrid",
}
MATURITY_STATES = {"experimental", "testing", "production", "deprecated", "unknown"}
VALIDATION_STATES = {"passed", "partial", "failed"}
CHECK_STATES = {"passed", "partial", "failed", "not_run"}


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _require_keys(value: Any, keys: Iterable[str], path: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{path}: expected an object")
        return
    for key in keys:
        if key not in value:
            errors.append(f"{path}: missing required key '{key}'")


def _check_nonempty(value: Any, path: str, errors: list[str]) -> None:
    if not _is_nonempty_string(value):
        errors.append(f"{path}: expected a non-empty string")


def _validate_source(source: Any, path: str, errors: list[str]) -> None:
    required = ("type", "location", "version")
    _require_keys(source, required, path, errors)
    if not isinstance(source, dict):
        return
    for key in required:
        if key in source:
            _check_nonempty(source[key], f"{path}.{key}", errors)


def _validate_source_version(value: Any, path: str, errors: list[str]) -> None:
    required = ("source_type", "locator", "ref", "revision", "environment", "analyzed_at")
    _require_keys(value, required, path, errors)
    if not isinstance(value, dict):
        return
    for key in required:
        if key in value:
            _check_nonempty(value[key], f"{path}.{key}", errors)


def _validate_evidence_state(
    item: dict[str, Any], path: str, errors: list[str], *, require_confidence: bool = True
) -> None:
    verification = item.get("verification_state")
    implementation = item.get("implementation_state")
    sources = item.get("sources")

    if verification not in VERIFICATION_STATES:
        errors.append(f"{path}.verification_state: invalid value {verification!r}")
    if implementation not in IMPLEMENTATION_STATES:
        errors.append(f"{path}.implementation_state: invalid value {implementation!r}")

    if require_confidence:
        confidence = item.get("confidence")
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
            errors.append(f"{path}.confidence: expected a number from 0 to 1")
        elif not 0 <= float(confidence) <= 1:
            errors.append(f"{path}.confidence: must be from 0 to 1")

    if not isinstance(sources, list):
        errors.append(f"{path}.sources: expected an array")
        sources = []
    else:
        for index, source in enumerate(sources):
            _validate_source(source, f"{path}.sources[{index}]", errors)

    if verification == "confirmed" and not sources:
        errors.append(f"{path}: confirmed items require at least one source")
    elif verification == "inferred" and not sources and not _is_nonempty_string(item.get("rationale")):
        errors.append(f"{path}: inferred items require a source or rationale")
    elif verification == "unknown" and not _is_nonempty_string(item.get("rationale")):
        errors.append(f"{path}: unknown items require a rationale")
    elif verification == "conflict":
        if len(sources) < 2:
            errors.append(f"{path}: conflict items require at least two sources")
        if not _is_nonempty_string(item.get("conflict_details")):
            errors.append(f"{path}: conflict items require conflict_details")


def _check_unique_ids(items: Any, path: str, errors: list[str]) -> None:
    if not isinstance(items, list):
        errors.append(f"{path}: expected an array")
        return
    seen: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"{path}[{index}]: expected an object")
            continue
        item_id = item.get("id")
        if not _is_nonempty_string(item_id):
            errors.append(f"{path}[{index}].id: expected a non-empty string")
            continue
        if item_id in seen:
            errors.append(f"{path}: duplicate id '{item_id}'")
        seen.add(item_id)


def validate_evidence_document(data: Any) -> list[str]:
    """Return semantic validation errors for an evidence document."""

    errors: list[str] = []
    required = (
        "schema_version",
        "project",
        "source_version",
        "facts",
        "components",
        "workflows",
        "open_questions",
        "analysis_limitations",
    )
    _require_keys(data, required, "$", errors)
    if not isinstance(data, dict):
        return errors

    if data.get("schema_version") != "1.0.0":
        errors.append("$.schema_version: expected '1.0.0'")

    project = data.get("project")
    _require_keys(project, ("id", "name", "source_type", "scope", "audiences"), "$.project", errors)
    if isinstance(project, dict):
        for key in ("id", "name", "scope"):
            if key in project:
                _check_nonempty(project[key], f"$.project.{key}", errors)
        if project.get("source_type") not in SOURCE_TYPES:
            errors.append(f"$.project.source_type: invalid value {project.get('source_type')!r}")
        audiences = project.get("audiences")
        if not isinstance(audiences, list) or not audiences or not all(_is_nonempty_string(v) for v in audiences):
            errors.append("$.project.audiences: expected a non-empty array of strings")
        if "maturity" in project and project.get("maturity") not in MATURITY_STATES:
            errors.append(f"$.project.maturity: invalid value {project.get('maturity')!r}")

    _validate_source_version(data.get("source_version"), "$.source_version", errors)

    facts = data.get("facts")
    _check_unique_ids(facts, "$.facts", errors)
    if isinstance(facts, list):
        for index, fact in enumerate(facts):
            path = f"$.facts[{index}]"
            _require_keys(
                fact,
                ("id", "category", "claim", "verification_state", "implementation_state", "confidence", "sources", "used_in"),
                path,
                errors,
            )
            if not isinstance(fact, dict):
                continue
            for key in ("category", "claim"):
                if key in fact:
                    _check_nonempty(fact[key], f"{path}.{key}", errors)
            if "used_in" in fact and not isinstance(fact.get("used_in"), list):
                errors.append(f"{path}.used_in: expected an array")
            _validate_evidence_state(fact, path, errors)

    components = data.get("components")
    _check_unique_ids(components, "$.components", errors)
    if isinstance(components, list):
        for index, component in enumerate(components):
            path = f"$.components[{index}]"
            _require_keys(
                component,
                ("id", "name", "type", "purpose", "verification_state", "implementation_state", "sources"),
                path,
                errors,
            )
            if not isinstance(component, dict):
                continue
            for key in ("name", "type", "purpose"):
                if key in component:
                    _check_nonempty(component[key], f"{path}.{key}", errors)
            _validate_evidence_state(component, path, errors, require_confidence=False)

    workflows = data.get("workflows")
    _check_unique_ids(workflows, "$.workflows", errors)
    if isinstance(workflows, list):
        for index, workflow in enumerate(workflows):
            path = f"$.workflows[{index}]"
            _require_keys(
                workflow,
                ("id", "name", "actor", "trigger", "steps", "success_state", "verification_state", "implementation_state", "sources"),
                path,
                errors,
            )
            if not isinstance(workflow, dict):
                continue
            for key in ("name", "actor", "trigger", "success_state"):
                if key in workflow:
                    _check_nonempty(workflow[key], f"{path}.{key}", errors)
            steps = workflow.get("steps")
            if not isinstance(steps, list) or not steps:
                errors.append(f"{path}.steps: expected a non-empty array")
            else:
                orders: list[int] = []
                for step_index, step in enumerate(steps):
                    step_path = f"{path}.steps[{step_index}]"
                    _require_keys(step, ("order", "name", "description"), step_path, errors)
                    if not isinstance(step, dict):
                        continue
                    order = step.get("order")
                    if not isinstance(order, int) or isinstance(order, bool) or order < 1:
                        errors.append(f"{step_path}.order: expected an integer >= 1")
                    else:
                        orders.append(order)
                    for key in ("name", "description"):
                        if key in step:
                            _check_nonempty(step[key], f"{step_path}.{key}", errors)
                if len(orders) != len(set(orders)):
                    errors.append(f"{path}.steps: duplicate order values")
            duplicate_risk = workflow.get("duplicate_risk")
            if duplicate_risk is not None and duplicate_risk not in {"none", "possible", "confirmed", "unknown"}:
                errors.append(f"{path}.duplicate_risk: invalid value {duplicate_risk!r}")
            _validate_evidence_state(workflow, path, errors, require_confidence=False)

    questions = data.get("open_questions")
    _check_unique_ids(questions, "$.open_questions", errors)
    if isinstance(questions, list):
        for index, question in enumerate(questions):
            path = f"$.open_questions[{index}]"
            _require_keys(question, ("id", "question", "why_it_matters", "status", "related_ids"), path, errors)
            if not isinstance(question, dict):
                continue
            for key in ("question", "why_it_matters"):
                if key in question:
                    _check_nonempty(question[key], f"{path}.{key}", errors)
            if question.get("status") not in QUESTION_STATES:
                errors.append(f"{path}.status: invalid value {question.get('status')!r}")
            if not isinstance(question.get("related_ids"), list):
                errors.append(f"{path}.related_ids: expected an array")
            if question.get("status") == "answered" and not _is_nonempty_string(question.get("answer")):
                errors.append(f"{path}: answered questions require an answer")
            answer_sources = question.get("answer_sources", [])
            if not isinstance(answer_sources, list):
                errors.append(f"{path}.answer_sources: expected an array")
            else:
                for source_index, source in enumerate(answer_sources):
                    _validate_source(source, f"{path}.answer_sources[{source_index}]", errors)

    if not isinstance(data.get("analysis_limitations"), list):
        errors.append("$.analysis_limitations: expected an array")

    return errors


def validate_manifest_document(data: Any) -> list[str]:
    """Return semantic validation errors for a documentation manifest."""

    errors: list[str] = []
    required = (
        "schema_version", "project_id", "evidence_file", "source_version", "generated_at",
        "documents", "validation", "change_summary", "unresolved_question_ids",
    )
    _require_keys(data, required, "$", errors)
    if not isinstance(data, dict):
        return errors

    if data.get("schema_version") != "1.0.0":
        errors.append("$.schema_version: expected '1.0.0'")
    for key in ("project_id", "evidence_file", "generated_at"):
        if key in data:
            _check_nonempty(data[key], f"$.{key}", errors)
    _validate_source_version(data.get("source_version"), "$.source_version", errors)
    if "previous_source_version" in data:
        _validate_source_version(data.get("previous_source_version"), "$.previous_source_version", errors)

    documents = data.get("documents")
    _require_keys(documents, ("developer", "user"), "$.documents", errors)
    if isinstance(documents, dict):
        for kind in ("developer", "user"):
            document = documents.get(kind)
            path = f"$.documents.{kind}"
            _require_keys(document, ("filename", "sections", "evidence_fact_ids"), path, errors)
            if not isinstance(document, dict):
                continue
            _check_nonempty(document.get("filename"), f"{path}.filename", errors)
            for key in ("sections", "evidence_fact_ids"):
                if not isinstance(document.get(key), list):
                    errors.append(f"{path}.{key}: expected an array")

    validation = data.get("validation")
    _require_keys(validation, ("status", "checks"), "$.validation", errors)
    if isinstance(validation, dict):
        if validation.get("status") not in VALIDATION_STATES:
            errors.append(f"$.validation.status: invalid value {validation.get('status')!r}")
        checks = validation.get("checks")
        if not isinstance(checks, list):
            errors.append("$.validation.checks: expected an array")
        else:
            for index, check in enumerate(checks):
                path = f"$.validation.checks[{index}]"
                _require_keys(check, ("name", "status"), path, errors)
                if not isinstance(check, dict):
                    continue
                _check_nonempty(check.get("name"), f"{path}.name", errors)
                if check.get("status") not in CHECK_STATES:
                    errors.append(f"{path}.status: invalid value {check.get('status')!r}")

    for key in ("change_summary", "unresolved_question_ids"):
        if not isinstance(data.get(key), list):
            errors.append(f"$.{key}: expected an array")

    return errors


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc


def infer_kind(path: Path, data: Any) -> str:
    if isinstance(data, dict) and "documents" in data and "evidence_file" in data:
        return "manifest"
    if path.name == "documentation-manifest.json":
        return "manifest"
    return "evidence"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Evidence or documentation-manifest JSON file")
    parser.add_argument("--kind", choices=("auto", "evidence", "manifest"), default="auto")
    args = parser.parse_args(argv)

    try:
        data = load_json(args.path)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    kind = infer_kind(args.path, data) if args.kind == "auto" else args.kind
    errors = validate_manifest_document(data) if kind == "manifest" else validate_evidence_document(data)

    if errors:
        print(f"Validation failed for {args.path} ({kind}):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validation passed for {args.path} ({kind}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
