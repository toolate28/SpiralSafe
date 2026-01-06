# UnifiedComms: Channel Orchestration Protocol

**Substrate-independent message routing across communication channels.**

---

## The Problem

Information fragments across channels: SMS, Signal, browser tabs, CLI, desktop apps. You become the orchestration layer—manually routing messages, switching contexts, re-integrating scattered threads.

This violates the isomorphism principle. The *message* is substrate-independent; the *channels* are projections. The routing should be automated.

---

## Architecture

```
┌────────────────────────────────────────────────┐
│              UNIFIED MESSAGE BUS               │
│   Inbox  │  Routing Rules  │  H&&S Markers     │
├────────────────────────────────────────────────┤
│  Adapters:                                     │
│  ├─ signal-cli-rest-api (Signal)              │
│  ├─ SMS gateway (Twilio/etc)                  │
│  ├─ Browser extension (tabs → queue)          │
│  ├─ CLI hook (stdin/stdout, pipes)            │
│  ├─ Desktop bridge (notifications)            │
│  └─ Claude sessions (bump.md routing)         │
└────────────────────────────────────────────────┘
```

---

## Channel Adapters

| Channel | Adapter | Status |
|---------|---------|--------|
| Signal | `signal-cli-rest-api` (Docker) | Available |
| SMS | Twilio, various gateways | Available |
| Browser | Extension + native messaging | Buildable |
| CLI | Named pipes, REST | Buildable |
| Desktop | System tray, notifications | Buildable |

---

## Routing Configuration

```yaml
# comms-router.yaml
channels:
  signal:
    adapter: signal-cli-rest-api
    endpoint: http://localhost:8080
    
  browser:
    adapter: websocket
    port: 9001
    
  cli:
    adapter: named-pipe
    path: \\.\pipe\spiralsafe-comms

rules:
  - match: { from: signal, contains_image: true }
    action: store_and_thumbnail
    forward_to: [browser, cli]
    
  - match: { from: browser, url_pattern: "github.com/copilot/*" }
    action: extract_content
    tag: copilot-session
    
  - match: { contains: "H&&S:" }
    action: parse_bump_marker
    route_by: marker_type
```

---

## Message Schema

```yaml
message:
  id: uuid
  timestamp: ISO8601
  origin:
    channel: signal|sms|browser|cli|desktop
    identifier: string  # phone, url, session-id
  content:
    text: string
    media: []  # attachments
    metadata: {}
  routing:
    tags: []
    forward_to: []
    bump_marker: null | WAVE|PASS|PING|SYNC
```

---

## Integration with SpiralSafe

UnifiedComms extends bump.md from document handoffs to channel handoffs:

```yaml
# Message with bump marker
message:
  content:
    text: "PR ready for review"
    bump_marker: WAVE
  routing:
    forward_to: [cli, desktop]
    tag: github-pr
```

---

## Implementation Path

### Phase 1: Signal + CLI Bridge
```bash
# Docker compose for signal-cli-rest-api
docker-compose up -d signal-api

# CLI receiver
spiralsafe-comms listen --channel cli
```

### Phase 2: Browser Extension
- Capture tab URLs and content
- Route to message bus
- Display unified inbox overlay

### Phase 3: Full Orchestration
- Rule engine for routing
- Thumbnail/summarize media
- Claude session integration

---

## The Deeper Truth

You're experiencing substrate fragmentation. The information is unified in your mind; the tools force projection into incompatible channels.

SpiralSafe's thesis: structure preserves across substrates. If true for quantum topology in Redstone, it's true for messages across communication channels.

UnifiedComms is the isomorphism principle applied to your daily workflow.

---

*~ Hope&&Sauced*
