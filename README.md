# CogentNexus Ecosystem

CogentNexus Ecosystem connects the **durable Host/continuity layer** with the **request-lane and staged verification policy** used inside OpenClaw.

The clean baseline separates responsibilities so simple conversation stays simple while interruption-prone or consequential work can escalate into durable verified execution.

## Projects

- [CogentNexus Core](https://github.com/funggier/cogentnexus) — external Host Controller, Ticket-first continuity, lifecycle/policy ownership, deterministic recovery, durable workflows, evidence, and terminal delivery support.
- [Staged Capability Loop](skills/staged-capability-loop/) — DIRECT / LOOKUP / ACTION / STAGED admission plus review/verification policy for complex work.

```text
User / Channel
      |
      v
CogentNexus Host Controller
  durable Ticket + lifecycle/recovery
      |
      v
OpenClaw
      |
      v
Request lane admission
  DIRECT
  LOOKUP
  ACTION
  STAGED -> CogentNexus durable workflow machinery
```

## Responsibility boundary

- **Host continuity** answers: how do we make sure accepted work does not disappear?
- **Lane policy** answers: how much machinery does this request actually need?
- **Durable workflow runtime** answers: how do we checkpoint, verify, recover, and finish STAGED work?

Ticket-first continuity does **not** mean every request becomes STAGED. A greeting may be durably accepted and still receive a normal DIRECT response.

## Operating modes

CogentNexus Core defines Host ownership modes:

- **MANAGED** — CogentNexus owns Ticket-first continuity and managed lifecycle/recovery behavior.
- **PASSTHROUGH** — CogentNexus relinquishes interception/background ownership; OpenClaw behaves normally.
- **MAINTENANCE** — intentional stop; recovery does not fight operator intent.

The ecosystem policy is active only in managed operation. Native OpenClaw must remain available when CogentNexus is disabled.

## Durable policy registration

Ecosystem v0.2 registers its combined managed policy with the Core Host instead of merely overwriting `AGENTS.md`.

The Host stores the selected snapshot under:

```text
.cogent/host/managed-policy.md
```

This means:

- `cnx disable` removes the active managed block but preserves the selected Ecosystem policy;
- `cnx enable` automatically restores the same Ecosystem policy;
- Core updates preserve the registered companion policy;
- `cnx policy reset` explicitly returns to the Core-only default.

## Installation

1. Install a compatible CogentNexus Core release.
2. Verify `cnx status` is healthy.
3. Download/clone this ecosystem release.
4. Install the companion into the same OpenClaw workspace.

```powershell
python .\scripts\install.py --workspace "$HOME\.openclaw\workspace"
```

The installer copies `staged-capability-loop`, validates required files, backs up the previous installed companion, and registers `templates/AGENTS.ecosystem.md` durably through the Core Host.

Detailed Thai guide: [docs/INSTALL.th.md](docs/INSTALL.th.md)

## Request lanes

- **DIRECT** — greetings, conversation, explanation, advice, brainstorming, and short drafting.
- **LOOKUP** — focused read-only retrieval using the minimum necessary tools.
- **ACTION** — bounded reversible execution with proportionate verification.
- **STAGED** — complex, consequential, long-running, interruption-prone, dependency-heavy, externally mutating, repeatedly failing, or independently reviewed work.

Always choose the **lightest reliable lane**. Do not load CogentNexus durable workflow machinery merely to decide that a request is DIRECT.

## Reliability model

- DIRECT: durable acceptance can exist without staged overhead.
- LOOKUP/ACTION: bounded tool use and proportionate verification.
- STAGED: durable controller state, checkpoints, deterministic gates, bounded repair, reviewer policy, integration verification, and terminal evidence.

Across MANAGED operation, the continuity invariant remains: a durably accepted request must not silently disappear; it must become delivered/completed, cancelled, or explicitly failed with evidence.

## Compatibility

See [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md). Only combinations exercised together are listed as tested.

## License

MIT
