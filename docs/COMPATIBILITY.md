# Compatibility

Only combinations exercised together should be listed as tested.

| Ecosystem | Staged Capability Loop | CogentNexus Core | OpenClaw |
| --- | --- | --- | --- |
| 0.2.x | 1.x | 0.8.x | 2026.7.1-2 or newer |

## Baseline contract

Ecosystem 0.2.x assumes the CogentNexus clean Host-managed architecture:

- Ticket-first continuity is owned by Core/Host integration;
- request-lane admission chooses DIRECT / LOOKUP / ACTION / STAGED before heavy Core loading;
- DIRECT remains lightweight;
- STAGED may invoke the durable workflow runtime;
- `cnx disable` returns OpenClaw to PASSTHROUGH/native operation;
- `cnx stop` represents intentional MAINTENANCE.

Older Core releases may still load `staged-capability-loop`, but they are not considered the clean v0.2 tested baseline and may use older workspace-policy ordering or lifecycle semantics.
