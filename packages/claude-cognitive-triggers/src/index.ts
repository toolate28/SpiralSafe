/**
 * @spiralsafe/claude-cognitive-triggers
 * Cognitive trigger system for Claude AI
 *
 * @author toolate28 & Claude
 * @license MIT
 */

export interface NegativeSpacePattern {
  pattern: string;
  indicators: string[];
  action: string;
  severity: "critical" | "high" | "medium" | "low";
}

export interface CreativeOpportunity {
  pattern: string;
  indicators: string[];
  action: string;
  examples?: string[];
}

export interface SafetyCheckpoint {
  name: string;
  trigger: string;
  actions: string[];
  severity: "critical" | "high" | "medium" | "low";
  blockOnFail: boolean;
}

export class CognitiveTriggerSystem {
  private negativeSpacePatterns: NegativeSpacePattern[] = [];
  private creativeOpportunities: CreativeOpportunity[] = [];
  private safetyCheckpoints: SafetyCheckpoint[] = [];

  constructor(configPath?: string) {
    if (configPath) {
      this.loadConfig(configPath);
    } else {
      this.loadDefaultConfig();
    }
  }

  /**
   * Detect negative space (what's missing) in a project
   */
  async detectNegativeSpace(
    projectPath: string,
  ): Promise<NegativeSpacePattern[]> {
    const detected: NegativeSpacePattern[] = [];

    // Check for empty config files
    const emptyConfigs = await this.findEmptyConfigs(projectPath);
    if (emptyConfigs.length > 0) {
      detected.push({
        pattern: "configuration_incomplete",
        indicators: emptyConfigs,
        action: "flag_for_optimization",
        severity: "high",
      });
    }

    // Check for missing automation
    const hasCI = await this.checkForCI(projectPath);
    if (!hasCI) {
      detected.push({
        pattern: "missing_automation",
        indicators: ["No CI/CD configuration found"],
        action: "propose_automation",
        severity: "medium",
      });
    }

    return detected;
  }

  /**
   * Find creative opportunities in constraints
   */
  async findCreativeOpportunities(
    context: string,
  ): Promise<CreativeOpportunity[]> {
    const opportunities: CreativeOpportunity[] = [];

    // Detect constraint-as-gift patterns
    if (context.includes("limitation") || context.includes("workaround")) {
      opportunities.push({
        pattern: "constraint_as_gift",
        indicators: ["Limitation mentioned", "Workaround implemented"],
        action: "transform_constraint_into_feature",
        examples: [
          "Path limit → Universal path detection",
          "Manual process → Self-improving automation",
        ],
      });
    }

    return opportunities;
  }

  /**
   * Run safety checkpoints before operations
   */
  async runSafetyCheckpoints(
    operation: string,
    context: any,
  ): Promise<boolean> {
    for (const checkpoint of this.safetyCheckpoints) {
      if (this.shouldTrigger(checkpoint, operation)) {
        const passed = await this.executeCheckpoint(checkpoint, context);
        if (!passed && checkpoint.blockOnFail) {
          console.error(`Safety checkpoint failed: ${checkpoint.name}`);
          return false;
        }
      }
    }
    return true;
  }

  private async findEmptyConfigs(path: string): Promise<string[]> {
    // Implementation would check for empty JSON/YAML files
    return [];
  }

  private async checkForCI(path: string): Promise<boolean> {
    // Implementation would check for .github/workflows, .gitlab-ci.yml, etc.
    return false;
  }

  private shouldTrigger(
    checkpoint: SafetyCheckpoint,
    operation: string,
  ): boolean {
    return operation.toLowerCase().includes(checkpoint.trigger.toLowerCase());
  }

  private async executeCheckpoint(
    checkpoint: SafetyCheckpoint,
    context: any,
  ): Promise<boolean> {
    // Implementation would run actual checks
    return true;
  }

  private loadConfig(path: string): void {
    // Load from file
  }

  private loadDefaultConfig(): void {
    // Load default patterns
    this.negativeSpacePatterns = [
      {
        pattern: "configuration_incomplete",
        indicators: ["empty config files", "TODO markers"],
        action: "flag_for_optimization",
        severity: "high",
      },
    ];
  }
}

export default CognitiveTriggerSystem;
