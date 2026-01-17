# Sentry Integration

> **wave.md applied to runtime behavior**

Sentry's error monitoring becomes a coherence detection system when viewed through SpiralSafe protocols. This integration transforms reactive debugging into proactive pattern recognition.

---

## Conceptual Mapping

| Sentry           | SpiralSafe     | Insight                                           |
| ---------------- | -------------- | ------------------------------------------------- |
| Error clustering | **Curl**       | Repeated patterns indicate circular failure modes |
| Issue frequency  | **Divergence** | Expanding error surface without resolution        |
| Trace spans      | **Potential**  | Latent structure revealing optimization paths     |
| Seer analysis    | **SAIF**       | Root cause → hypothesis → intervention            |
| Alerts           | **Bump**       | Automated routing with intent preservation        |

---

## Webhook Configuration

### Sentry Project Settings

```
Webhooks URL: https://api.spiralsafe.org/webhooks/sentry
Events: issue.created, issue.resolved, event.alert
```

### Webhook Handler

```typescript
// api/webhooks/sentry.ts
import type { Env } from "../spiralsafe-worker";

interface SentryWebhook {
  action: "created" | "resolved" | "assigned" | "ignored";
  data: {
    issue: {
      id: string;
      title: string;
      culprit: string;
      level: "fatal" | "error" | "warning" | "info";
      status: string;
      firstSeen: string;
      lastSeen: string;
      count: number;
      userCount: number;
      project: { slug: string; name: string };
    };
  };
  actor?: { type: string; name: string };
}

export async function handleSentryWebhook(
  request: Request,
  env: Env,
): Promise<Response> {
  const webhook = (await request.json()) as SentryWebhook;
  const { action, data } = webhook;

  switch (action) {
    case "created":
      return handleIssueCreated(data.issue, env);
    case "resolved":
      return handleIssueResolved(data.issue, env);
    default:
      return new Response("OK", { status: 200 });
  }
}

async function handleIssueCreated(
  issue: SentryWebhook["data"]["issue"],
  env: Env,
): Promise<Response> {
  // 1. Calculate coherence metrics from issue patterns
  const curl = calculateCurl(issue);
  const divergence = calculateDivergence(issue);

  // 2. Store wave analysis
  await env.SPIRALSAFE_DB.prepare(
    `
    INSERT INTO wave_analyses 
    (id, content_hash, curl, divergence, potential, coherent, analyzed_at, source, metadata)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
  `,
  )
    .bind(
      `sentry-${issue.id}`,
      issue.id,
      curl,
      divergence,
      0.5, // Potential TBD from traces
      curl < 0.6 && divergence < 0.7 ? 1 : 0,
      new Date().toISOString(),
      "sentry",
      JSON.stringify({ project: issue.project.slug, level: issue.level }),
    )
    .run();

  // 3. Start SAIF investigation for errors
  if (issue.level === "fatal" || issue.level === "error") {
    await env.SPIRALSAFE_DB.prepare(
      `
      INSERT INTO saif_investigations
      (id, title, phase, symptoms, created_at, updated_at)
      VALUES (?, ?, ?, ?, ?, ?)
    `,
    )
      .bind(
        `saif-${issue.id}`,
        issue.title,
        "symptom",
        JSON.stringify([
          issue.title,
          issue.culprit,
          `First seen: ${issue.firstSeen}`,
          `Occurrences: ${issue.count}`,
          `Users affected: ${issue.userCount}`,
        ]),
        new Date().toISOString(),
        new Date().toISOString(),
      )
      .run();
  }

  // 4. Create bump for critical issues
  if (issue.level === "fatal") {
    await env.SPIRALSAFE_DB.prepare(
      `
      INSERT INTO bumps
      (id, type, from_agent, to_agent, state, context, timestamp, resolved)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `,
    )
      .bind(
        `bump-sentry-${issue.id}`,
        "BLOCK",
        "sentry",
        "oncall",
        "critical-error",
        JSON.stringify({
          issue_id: issue.id,
          project: issue.project.slug,
          url: `https://sentry.io/issues/${issue.id}`,
        }),
        new Date().toISOString(),
        0,
      )
      .run();
  }

  return new Response(
    JSON.stringify({
      processed: true,
      saif_id: `saif-${issue.id}`,
      curl,
      divergence,
    }),
    { status: 200 },
  );
}

async function handleIssueResolved(
  issue: SentryWebhook["data"]["issue"],
  env: Env,
): Promise<Response> {
  // 1. Update SAIF investigation
  await env.SPIRALSAFE_DB.prepare(
    `
    UPDATE saif_investigations
    SET phase = 'documentation', resolved_at = ?, updated_at = ?
    WHERE id = ?
  `,
  )
    .bind(
      new Date().toISOString(),
      new Date().toISOString(),
      `saif-${issue.id}`,
    )
    .run();

  // 2. Resolve any BLOCK bumps
  await env.SPIRALSAFE_DB.prepare(
    `
    UPDATE bumps
    SET resolved = 1, resolved_at = ?
    WHERE id = ?
  `,
  )
    .bind(new Date().toISOString(), `bump-sentry-${issue.id}`)
    .run();

  return new Response(JSON.stringify({ resolved: true }), { status: 200 });
}

