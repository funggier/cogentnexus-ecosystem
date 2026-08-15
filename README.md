# CogentNexus Ecosystem

The official project hub for CogentNexus components built around OpenClaw.

The ecosystem separates **durable continuity** from **execution depth** so everyday conversation can stay lightweight while complex or interruption-prone work gains checkpoints, recovery, review, and evidence when needed.

## Projects

- [CogentNexus Core](https://github.com/funggier/cogentnexus) — external Host Controller, Ticket-first continuity, runtime lifecycle ownership, deterministic recovery, durable workflows, evidence, and terminal delivery support.
- [Staged Capability Loop](skills/staged-capability-loop/) — request-lane policy for DIRECT, LOOKUP, ACTION, and STAGED execution, including review and verification rules for complex work.

```text
User / Channel
      |
      v
CogentNexus Host Controller
      |  durable Ticket + lifecycle/recovery
      v
OpenClaw
      |
      v
Staged Capability Loop admission
  | DIRECT
  | LOOKUP
  | ACTION
  ` STAGED -> CogentNexus durable workflow machinery as needed
```

The key boundary is intentional:

- **CogentNexus Host** answers: "How do we make sure accepted work does not disappear?"
- **Staged Capability Loop** answers: "How much execution machinery does this request actually need?"
- **Durable workflow controller** answers: "How do we verify, checkpoint, recover, and complete the requests that truly need staged execution?"

Ticket-first continuity does not mean every request becomes STAGED. A greeting may receive a normal DIRECT reply even though its owner message was durably accepted first.

## Optional control layer

CogentNexus enhances OpenClaw without making OpenClaw depend on CogentNexus.

In **MANAGED** mode, CogentNexus owns Ticket-first continuity and managed lifecycle/recovery behavior. In **PASSTHROUGH** mode, CogentNexus relinquishes interception/background ownership and OpenClaw behaves normally. Deliberate shutdown uses **MAINTENANCE** semantics so the supervisor does not fight operator intent.

This means the system can be disabled for native OpenClaw testing or normal use without uninstalling CogentNexus or deleting durable state.

## Installation

1. Install [CogentNexus Core](https://github.com/funggier/cogentnexus/blob/main/docs/INSTALL.md).
2. Clone this repository.
3. Run the ecosystem installer:

```powershell
python .\scripts\install.py --workspace "$HOME\.openclaw\workspace"
```

The installer copies `staged-capability-loop`, validates the installed files, and safely updates only the CogentNexus-managed block in `AGENTS.md`. Existing user content is preserved and backed up.

Use `--skip-agents-policy` only when another workspace policy already provides equivalent managed admission/routing behavior.

## Request routing

- **DIRECT** — greetings, conversation, advice, explanations, brainstorming, and simple drafting.
- **LOOKUP** — focused read-only retrieval with the minimum necessary tools.
- **ACTION** — bounded reversible work with proportionate verification.
- **STAGED** — complex, risky, long-running, interruption-prone, dependency-heavy, externally mutating, repeatedly failing, or independently reviewed work.

Always choose the **lightest reliable lane**. Do not escalate merely because CogentNexus is enabled.

## Reliability model

The ecosystem intentionally applies different reliability costs to different work:

- **DIRECT:** lightweight execution with durable acceptance; no staged workflow by default.
- **LOOKUP/ACTION:** bounded tools and proportionate verification.
- **STAGED:** durable checkpoints, controller state, deterministic gates, bounded repair, reviewer policy, and recovery from interruption.

Across all managed modes, the continuity invariant remains: once a user message is durably accepted, it must not silently disappear; it must eventually become delivered/completed, cancelled, or explicitly failed with evidence.

## Compatibility

Compatibility is stated only for versions tested together. See [COMPATIBILITY.md](docs/COMPATIBILITY.md) and each GitHub release.

## License

MIT
