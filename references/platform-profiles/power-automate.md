# Microsoft Power Automate Profile

Use this profile for cloud flows, desktop flows, solution-aware flows, or workflows that rely on Power Platform connectors.

## Preferred evidence order

1. Solution export
2. Non-solution flow package export
3. Run-history CSV or detailed run evidence
4. Screenshots of trigger, actions, conditions, expressions, and settings
5. Existing documentation
6. User description

Record which environment and export type each artifact represents.

## Inspect or ask about

### Identity and ownership

- Flow owner
- Co-owners
- Service account versus personal connection
- Connection references
- Required Power Platform, Microsoft 365, or premium licenses

### Trigger

- Trigger type
- Recurrence, event, or manual input
- Trigger conditions
- Concurrency settings
- Environment-specific source identifiers

### Actions and control flow

- Action display names and connector types
- Conditions and switch branches
- Apply-to-each loops
- Do-until loops
- Parallel branches
- Scopes and run-after configuration
- Expressions and transformations
- Child flows
- Approvals

### Data and outputs

- SharePoint sites and lists
- Dataverse tables
- Excel workbooks and tables
- Forms
- Email mailboxes
- Teams channels
- APIs and custom connectors
- Files created or updated
- Notifications and approval results

### Reliability

- Retry policies
- Timeouts
- Pagination
- Concurrency
- Duplicate prevention
- Partial completion
- Terminate actions
- Failure notification
- Safe rerun behavior

### Operations

- Development, test, and production environments
- Solution and environment-variable usage
- Import and connection rebinding
- Monitoring and failed-run ownership
- Connector expiration or ownership transfer
- Versioning and rollback

## Documentation safety

Document connection-reference and environment-variable names, but never secret values, tokens, passwords, or full connection strings.

Do not tell end users to resubmit or rerun a flow until duplicate and external-action behavior is known.

## User-guide emphasis

Explain:

- How the user triggers or supplies input
- Required fields and file formats
- What confirmation appears
- Where output or approval status appears
- Which correction and retry actions are safe
- What run information to collect before escalation