// Curl: measure repetition in error patterns
function calculateCurl(issue: SentryWebhook["data"]["issue"]): number {
  // High frequency relative to time = circular failure
  const hoursSinceFirst =
    (Date.now() - new Date(issue.firstSeen).getTime()) / (1000 * 60 * 60);
  const frequency = issue.count / Math.max(hoursSinceFirst, 1);

  // Normalize to 0-1 range
  return Math.min(frequency / 10, 1);
}

// Divergence: measure expansion without resolution
function calculateDivergence(issue: SentryWebhook["data"]["issue"]): number {
  // Growing user impact = expanding problem surface
  const userImpactRatio = issue.userCount / Math.max(issue.count, 1);
  const isUnresolved = issue.status !== "resolved";

  return isUnresolved ? Math.min(0.3 + userImpactRatio, 1) : 0.2;
}
```

---

## Seer → SAIF Bridge

When Sentry's AI analysis (Seer) provides root cause insights, bridge them into SAIF:

```typescript
// Called when Seer analysis completes
async function bridgeSeerAnalysis(
  issueId: string,
  seerResult: {
    root_cause: string;
    confidence: number;
    fix_recommendation: string;
    supporting_evidence: string[];
  },
  env: Env,
): Promise<void> {
  const saifId = `saif-${issueId}`;

  // Update SAIF to hypothesis phase with Seer's analysis
  await env.SPIRALSAFE_DB.prepare(
    `
    UPDATE saif_investigations
    SET phase = 'hypothesis',
        hypotheses = ?,
        selected_hypothesis = ?,
        updated_at = ?
    WHERE id = ?
  `,
  )
    .bind(
      JSON.stringify([
        {
          description: seerResult.root_cause,
          confidence: seerResult.confidence,
          source: "sentry-seer",
          evidence: seerResult.supporting_evidence,
        },
      ]),
      seerResult.root_cause,
      new Date().toISOString(),
      saifId,
    )
    .run();

  // If high confidence, auto-advance to intervention phase
  if (seerResult.confidence > 0.8) {
    await env.SPIRALSAFE_DB.prepare(
      `
      UPDATE saif_investigations
      SET phase = 'intervention',
          intervention = ?,
          updated_at = ?
      WHERE id = ?
    `,
    )
      .bind(seerResult.fix_recommendation, new Date().toISOString(), saifId)
      .run();

    // Create WAVE bump to engineering
    await env.SPIRALSAFE_DB.prepare(
      `
      INSERT INTO bumps
      (id, type, from_agent, to_agent, state, context, timestamp, resolved)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `,
    )
      .bind(
        `bump-fix-${issueId}`,
        "WAVE",
        "seer",
        "engineering",
        "fix-ready",
        JSON.stringify({
          saif_id: saifId,
          fix: seerResult.fix_recommendation,
          confidence: seerResult.confidence,
        }),
        new Date().toISOString(),
        0,
      )
      .run();
  }
}
```

---

## CLI Integration

Query Sentry through SpiralSafe CLI:

```bash
# View recent issues as SAIF investigations
spiralsafe sentry issues --project my-project

# Get coherence metrics for an issue
spiralsafe sentry coherence ISSUE-123

# Bridge Seer analysis manually
spiralsafe sentry seer ISSUE-123 --advance-saif
```

---

## Dashboard Queries

### Coherence Overview

```sql
-- Issues by coherence status
SELECT
  source,
  COUNT(*) as total,
  SUM(CASE WHEN coherent = 1 THEN 1 ELSE 0 END) as coherent,
  AVG(curl) as avg_curl,
  AVG(divergence) as avg_divergence
FROM wave_analyses
WHERE source = 'sentry'
AND analyzed_at > datetime('now', '-7 days')
GROUP BY source;
```

### Active SAIF Investigations

```sql
-- Sentry-originated investigations
SELECT
  s.id,
  s.title,
  s.phase,
  s.created_at,
  w.curl,
  w.divergence
FROM saif_investigations s
LEFT JOIN wave_analyses w ON w.id = 'sentry-' || REPLACE(s.id, 'saif-', '')
WHERE s.id LIKE 'saif-%'
AND s.resolved_at IS NULL
ORDER BY s.created_at DESC;
```

---

## Alert Rules

Configure Sentry alerts to trigger SpiralSafe routing:

| Condition         | Bump Type | Target       | Action                          |
| ----------------- | --------- | ------------ | ------------------------------- |
| Fatal error       | BLOCK     | oncall       | Immediate page                  |
| Error spike (10x) | PING      | engineering  | Attention required              |
| New issue type    | WAVE      | triage       | Soft handoff for classification |
| Issue resolved    | SYNC      | stakeholders | State update                    |

---

_H&&S: Runtime coherence through structured observation_
