# Hybrid Analysis Mode

Use this mode when one solution spans conventional code, low-code workflows, external platforms, data stores, dashboards, files, and human actions.

## Goal

Document the complete operating chain while preserving the evidence and ownership boundaries of each component.

## 1. Create a system boundary map

List every material component and classify it as:

- Software application or service
- Scheduled or event-driven job
- Low-code workflow
- Data store
- File or spreadsheet
- External API or platform
- Dashboard or report
- Manual review or approval
- Notification or downstream system

Record the owner, environment, input, output, and evidence source for each component.

## 2. Apply the supporting modes

Use `repository-analysis.md` for code components and `guided-build.md` for low-code, manual, or artifact-driven components.

Do not force every component into one evidence type. Preserve repository references, export references, screenshots, run history, and stakeholder answers separately.

## 3. Document boundaries explicitly

For every connection between components, capture:

- Producer
- Consumer
- Trigger or transfer mechanism
- Data contract or file format
- Authentication or permission model
- Expected timing
- Retry behavior
- Duplicate handling
- Failure owner
- Evidence source

A boundary without an owner or failure path should become an open question.

## 4. Trace end-to-end workflows

Show the complete path, for example:

```text
Web application
    ↓ API or file output
Data store
    ↓ event or schedule
Low-code workflow
    ↓ approval request
Human reviewer
    ↓ decision
Notification and downstream update
```

Document current behavior and intended behavior separately when components are out of sync.

## 5. Generate role-aware documents

The developer guide should cover the full chain, component boundaries, interfaces, credentials ownership, environment promotion, monitoring, and cross-system recovery.

The user guide should include only the portions relevant to the user's role. Do not expose backend or administrator actions merely because they exist elsewhere in the workflow.

## 6. Validate cross-system consistency

Check:

- Names and identifiers match at each boundary.
- Upstream outputs satisfy downstream input requirements.
- Timing and retry assumptions do not conflict.
- Failure ownership is defined.
- User recovery cannot create duplicate downstream work.
- Secret values and private data are excluded.
