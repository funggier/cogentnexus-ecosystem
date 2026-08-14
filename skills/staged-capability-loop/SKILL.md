---
name: "staged-capability-loop"
description: "Conversation, questions, advice, lookup, bounded actions, and staged verified work."
---

# Staged Capability Loop

Choose the lightest reliable lane. Handle ordinary conversation directly; use staged, recoverable execution only when the work benefits from decomposition, durable evidence, or independent review.

## Admission and fast path

Classify each request before entering the staged state machine:

- **DIRECT:** greetings, casual conversation, simple questions, explanations, advice, brainstorming, short drafting, clarification, and other low-risk work that can be answered from current context. Respond immediately and naturally. Do not create contracts, checkpoints, reviewers, files, plans, or tool calls unless the request actually needs them.
- **LOOKUP:** focused information retrieval or a small read-only check. Use only the minimum necessary source or tool, verify the relevant fact, and answer. Do not decompose into staged units merely because a tool is involved.
- **ACTION:** a bounded, reversible task with clear scope. Execute directly, verify in proportion to risk, and report the outcome without constructing the full staged workflow.
- **STAGED:** multi-step, consequential, long-running, interruption-prone, ambiguous, dependency-heavy, externally mutating, repeatedly failing, or independently reviewed work. Use the full workflow below.

Prefer DIRECT when a request is only conversational. A greeting such as “สวัสดีครับ” should receive a normal greeting, not a workflow announcement. A request for an opinion or consultation should remain conversational unless it requires current external facts, consequential action, or durable work.

Escalate from DIRECT, LOOKUP, or ACTION to STAGED only when observed complexity or risk justifies it. Never escalate merely to demonstrate process. If scope expands during the turn, preserve completed work and enter STAGED at the smallest necessary boundary.

For DIRECT responses:

- answer in the same turn and match the user’s tone;
- keep process internal and omit workflow terminology;
- do not load staged references;
- ask a clarifying question only when a missing choice materially changes the answer;
- finish once the user’s conversational need is met.

For role routing, reviewer policy, verdict schemas, and operational examples in STAGED work, read [hybrid-review-guide.md](references/hybrid-review-guide.md). For components, trust boundaries, state flow, and file layout, read [hybrid-architecture.md](references/hybrid-architecture.md).

## Staged workflow

Only the STAGED lane uses the full sequence:

ASSESS → DECOMPOSE → PLAN → REQUIRE → DISCOVER → SUBSTITUTE → RECHECK → REMEDIATE → EXECUTE → VERIFY → REPAIR → CHECKPOINT → INTEGRATE → INTEGRATION_VERIFY → REPORT.

Decompose work into bounded replaceable units. Execute one ready leaf at a time, accept only verified artifacts, integrate bottom-up, and preserve evidence for recovery.

Executor output is always CANDIDATE. Only the workflow controller may advance it to PASS after required gates succeed.

## Unit contract

Record for each stable unit ID:

- objective, parent, children, dependencies, inputs, and exact outputs;
- allowed write scope and external side effects;
- executor, deterministic validator, reviewer policy, and reviewer identity;
- integration interface and retry count;
- status: PENDING, READY, RUNNING, CANDIDATE, PASS, REPAIR, DISPUTED, BLOCKED, or FAILED;
- artifact hashes, measured evidence, and exact next READY leaf.

A leaf becomes READY only when dependencies are PASS and required capabilities are resolved. Re-read and validate serialized manifests after updates.

## Hybrid role model

Use one workflow contract in every STAGED mode:

- Controller: owns state transitions, scope enforcement, retries, and audit events. Prefer deterministic code, not an AI role.
- Primary AI: plans, executes, diagnoses, repairs, and integrates within the current unit contract.
- Deterministic validator: checks schema, types, hashes, tests, inventory, exit codes, and other measurable facts. Its failure cannot be overridden by AI.
- Reviewer: evaluates semantic correctness and contract fit. It may be the primary model in a fresh restricted context or an independent model/session.
- Reporter: summarizes only terminal controller evidence.

