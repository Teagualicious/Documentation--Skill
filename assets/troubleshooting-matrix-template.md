# Troubleshooting Matrix Template

Use one row per user-visible symptom.

| What the user sees | Likely scope | What to check | Safe user action | Operator/admin action | Duplicate or destructive risk | Escalate when | Evidence source |
|---|---|---|---|---|---|---|---|
| [symptom] | [input / access / workflow / dependency / output] | [observable check] | [safe action or none] | [restricted action] | [none / possible / confirmed] | [stop condition] | [source] |

## Rules

- Phrase symptoms using language the user actually sees.
- Never diagnose a cause as certain unless evidence confirms it.
- State when retrying is unsafe or unknown.
- Keep credentials, connection changes, production edits, record deletion, and forced reruns out of the user guide.
- Include the identifier or evidence the user should collect before escalation.
