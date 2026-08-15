# CogentNexus Ecosystem integration

This document defines the clean integration boundary for Ecosystem v0.2+ with CogentNexus Core v0.8+.

## Responsibility boundary

- **OpenClaw** hosts channels, conversations, sessions, skills, plugins, and tools.
- **CogentNexus Host Controller** runs outside model inference and owns managed continuity: durable Ticket intake, desired runtime state, selected managed policy, lifecycle reconciliation, deterministic recovery supervision, cancellation, and session fencing.
- **CogentNexus durable runtime** owns checkpointed workflows, controller state, evidence, recovery, context handoff, and terminal delivery for work that actually needs those mechanisms.
- **Staged Capability Loop** chooses DIRECT / LOOKUP / ACTION / STAGED and defines staged review/verification behavior.

These layers must not be collapsed into one mandatory heavy workflow.

## Control order

For MANAGED requests:

1. higher-priority safety, authorization, and platform constraints;
2. user intent and requested outcome;
3. already-committed Host/Ticket continuity state;
4. choose the lightest reliable request lane;
5. load CogentNexus durable workflow machinery only if STAGED/recovery requires it;
6. executor/tools/validators/reviewers act only within bounded authority;
7. terminal evidence governs consequential completion claims.

The Host protects continuity. It does not make every request STAGED.

## Request lifecycle

```text
message received
  -> durable Ticket committed by managed bridge
  -> lane selected
     -> DIRECT: answer naturally
     -> LOOKUP: minimal read-only retrieval
     -> ACTION: bounded execution + verification
     -> STAGED: durable verified workflow
  -> response/outbox delivery
  -> terminal state
```

A greeting is the canonical lightweight test: it should remain DIRECT even when its message has a durable Ticket.

## Operating modes

Core Host modes:

- **MANAGED** — Ticket-first continuity and managed lifecycle/recovery are active.
- **PASSTHROUGH** — CogentNexus interception/background ownership are disabled; native OpenClaw works normally.
- **MAINTENANCE** — deliberate managed stop; supervisor does not restart against operator intent.

`disable` means PASSTHROUGH and is intentionally different from `stop`, which means MAINTENANCE.

## Managed policy ownership

The Core Host owns the currently selected managed policy as durable state:

```text
.cogent/host/managed-policy.md
```

The Ecosystem installer registers `templates/AGENTS.ecosystem.md` through the Host `policy register` command. The Host then applies that registered policy inside the bounded `AGENTS.md` block:

```text
<!-- cogentnexus:begin -->
...
<!-- cogentnexus:end -->
```

Existing user content outside those markers is preserved.

This ownership model is important:

- installing Ecosystem replaces the selected Core-only policy with the combined continuity + four-lane policy;
- `cnx disable` removes the active managed block but preserves the selected Ecosystem snapshot;
- `cnx enable` restores the same Ecosystem policy automatically;
- Core upgrades preserve the registered companion policy instead of silently reverting it;
- `cnx policy reset` is the explicit way to return to the Core-only policy.

The combined policy must never reintroduce the bootstrap inversion where `cogentnexus` is loaded before deciding whether the request is DIRECT.

## Recovery invariant

Once an eligible message is durably accepted, it must not silently disappear. It must become one of:

- delivered/completed;
- cancelled; or
- explicitly failed with recorded evidence/reason.

This is a continuity rule, not a workflow-depth rule.

## Recommended installation order

1. Install a compatible CogentNexus Core/Host release.
2. Verify `cnx status` reports MANAGED and Gateway health.
3. Install the Ecosystem companion into the same workspace; confirm `cnx policy status` reports a registered snapshot.
4. Start a fresh OpenClaw session so skill/workspace metadata reload.
5. Verify a greeting stays DIRECT.
6. Verify a consequential multi-step task selects STAGED.
7. Verify `cnx disable` returns OpenClaw to native PASSTHROUGH behavior.
8. Verify `cnx enable` restores the Ecosystem managed policy without reinstalling it.

## Compatibility

See [COMPATIBILITY.md](COMPATIBILITY.md). Only combinations exercised together are called tested.
