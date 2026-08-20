# [Project Name] — Developer Guide

> For low-code projects, replace the displayed title with **[Project Name] — Builder and Administrator Guide**.

## Document control

| Field | Value |
|---|---|
| Documented scope | [scope] |
| Source type | [repository / export / hybrid / description] |
| Source locator | [repository, path, export, or artifact] |
| Source revision | [commit, branch, export version, or unknown] |
| Environment | [development / test / production / mixed / unknown] |
| Last verified | [date] |
| Documentation status | [complete for scope / partial / blocked] |

## 1. Project overview

### Purpose

[What problem the project solves.]

### Primary users and owners

[Users, maintainers, administrators, and support owners.]

### Current maturity

[Experimental, testing, production-supported, deprecated, or unknown.]

## 2. Scope and system context

### In scope

- [component or workflow]

### Out of scope

- [explicit boundary]

### External systems and actors

[Describe upstream, downstream, and human boundaries.]

## 3. Architecture

### High-level diagram

[Use the architecture diagram template.]

### Components

| Component | Type | Responsibility | Inputs | Outputs | Owner | Evidence state |
|---|---|---|---|---|---|---|
| [name] | [type] | [purpose] | [inputs] | [outputs] | [owner or unknown] | [confirmed/inferred/etc.] |

### Design decisions and constraints

[Confirmed decisions, tradeoffs, and limitations.]

## 4. Workflow and data flow

### [Workflow name]

- **Actor:** [actor]
- **Trigger:** [trigger]
- **Preconditions:** [preconditions]
- **Success state:** [success]

[Ordered workflow and decision branches.]

### Failure and recovery

[Failure states, retries, duplicate risk, rollback, and escalation.]

## 5. Setup and configuration

### Prerequisites

- [requirement]

### Installation, import, or environment setup

[Exact confirmed procedure.]

### Configuration

| Name | Purpose | Required | Environment-specific | Secret | Owner |
|---|---|---:|---:|---:|---|
| [name] | [purpose] | [yes/no] | [yes/no] | [yes/no] | [owner] |

Never include secret values.

## 6. Interfaces and data contracts

[APIs, functions, events, actions, files, tables, lists, schemas, and input/output contracts.]

## 7. Security and permissions

[Authentication, authorization, data handling, credential ownership, retention, and security assumptions.]

## 8. Testing and validation

[Existing tests, manual validation, test data, expected results, and known gaps.]

## 9. Deployment and release

[Build, deployment/import, environment promotion, release verification, versioning, and rollback.]

## 10. Monitoring and troubleshooting

[Logs, run history, alerts, diagnostics, common failures, recovery, and escalation.]

## 11. Maintenance and change impact

[Common modifications, dependency updates, ownership, technical debt, and sections affected by likely changes.]

## 12. Evidence and unresolved items

### Assumptions and inferences

- [item]

### Conflicts

- [item]

### Unknowns

- [item]

### Analysis limitations

- [unread files, unavailable exports, unsupported formats, or scope exclusions]
