from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.validate_evidence import validate_evidence_document, validate_manifest_document

FIXTURES = Path(__file__).parent / "fixtures"


def load_fixture(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class EvidenceValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.valid = load_fixture("evidence_valid.json")

    def test_valid_evidence_passes(self) -> None:
        self.assertEqual(validate_evidence_document(self.valid), [])

    def test_duplicate_fact_id_fails(self) -> None:
        invalid = copy.deepcopy(self.valid)
        invalid["facts"].append(copy.deepcopy(invalid["facts"][0]))
        errors = validate_evidence_document(invalid)
        self.assertTrue(any("duplicate id 'FACT-001'" in error for error in errors), errors)

    def test_confirmed_fact_requires_source(self) -> None:
        invalid = copy.deepcopy(self.valid)
        invalid["facts"][0]["sources"] = []
        errors = validate_evidence_document(invalid)
        self.assertTrue(any("confirmed items require at least one source" in error for error in errors), errors)

    def test_invalid_verification_and_implementation_states_fail(self) -> None:
        invalid = copy.deepcopy(self.valid)
        invalid["facts"][0]["verification_state"] = "probably"
        invalid["facts"][0]["implementation_state"] = "maybe"
        errors = validate_evidence_document(invalid)
        self.assertTrue(any("verification_state" in error for error in errors), errors)
        self.assertTrue(any("implementation_state" in error for error in errors), errors)

    def test_conflict_requires_two_sources_and_details(self) -> None:
        invalid = copy.deepcopy(self.valid)
        invalid["facts"][0]["verification_state"] = "conflict"
        invalid["facts"][0].pop("conflict_details", None)
        errors = validate_evidence_document(invalid)
        self.assertTrue(any("at least two sources" in error for error in errors), errors)
        self.assertTrue(any("conflict_details" in error for error in errors), errors)

    def test_incomplete_source_version_fails(self) -> None:
        invalid = copy.deepcopy(self.valid)
        del invalid["source_version"]["revision"]
        errors = validate_evidence_document(invalid)
        self.assertTrue(any("missing required key 'revision'" in error for error in errors), errors)

    def test_answered_question_requires_answer(self) -> None:
        invalid = copy.deepcopy(self.valid)
        invalid["open_questions"][0]["status"] = "answered"
        errors = validate_evidence_document(invalid)
        self.assertTrue(any("answered questions require an answer" in error for error in errors), errors)


class ManifestValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.valid = load_fixture("manifest_valid.json")

    def test_valid_manifest_passes(self) -> None:
        self.assertEqual(validate_manifest_document(self.valid), [])

    def test_manifest_requires_both_documents(self) -> None:
        invalid = copy.deepcopy(self.valid)
        del invalid["documents"]["user"]
        errors = validate_manifest_document(invalid)
        self.assertTrue(any("missing required key 'user'" in error for error in errors), errors)

    def test_manifest_rejects_invalid_check_state(self) -> None:
        invalid = copy.deepcopy(self.valid)
        invalid["validation"]["checks"][0]["status"] = "fine"
        errors = validate_manifest_document(invalid)
        self.assertTrue(any("invalid value 'fine'" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
