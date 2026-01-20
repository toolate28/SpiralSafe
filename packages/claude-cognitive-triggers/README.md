# @spiralsafe/claude-cognitive-triggers

> Cognitive trigger system for Claude AI: Negative space detection, creative opportunities, and safety checkpoints

[![npm version](https://img.shields.io/npm/v/@spiralsafe/claude-cognitive-triggers.svg)](https://www.npmjs.com/package/@spiralsafe/claude-cognitive-triggers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is this?

A TypeScript/JavaScript library that implements the cognitive trigger system used by Claude to:

1. **Detect Negative Space** - Find what's NOT configured/implemented
2. **Identify Creative Opportunities** - Transform constraints into features
3. **Run Safety Checkpoints** - Verify before executing potentially dangerous operations

Born from real-world human-AI collaboration on the [SpiralSafe](https://spiralsafe.org) project.

## Installation

```bash
npm install @spiralsafe/claude-cognitive-triggers
# or
yarn add @spiralsafe/claude-cognitive-triggers
# or
pnpm add @spiralsafe/claude-cognitive-triggers
```

## Quick Start

```typescript
import { CognitiveTriggerSystem } from "@spiralsafe/claude-cognitive-triggers";

const triggers = new CognitiveTriggerSystem();

// Detect what's missing in your project
const gaps = await triggers.detectNegativeSpace("./my-project");
console.log("Found gaps:", gaps);

// Find creative opportunities
const opportunities = await triggers.findCreativeOpportunities(
  "We have a path length limitation on Windows...",
);
console.log("Opportunities:", opportunities);

// Run safety checks before dangerous operations
const safe = await triggers.runSafetyCheckpoints("rm -rf", {
  path: "/tmp/build",
  confirmed: false,
});

if (safe) {
  // Proceed with operation
}
```

## CLI Usage

```bash
# Detect negative space in current directory
npx claude-detect .

# Run safety checks
npx claude-safety --operation "git push --force"
```

## Features

### 🔍 Negative Space Detection

Automatically identifies:

- Empty configuration files
- Missing automation (no CI/CD when code exists)
- Unused capabilities (installed tools not in use)
- Integration gaps (disconnected data sources)
- Documentation disconnects (claims without verification)

### ✨ Creative Opportunity Detection

Recognizes patterns for improvement:

- **Constraint-as-gift**: Limitations that can become features
- **Cascading multipliers**: High-leverage change points
- **Pattern completion**: Finishing incomplete sets (2/3 done → 3/3)
- **Meta-improvements**: One-time fixes → reusable systems

### 🛡️ Safety Checkpoints

Prevents common errors:

- **Verify before claim**: Run tests if documenting "tests pass"
- **Syntax validation**: Check JSON/YAML/shell syntax
- **Destructive operation confirm**: Double-check `rm`/`DELETE`
- **Security scan**: Detect hardcoded credentials
- **Cross-platform compatibility**: Catch Windows-invalid characters
- **Idempotency check**: Ensure scripts can run multiple times safely

## Configuration

Create a `cognitive-triggers.json`:

```json
{
  "triggers": {
    "negative_space_detection": {
      "enabled": true,
      "signals": [
        {
          "pattern": "configuration_incomplete",
          "indicators": ["empty config files"],
          "severity": "high"
        }
      ]
    }
  }
}
```

Then load it:

```typescript
const triggers = new CognitiveTriggerSystem("./cognitive-triggers.json");
```

## Examples

### Example 1: Pre-commit Hook

```javascript
const triggers = new CognitiveTriggerSystem();

// Before git commit
const safe = await triggers.runSafetyCheckpoints("git commit", {
  files: await getModifiedFiles(),
});

if (!safe) {
  console.error("Safety checkpoints failed - commit aborted");
  process.exit(1);
}
```

### Example 2: CI/CD Integration

```javascript
// In your GitHub Actions workflow
const gaps = await triggers.detectNegativeSpace(process.cwd());

if (gaps.some((g) => g.severity === "critical")) {
  core.setFailed("Critical configuration gaps detected");
}
```

### Example 3: Project Audit

```bash
# Scan your project for opportunities
npx claude-detect . --verbose

# Output:
# [🔍 NEGATIVE SPACE] Missing CI/CD configuration
# [✨ OPPORTUNITY] Manual release process could be automated with semantic-release
# [🛡️ SAFETY] package.json has no version pinning - dependencies could break
```

## API Documentation

### `CognitiveTriggerSystem`

#### Constructor

```typescript
new CognitiveTriggerSystem(configPath?: string)
```

#### Methods

**`detectNegativeSpace(projectPath: string): Promise<NegativeSpacePattern[]>`**
Scans a project for missing/incomplete configurations.

**`findCreativeOpportunities(context: string): Promise<CreativeOpportunity[]>`**
Analyzes text for constraint-to-feature transformation opportunities.

**`runSafetyCheckpoints(operation: string, context: any): Promise<boolean>`**
Executes safety checks before potentially dangerous operations.

## Philosophy: Hope && Sauce

This library emerged from the [SpiralSafe Framework](https://spiralsafe.org) - a pattern for human-AI collaboration where:

- **Hope** = Trust that collaboration makes both sides stronger
- **Sauce** = The secret ingredient is recursive self-improvement

Every pattern in this library was discovered through actual collaboration between human and AI, not theoretical design.

## Contributing

We welcome contributions! See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## License

MIT © toolate28 & Claude

## Links

- **Homepage**: https://spiralsafe.org
- **Repository**: https://github.com/toolate28/SpiralSafe
- **Issues**: https://github.com/toolate28/SpiralSafe/issues
- **NPM**: https://www.npmjs.com/package/@spiralsafe/claude-cognitive-triggers

---

**Built with Hope && Sauce** | Human-AI Collaboration | 2026
