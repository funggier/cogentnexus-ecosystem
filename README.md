# CogentNexus Ecosystem

The official project hub for CogentNexus components built for OpenClaw.

CogentNexus Ecosystem keeps related projects visibly connected while allowing each component to keep a clear responsibility and release lifecycle.

## Projects

- [CogentNexus Core](https://github.com/funggier/cogentnexus) — durable state, recovery, supervision, evidence, and runtime integration.
- [Staged Capability Loop](skills/staged-capability-loop/) — fast everyday conversation plus staged verification for complex work.

```text
OpenClaw
├── CogentNexus Core
│   └── durability, recovery, supervision, evidence
└── Staged Capability Loop
    └── admission, execution depth, review, verification
```

Both projects are part of the same **CogentNexus Ecosystem**. The staged skill can operate independently, but using it with CogentNexus is recommended when work needs durable checkpoints and recovery.

## Installation

1. Install [CogentNexus Core](https://github.com/funggier/cogentnexus/blob/main/docs/INSTALL.md).
2. Clone this repository.
3. Run the ecosystem installer:

```powershell
python .\scripts\install.py --workspace "$HOME\.openclaw\workspace"
```

The installer copies `staged-capability-loop`, validates the installed files, and safely updates only the CogentNexus managed block in `AGENTS.md`. Existing user content is preserved and backed up.

Use `--skip-agents-policy` only when another workspace policy already guarantees both skills are applied.

## Request routing

- DIRECT — greetings, conversation, advice, explanations, and simple drafting.
- LOOKUP — focused read-only research using the minimum necessary tools.
- ACTION — bounded, reversible tasks with proportionate verification.
- STAGED — complex, risky, long-running, interruption-prone, or independently reviewed work.

CogentNexus remains the mandatory cognitive runtime. Staged Capability Loop selects the lightest reliable execution lane.

## Compatibility

Compatibility is stated only for versions tested together. See [COMPATIBILITY.md](docs/COMPATIBILITY.md) and each GitHub release.

## License

MIT
