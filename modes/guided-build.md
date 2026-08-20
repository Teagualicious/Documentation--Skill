# Guided Build Mode

Use this workflow when the project is low-code, no-code, process-heavy, described conversationally, or supplied through screenshots, diagrams, exports, run history, forms, and sample outputs rather than a conventional repository.

## Goal

Turn incomplete and heterogeneous project evidence into a structured workflow blueprint, ask only the clarification questions that materially improve the documentation, and produce synchronized builder/administrator and end-user guides.

## 1. Classify the platform and available evidence

Identify the project platform when possible. Read the relevant file under `references/platform-profiles/`.

Possible inputs include:

- Platform export packages
- Workflow definitions
- Screenshots
- Diagrams
- Run-history CSV files
- Screen-recording transcripts
- Forms and field lists
- Sample input and output files
- Error messages
- Existing SOPs
- User descriptions

Prefer structured exports and run evidence over screenshots and memory-based descriptions.

## 2. Build a workflow blueprint

Capture:

- Purpose and business problem
- Intended users and maintainers
- Trigger
- Preconditions
- Inputs and source systems
- Ordered actions
- Conditions and branches
- Loops and parallel paths
- Calculations and transformations
- Approvals and human decisions
- Connections and permissions
- Outputs and destinations
- Success state
- Failure states
- Retry and duplicate behavior
- Monitoring and support ownership
- Environments, deployment, and change control

Mark each item confirmed, inferred, unknown, or conflicting.

## 3. Use adaptive clarification

Do not ask every question in the question bank. Fill the blueprint from supplied evidence first.

Ask only about unresolved facts that change:

- User instructions
- Access or prerequisites
- Security or permissions
- Inputs and outputs
- Branch behavior
- Error recovery
- Ownership or escalation
- Environment promotion
- Destructive or duplicate-producing actions

Use batches of no more than five questions. Offer a proposed assumption when safe.

## 4. Handle description-only projects

When no export or technical artifact exists:

1. Capture the happy path from trigger to output.
2. Ask for one real or synthetic example.
3. Identify every system touched.
4. Identify owners and user roles.
5. Ask what happens when each major dependency is missing, empty, delayed, duplicated, or unavailable.
6. Preserve technical implementation details as unknown when the user cannot verify them.

Do not make a prose description look technically verified.

## 5. Separate user and administrator actions

Classify recovery actions as:

- Safe for end users
- Safe for trained operators
- Administrator-only
- Destructive or approval-required

Only the first category belongs in the user guide by default. Operator or administrator actions belong in the developer/administrator guide and must include prerequisites and risks.

## 6. Generate both guides

For low-code projects, title `DEVELOPER_GUIDE.md` as **Builder and Administrator Guide** inside the document.

The administrator guide should explain connectors, ownership, environments, permissions, actions, branches, error handling, deployment, monitoring, and maintenance.

The user guide should explain how to start or use the workflow, what information to supply, what success looks like, what the user can safely retry or correct, and what evidence to collect before escalation.

## 7. Validate

Check that:

- Every named action, field, connection, form, table, list, file, and output is supported or labeled.
- The user guide does not expose credentials or administrative configuration.
- Retry instructions do not create duplicates or repeat destructive actions.
- Ownership and escalation are not invented.
- Unknown implementation details remain visible.
