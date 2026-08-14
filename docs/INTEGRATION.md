# CogentNexus Ecosystem integration

## Responsibility boundary

- OpenClaw hosts conversations, skills, plugins, tools, and sessions.
- CogentNexus Core provides durable state, admission, recovery, supervision, evidence, and terminal delivery support.
- Staged Capability Loop selects the lightest reliable lane and defines staged review behavior when complexity or risk requires it.

The companion skill does not replace CogentNexus. CogentNexus does not require every greeting or simple answer to enter a durable staged workflow.

## Activation

The ecosystem installer manages one bounded section of workspace `AGENTS.md` between `<!-- cogentnexus:begin -->` and `<!-- cogentnexus:end -->`. It preserves all content outside those markers, creates a backup before changing an existing file, and updates the same block idempotently.

Installing CogentNexus Core alone activates the mandatory CogentNexus Kernel. Installing this ecosystem companion afterward replaces that managed block with the combined runtime-and-routing policy.

## Recommended order

1. Install CogentNexus Core.
2. Install CogentNexus Ecosystem companion skills.
3. Start a fresh OpenClaw session so skill metadata and workspace instructions reload.
4. Verify that both skills are visible and that a greeting uses DIRECT while a consequential multi-step task selects STAGED.
