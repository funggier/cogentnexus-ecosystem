# Hybrid review usage guide

## Purpose

Run the same staged workflow with one AI or add an independent supervisor without changing unit contracts or artifacts. Reliability comes from controller-owned state, deterministic gates, restricted reviewer context, and recorded evidence.

## Recommended configuration

```json
{
  "schema_version": 1,
  "primary_executor": "ai-primary",
  "review_policy": "risk_based",
  "independent_reviewer": "ai-secondary",
  "fallback_to_single": true,
  "deterministic_gate_required": true,
  "independent_required_for": [
    "high_risk",
    "ambiguous_acceptance",
    "repeated_failure",
    "external_side_effect"
  ],
  "max_repairs_per_unit": 3
}
```

Set `independent_reviewer` to null when unavailable. Set `fallback_to_single` to false when true independence is mandatory.

## Single-AI operation

1. Controller issues one bounded contract to the Primary role.
2. Primary writes only the allowed candidate paths.
3. Controller runs deterministic validators against storage.
4. Start a fresh restricted context for the Reviewer role.
5. Reviewer receives only contract, criteria, artifact, hashes, and validator evidence.
6. Controller accepts PASS, routes FAIL to REPAIR, or records DISPUTED.
7. After repair, repeat the full leaf gate and only affected ancestor gates.

This is role separation, not independent-agent verification. Record `reviewer_mode: single`.

## Independent-review operation

1. Run Primary execution and deterministic validation exactly as above.
2. Send the independent reviewer a read-only review packet.
3. Confirm its returned artifact hashes still match storage.
4. Validate its verdict schema and criterion coverage.
5. Controller alone applies the decision policy.
6. Never let the independent reviewer edit artifacts or declare root success.

Record `reviewer_mode: independent` and a non-secret stable reviewer identity.

## Risk-based routing

Require independent review when any of these are true:

- the action is destructive, public, financial, credential-related, or externally visible;
- acceptance depends on interpretation rather than deterministic tests;
- the same symptom recurs after a repair;
- the unit changes controller, validator, security, or recovery behavior;
- policy or the user explicitly requires a second reviewer.

Otherwise use a fresh same-model review context or deterministic-only validation when the contract is fully machine-decidable.

## Review packet

```json
{
  "unit_id": "L-GREEN",
  "contract": {
    "objective": "Produce a green score record",
    "allowed_write_scope": ["parts/green.json"],
    "acceptance_criteria": [
      {"id": "C1", "rule": "exact keys are id and score"},
      {"id": "C2", "rule": "id is green and score is integer 80"}
    ]
  },
  "artifacts": [
    {
      "path": "parts/green.json",
      "sha256": "MEASURED_HASH"
    }
  ],
  "deterministic_evidence": {
    "result": "PASS",
    "validator": "validate_leaf",
    "inventory_result": "PASS"
  },
  "authority": "read_only"
}
```

Do not include executor reasoning, confidence, suggested verdict, or unsupported summaries.

## Reviewer response

```json
{
  "unit_id": "L-GREEN",
  "reviewer_mode": "independent",
  "reviewer_identity": "secondary-model",
  "artifact_hashes": {
    "parts/green.json": "MEASURED_HASH"
  },
  "verdict": "PASS",
  "findings": [],
  "criteria_covered": ["C1", "C2"],
  "authority_used": "read_only"
}
```

A FAIL finding should include `criterion_id`, `severity`, `evidence`, and `next_action`.

## Decision matrix

- Deterministic FAIL: REPAIR or FAILED.
- Deterministic PASS + reviewer PASS: PASS.
- Deterministic PASS + reviewer FAIL with evidence: REPAIR.
- Stale hash or malformed verdict: reject verdict and re-review.
- Reviewer conflict or ambiguous material finding: DISPUTED.
- Required independent reviewer unavailable: BLOCKED.
- Optional independent reviewer unavailable: recorded fallback to single review.

No AI may override a deterministic failure.

## Audit events

At minimum record:

- `candidate_created`
- `deterministic_gate_passed` or `deterministic_gate_failed`
- `review_requested`
- `review_fallback` when applicable
- `review_verdict_received`
- `dispute_opened` and `dispute_resolved`
- `repair_started` and `repair_completed`
- `integration_passed`
- `root_gate_passed`

Each event should include sequence, UTC timestamp, unit ID, artifact hashes, observed reviewer mode, and measured result where relevant.

## Migration from a single-role workflow

1. Keep existing artifacts and deterministic validators.
2. Move state transitions to a controller.
3. Change executor output from PASS to CANDIDATE.
4. Add reviewer policy and reviewer identity fields.
5. Add DISPUTED state and decision rules.
6. Add review packet/verdict schemas.
7. Test single, independent, fallback, stale-hash, deterministic-fail, and dispute paths.
8. Enable independent review first for high-risk units, then expand based on evidence.

## Minimal acceptance test

A conforming implementation must demonstrate:

- single mode completes and is labelled single;
- independent mode completes with a separate reviewer identity;
- required-independent mode blocks when the reviewer is unavailable;
- optional fallback is recorded rather than silent;
- deterministic failure cannot be overridden;
- stale reviewer hashes are rejected;
- disagreement produces DISPUTED;
- repair changes only allowed paths and preserves frozen sibling hashes;
- root SUCCESS is impossible with unresolved disputes.
