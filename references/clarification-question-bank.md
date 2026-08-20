# Clarification Question Bank

Use these patterns after analyzing available evidence. Ask only questions that resolve material gaps. Limit each batch to five questions.

For each question, state why the answer matters and provide a proposed assumption when safe.

## Scope and maturity

- Which application, package, flow, or environment is the documentation intended to cover?
- Is this implementation experimental, in testing, or production-supported?
- Does the existing documentation describe the current version or an earlier version?

## Purpose and audience

- What decision or task should the end user be able to complete?
- Which roles use the system, and which roles maintain it?
- Are there role-specific workflows that require separate instructions?

## Trigger and inputs

- What event starts the workflow in production?
- Which inputs are required, optional, or derived automatically?
- What should happen when an input is empty, invalid, delayed, or duplicated?

## Outputs and success

- What exact result confirms success for the user?
- Where is the output stored or delivered?
- Who receives notifications, and are failures communicated differently from successes?

## Permissions and ownership

- Is the connection owned by a service account or an individual?
- Which permissions or licenses are required for users and maintainers?
- Who owns monitoring, connector renewal, failed-run review, and escalation?

## Failure and recovery

- Is retrying safe, or can it create duplicates or repeat an external action?
- Which failures can an end user correct without administrator access?
- What evidence should be collected before escalation?
- Is there a documented rollback, cancellation, or manual recovery path?

## Environments and deployment

- Which path represents production?
- How are changes promoted between development, test, and production?
- Which settings differ by environment?
- What is the rollback or previous-version recovery process?

## Conflicts

- The implementation and existing guide describe different behavior. Which reflects the supported current state?
- Is the difference an accepted limitation, unfinished change, defect, or outdated documentation?
