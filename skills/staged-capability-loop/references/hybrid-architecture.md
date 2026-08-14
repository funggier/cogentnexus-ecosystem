# Hybrid staged-review architecture

## Design goal

Use one durable workflow and one artifact contract whether execution uses a single AI, an independent reviewer, or risk-based routing. Changing reviewer availability must not change unit IDs, acceptance criteria, validator behavior, audit format, or root completion rules.

## Components

```text
User / Policy
      |
      v
+-----------------------+
| Workflow Controller   |
| state, policy, audit  |
+----+-------------+----+
     |             |
     v             v
+----------+   +----------------------+
| Primary  |   | Deterministic Gates  |
| AI       |   | schema/tests/hash    |
+----+-----+   +----------+-----------+
     |                    |
     v                    |
  CANDIDATE --------------+
                          |
                          v
                +--------------------+
                | Reviewer Router    |
                +-----+---------+----+
                      |         |
                single mode  independent mode
                      |         |
                      v         v
                Fresh same-AI  Secondary AI
                review context read-only review
                      |         |
                      +----+----+
                           v
                  Structured Verdict
                           |
                           v
                 Controller Decision
                   |       |       |
                  PASS   REPAIR  DISPUTED
                   |               |
                   v               v
               Integrator     clarify/check/
                   |          re-review/human
                   v
                Root Gate
                   |
                   v
                 Report
```

The controller is the only component allowed to change workflow state. AI outputs are proposals or verdicts, never authoritative state transitions.

## Responsibility boundaries

### Workflow Controller

- selects the exact READY unit;
- issues bounded contracts;
- records requested and observed reviewer modes;
- runs policy and schema checks;
- enforces retry limits and allowed paths;
- validates artifact and verdict hashes;
- opens and resolves disputes;
- emits append-only audit events;
- decides whether integration and external side effects are allowed.

Prefer deterministic implementation. If an AI assists controller planning, deterministic code must still enforce transitions and gates.

### Primary AI

- performs planning and execution for one unit;
- writes only within the allowed scope;
- diagnoses failures and proposes repairs;
- produces CANDIDATE artifacts;
- never validates its own candidate authoritatively;
- never declares root success.

### Deterministic Validator

- reads artifacts from storage after execution;
- checks machine-decidable criteria;
- emits measured evidence;
- has veto authority: FAIL cannot be overridden by any AI;
- does not judge subjective or semantic quality unless encoded as a deterministic rule.

### Reviewer Router

- applies `single`, `independent`, `risk_based`, or `deterministic_only` policy;
- builds the restricted review packet;
- records fallback or blocks when independence is mandatory;
- does not modify artifacts or verdict content.

### Semantic Reviewer

- reads only the contract, criteria, artifact, hashes, and deterministic evidence;
- returns PASS, FAIL, or DISPUTED in a validated schema;
- is read-only;
- does not integrate, repair, perform external side effects, or transition state.

### Integrator and Root Gate

- consume only PASS children;
- recheck stored child hashes and interfaces;
- build the parent artifact;
- confirm root acceptance and exact inventory;
- reject unresolved disputes and missing mandatory reviews.

## Trust boundaries

```text
Untrusted:
  Primary AI prose
  Candidate artifact
  Reviewer prose without schema
  Claimed hashes or claimed command results

Conditionally trusted after validation:
  Parsed reviewer verdict with current artifact hashes
  Controller checkpoint with schema and round-trip validation

Authoritative measured evidence:
  Filesystem reads
  Deterministic validator output
  Calculated hashes
  Exact inventory
  Exit codes and captured test results
```

No component should trust another component's statement that a command ran or an artifact exists. Read and measure the target state.

## State machine

```text
PENDING
  -> READY
  -> RUNNING
  -> CANDIDATE
       -> deterministic FAIL -> REPAIR -> RUNNING
       -> deterministic PASS -> REVIEWING
            -> reviewer PASS -> PASS
            -> reviewer FAIL -> REPAIR
            -> ambiguity/conflict -> DISPUTED
                 -> clarified/rechecked -> REVIEWING
                 -> authority missing -> BLOCKED
                 -> unrecoverable -> FAILED
PASS children
  -> INTEGRATING
  -> INTEGRATION_VERIFY
       -> PASS parent
       -> REPAIR parent/affected leaf
Root PASS
  -> REPORT
```

