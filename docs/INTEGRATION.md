# CogentNexus Ecosystem integration

## Responsibility boundary

The ecosystem is intentionally split into layers with different responsibilities:

- **OpenClaw** hosts conversations, skills, plugins, tools, channels, and sessions.
- **CogentNexus Host Controller** sits outside model inference and owns managed continuity: durable Ticket intake, desired runtime state, lifecycle reconciliation, deterministic recovery supervision, cancellation, and session fencing.
- **CogentNexus durable runtime** handles checkpointed workflows, evidence, recovery, durable context handoff, and terminal delivery for work that actually needs those mechanisms.
- **Staged Capability Loop** selects the lightest reliable request lane and defines staged review/verification behavior when complexity or risk justifies it.

These layers must not be collapsed into one mandatory heavy workflow.

A managed greeting may be durably accepted by the Host and still remain DIRECT. Conversely, a complex or interruption-prone request may escalate into the durable workflow machinery after admission.

## Control and authority order

For managed requests, use this conceptual order:

1. Higher-priority safety, authorization, and platform constraints.
2. User intent and requested outcome.
3. Host continuity state: preserve accepted message/session identity and avoid duplicate execution.
4. Request-lane admission: DIRECT, LOOKUP, ACTION, or STAGED.
5. Durable workflow controller only when the selected lane requires it.
6. Executors, tools, deterministic validators, and reviewers within their bounded authority.
7. Terminal evidence before claiming consequential completion.

The Host Controller protects continuity; it does not decide that every request deserves staged execution.

## Operating modes

CogentNexus Core supports three host-level semantics:

- **MANAGED** — CogentNexus owns Ticket-first continuity and managed runtime lifecycle/recovery behavior.
- **PASSTHROUGH** — CogentNexus relinquishes interception and background ownership; OpenClaw behaves normally.
- **MAINTENANCE** — intentional stop state; durable state remains but automatic recovery must not restart the runtime against operator intent.

`disable` means PASSTHROUGH and is intentionally different from `stop`, which means MAINTENANCE.

OpenClaw must remain usable without CogentNexus. CogentNexus must also be able to retain durable control state without depending on a live OpenClaw inference process.

## Activation

The ecosystem installer manages one bounded section of workspace `AGENTS.md` between:

```text
<!-- cogentnexus:begin -->
<!-- cogentnexus:end -->
```

It preserves all content outside those markers, creates a backup before changing an existing file, and updates the same block idempotently.

Installing CogentNexus Core establishes the Host-managed continuity policy and runtime integration. Installing this ecosystem companion afterward extends the managed block with the staged request-lane policy.

PASSTHROUGH mode removes/disables the managed interception policy so native OpenClaw behavior is restored without uninstalling the software or deleting durable state.

## Request lifecycle

A normal managed message follows this conceptual path:

```text
message received
  -> durable Ticket committed
  -> request lane selected
     -> DIRECT: answer naturally
     -> LOOKUP: perform minimal retrieval
     -> ACTION: execute bounded work + proportionate verification
     -> STAGED: enter durable verified workflow
  -> durable/normal response delivery
  -> terminal state
```

If the Gateway is interrupted after Ticket commit, the Host Controller can reconcile the runtime and recover eligible non-terminal work. Recovery must respect cancellation, generation fencing, leases, idempotency, and external-side-effect boundaries.

## Recovery invariant

Once an eligible user message is durably accepted, it must not silently disappear. It must eventually reach an explicit terminal outcome:

- delivered/completed;
- cancelled; or
- failed with recorded evidence/reason.

This invariant applies to continuity, not to workflow heaviness.

## Recommended installation order

1. Install CogentNexus Core / Host Controller.
2. Install CogentNexus Ecosystem companion skills.
3. Start a fresh OpenClaw session so skill metadata and workspace instructions reload.
4. Verify MANAGED mode and Ticket-first state.
5. Verify a greeting stays DIRECT.
6. Verify a consequential multi-step task selects STAGED.
7. Verify `cnx disable` returns OpenClaw to PASSTHROUGH/native behavior.

## Compatibility

Use only version combinations listed in [COMPATIBILITY.md](COMPATIBILITY.md) as tested together. Host Controller features require a CogentNexus Core release that includes the managed-host architecture.