Select reviewer mode per unit:

- `single`: same model, fresh reviewer context;
- `independent`: separate model or isolated agent/session;
- `risk_based`: independent for high-risk, ambiguous, repeated-failure, or external-side-effect units; otherwise single;
- `deterministic_only`: only when acceptance is completely machine-decidable.

Record the observed reviewer mode and identity. Never claim independent review when the same model or context performed it.

## Context and authority separation

Give the reviewer only the unit contract, acceptance criteria, stored artifact, and deterministic evidence. Withhold executor reasoning, confidence, and claimed status unless required to reproduce a defect.

Reviewers are read-only by default. They return structured findings; they do not repair, integrate, mutate PASS siblings, or declare root success. The controller routes accepted findings to REPAIR.

When independent review is unavailable:

- continue only if policy permits fallback;
- record `requested_mode`, `observed_mode`, and `fallback_reason`;
- never silently downgrade a unit whose policy requires independence;
- mark BLOCKED if independence is mandatory.

## Deterministic VERIFY

Before semantic review, independently inspect storage and enforce:

- existence, non-emptiness, UTF-8, parse/schema, exact keys, and typed values;
- expected artifact count, allowed-path scan, and side-effect inventory;
- hashes of current artifacts and frozen PASS siblings;
- unit tests or exact comparisons where available;
- exit code and measured output.

A process success or executor statement does not prove PASS. Capture intentional negative-test failures before repair.

## Reviewer verdict

Require a machine-readable verdict with:

- `unit_id`, `reviewer_mode`, `reviewer_identity`, and `artifact_hashes`;
- `verdict`: PASS, FAIL, or DISPUTED;
- findings with criterion ID, severity, evidence, and suggested next action;
- acknowledgement that the reviewer had read-only authority.

Reject malformed verdicts, stale artifact hashes, missing criterion coverage, invented evidence, and prose-only claims.

Decision rules:

- deterministic gate FAIL → REPAIR or FAILED; no AI override;
- deterministic gate PASS plus reviewer PASS → PASS;
- reviewer FAIL with evidence → REPAIR;
- conflicting reviewers, ambiguous evidence, or unresolved material finding → DISPUTED;
- DISPUTED → add a deterministic check, clarify the contract, request another independent review, or escalate to a human;
- external side effects occur only after required preflight review and authorization.

## Repair isolation

On failure, mark the smallest unit REPAIR and preserve the candidate. Freeze PASS sibling hashes, classify the defect, modify only allowed paths, rerun the full leaf validator, and rerun affected ancestor checks.

Allow at most three bounded repair attempts. Never make a third materially identical attempt. Change strategy, executor, unit size, or contract after repeated symptoms.

## Checkpoint and audit

After PASS preserve:

- artifact hashes and exact inventory;
- deterministic validator command/result;
- requested and observed reviewer modes;
- reviewer verdict and covered criteria;
- failures, repair strategy, changed-file set, and unchanged sibling hashes;
- affected parent and exact next READY leaf.

Emit append-only events for candidate creation, gate results, review requests/verdicts, fallback, disputes, repair, integration, and root completion. Revalidate each serialized checkpoint.

## Integration and completion

Integrate only PASS children at their nearest parent. Verify child hashes, interfaces, ordering, parent assembly, smoke tests, acceptance criteria, and exact side-effect inventory.

SUCCESS requires every required leaf and parent gate to PASS, mandatory independent reviews to be present, checkpoints to remain unchanged, root acceptance to PASS, and no unresolved placeholders or disputes. Otherwise report PARTIAL, FAILED, BLOCKED, or DISPUTED truthfully.

## Report

For DIRECT, LOOKUP, and ACTION, respond naturally with only the detail the user needs.

For STAGED work, return two to six concise lines: Status, Completed, Verified, and Remaining when applicable. Name the actual review mode; do not imply independence that did not occur.