`REVIEWING` and `INTEGRATING` may be stored explicitly or represented as events, but CANDIDATE, PASS, REPAIR, DISPUTED, BLOCKED, and FAILED must remain distinguishable.

## Control flow by mode

### Single mode

```text
Primary context -> artifact -> deterministic gate
-> fresh restricted same-model context -> verdict
-> controller decision
```

This provides role and context separation, not independent-agent verification.

### Independent mode

```text
Primary AI -> artifact -> deterministic gate
-> separate reviewer identity/session/model -> verdict
-> hash and schema validation -> controller decision
```

Independence requires separate execution context and truthful identity recording. A second role in the same context is not independent.

### Risk-based mode

```text
classify unit risk
  low + machine-decidable -> deterministic_only or single
  semantic/medium         -> single, optionally independent
  high/repeated/external  -> independent required
```

If an optional reviewer is unavailable, record fallback. If required independence is unavailable, transition to BLOCKED.

## Suggested file layout

```text
workflow/
  config/
    review-policy.json
  contracts/
    <unit-id>.json
  candidates/
    <unit-id>/
  evidence/
    deterministic/
    reviews/
    repairs/
  checkpoints/
    <unit-id>.json
  integration/
  events.jsonl
  manifest.json
```

- `review-policy.json`: routing rules, fallback policy, repair limits.
- `contracts/`: immutable acceptance criteria and allowed scope per unit version.
- `candidates/`: executor outputs; untrusted until gated.
- `evidence/deterministic/`: validator outputs and measured hashes.
- `evidence/reviews/`: review packets and verdicts.
- `evidence/repairs/`: before/after hashes and exact changed sets.
- `checkpoints/`: accepted artifacts, evidence references, and next state.
- `events.jsonl`: append-only lifecycle audit.
- `manifest.json`: current recoverable workflow state.

For small workflows, these may be consolidated, but preserve the same logical boundaries and evidence fields.

## Core records

### Manifest

Must identify workflow version, current state, exact next READY unit, review policy, unresolved disputes, and terminal status.

### Unit contract

Must identify inputs, outputs, allowed writes, dependencies, criteria IDs, deterministic validator, reviewer requirement, integration interface, and retry limit.

### Review evidence

Must bind the verdict to artifact hashes and criteria. Stale hashes invalidate the verdict.

### Repair evidence

Must record before/after hashes, allowed and actual changed sets, frozen sibling hashes, attempt number, and validation result.

### Audit event

Must include sequence, UTC timestamp, event type, unit ID, state transition, reviewer mode when applicable, artifact hashes, and measured result.

## Failure and dispute paths

- Deterministic defect: smallest affected unit enters REPAIR.
- Semantic defect with evidence: route finding to REPAIR.
- Malformed or stale verdict: reject it and request a fresh review.
- Primary/reviewer conflict: controller opens DISPUTED; neither party wins automatically.
- Ambiguous criterion: clarify and version the contract, invalidate affected review evidence, then re-review.
- Repeated failure: change executor, strategy, unit size, or validator.
- Required reviewer unavailable: BLOCKED, never silent fallback.
- External side-effect gate unresolved: preserve candidate; do not perform the side effect.

## Security and isolation

- Reviewer access is read-only by default.
- Give each executor the smallest writable path set.
- Keep secrets out of review packets unless strictly necessary.
- Use non-secret stable reviewer identities.
- Bind verdicts to calculated artifact hashes.
- Fence duplicate workers and use idempotency keys for retryable external operations.
- Require explicit authorization for destructive or public actions.

## Extension points

The architecture permits:

- same model in a fresh context;
- another model from the same provider;
- a separate agent or session;
- a human reviewer;
- multiple reviewers with quorum policy;
- domain-specific deterministic validators.

All extensions must return the same review verdict contract, allowing the controller and workflow artifacts to remain unchanged.

## Implementation acceptance

Before deployment, test:

1. single mode labelled truthfully;
2. independent mode with distinct identity;
3. optional fallback recorded;
4. mandatory-independent unavailability blocks;
5. deterministic FAIL cannot be overridden;
6. stale review hashes are rejected;
7. disagreement opens DISPUTED;
8. resolution closes the dispute with new evidence;
9. repair modifies only allowed paths;
10. root SUCCESS is impossible with missing gates or unresolved disputes.
