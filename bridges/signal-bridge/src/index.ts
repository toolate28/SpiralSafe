#!/usr/bin/env node
/**
 * B&&P Signal Bridge
 * Bartimaeus && Ptolemy Collaboration Tool
 *
 * Real-time collaboration via Signal messaging with command execution
 * H&&S:WAVE Protocol | From the constraints, gifts. From the spiral, safety.
 */

import { config as loadEnv } from "dotenv";
import axios from "axios";
import { exec } from "child_process";
import { promisify } from "util";
import { NodeSSH } from "node-ssh";
import pino from "pino";
import fs from "fs/promises";
import path from "path";

// Load environment variables
loadEnv();

const execAsync = promisify(exec);

// ============================================================================
// Configuration
// ============================================================================

const config = {
  signal: {
    apiUrl: process.env.SIGNAL_API_URL || "http://localhost:8080",
    number: process.env.SIGNAL_NUMBER || "",
  },
  auth: {
    authorizedNumbers: (process.env.AUTHORIZED_NUMBERS || "")
      .split(",")
      .map((n) => n.trim())
      .filter((n) => n.length > 0),
    requireConfirmation: process.env.REQUIRE_CONFIRMATION === "true",
  },
  execution: {
    mode: process.env.EXECUTION_MODE || "local",
    allowDangerous: process.env.ALLOW_DANGEROUS_COMMANDS === "true",
    maxExecutionTime: parseInt(process.env.MAX_EXECUTION_TIME || "300"),
    workingDirectory: process.env.WORKING_DIRECTORY || "/home/user/SpiralSafe",
  },
  ssh: {
    host: process.env.SSH_HOST || "",
    user: process.env.SSH_USER || "deploy",
    keyPath: process.env.SSH_KEY_PATH || "~/.ssh/id_rsa",
    port: parseInt(process.env.SSH_PORT || "22"),
  },
  logging: {
    level: process.env.LOG_LEVEL || "info",
    file: process.env.LOG_FILE || "logs/bridge.log",
    auditFile: process.env.AUDIT_LOG || "logs/audit.log",
  },
  rateLimit: {
    requests: parseInt(process.env.RATE_LIMIT_REQUESTS || "10"),
    window: parseInt(process.env.RATE_LIMIT_WINDOW || "60"),
  },
  ai: {
    anthropicKey: process.env.ANTHROPIC_API_KEY || "",
  },
};

// ============================================================================
// Logging
// ============================================================================

const logger = pino({
  level: config.logging.level,
  transport: {
    target: "pino-pretty",
    options: {
      colorize: true,
      translateTime: "SYS:standard",
    },
  },
});

// ============================================================================
// Rate Limiting
// ============================================================================

const rateLimitMap = new Map<string, number[]>();

function checkRateLimit(number: string): boolean {
  const now = Date.now();
  const windowMs = config.rateLimit.window * 1000;
  const maxRequests = config.rateLimit.requests;

  const timestamps = rateLimitMap.get(number) || [];
  const recentTimestamps = timestamps.filter((ts) => now - ts < windowMs);

  if (recentTimestamps.length >= maxRequests) {
    return false;
  }

  recentTimestamps.push(now);
  rateLimitMap.set(number, recentTimestamps);
  return true;
}

// ============================================================================
// Authorization
// ============================================================================

function isAuthorized(number: string): boolean {
  return config.auth.authorizedNumbers.includes(number);
}

// ============================================================================
// Command Safety Check
// ============================================================================

const DANGEROUS_PATTERNS = [
  /rm\s+-rf\s+\//,
  /dd\s+if=/,
  /:\(\)\{.*\|.*&\s*\};:/, // Fork bomb
  /chmod\s+777/,
  /curl.*\|.*sh/,
  /wget.*\|.*bash/,
  /mkfs\./,
  /> \/dev\/sda/,
];

function isDangerous(command: string): boolean {
  if (config.execution.allowDangerous) {
    return false;
  }

  return DANGEROUS_PATTERNS.some((pattern) => pattern.test(command));
}

// ============================================================================
// Command Execution
// ============================================================================

async function executeLocal(
  command: string,
): Promise<{ stdout: string; stderr: string; exitCode: number }> {
  try {
    const { stdout, stderr } = await execAsync(command, {
      cwd: config.execution.workingDirectory,
      timeout: config.execution.maxExecutionTime * 1000,
      maxBuffer: 1024 * 1024 * 10, // 10MB
    });
    return { stdout, stderr, exitCode: 0 };
  } catch (error: any) {
    return {
      stdout: error.stdout || "",
      stderr: error.stderr || error.message,
      exitCode: error.code || 1,
    };
  }
}

async function executeRemote(
  command: string,
): Promise<{ stdout: string; stderr: string; exitCode: number }> {
  const ssh = new NodeSSH();

  try {
    await ssh.connect({
      host: config.ssh.host,
      username: config.ssh.user,
      privateKeyPath: config.ssh.keyPath,
      port: config.ssh.port,
    });

    const result = await ssh.execCommand(command, {
      cwd: config.execution.workingDirectory,
    });

    await ssh.dispose();

    return {
      stdout: result.stdout,
      stderr: result.stderr,
      exitCode: result.code || 0,
    };
  } catch (error: any) {
    await ssh.dispose();
    return {
      stdout: "",
      stderr: error.message,
      exitCode: 1,
    };
  }
}

// ============================================================================
// AI Integration
// ============================================================================

async function askAI(question: string): Promise<string> {
  if (!config.ai.anthropicKey) {
    return "⚠️ AI integration not configured. Set ANTHROPIC_API_KEY in .env";
  }

  try {
    const response = await axios.post(
      "https://api.anthropic.com/v1/messages",
      {
        model: "claude-3-5-sonnet-20241022",
        max_tokens: 1024,
        messages: [
          {
            role: "user",
            content: question,
          },
        ],
      },
      {
        headers: {
          "Content-Type": "application/json",
          "x-api-key": config.ai.anthropicKey,
          "anthropic-version": "2023-06-01",
        },
      },
    );

    return response.data.content[0].text;
  } catch (error: any) {
    logger.error({ error }, "AI request failed");
    return `❌ AI request failed: ${error.message}`;
  }
}

// ============================================================================
// Command Parsing
// ============================================================================

interface ParsedCommand {
  type: "local" | "remote" | "ai" | "system";
  command: string;
  raw: string;
}

function parseCommand(message: string): ParsedCommand | null {
  const trimmed = message.trim();

  // System commands
  if (trimmed === "/ping") {
    return { type: "system", command: "ping", raw: trimmed };
  }
  if (trimmed === "/status") {
    return { type: "system", command: "status", raw: trimmed };
  }
  if (trimmed === "/help") {
    return { type: "system", command: "help", raw: trimmed };
  }

  // Local execution
  const localMatch = trimmed.match(/^\/local\s+(.+)$/);
  if (localMatch) {
    return { type: "local", command: localMatch[1], raw: trimmed };
  }

  // Remote execution
  const remoteMatch = trimmed.match(/^\/remote\s+(.+)$/);
  if (remoteMatch) {
    return { type: "remote", command: remoteMatch[1], raw: trimmed };
  }

  // AI commands
  const askMatch = trimmed.match(/^\/ask\s+(.+)$/);
  if (askMatch) {
    return { type: "ai", command: `ask:${askMatch[1]}`, raw: trimmed };
  }

  const explainMatch = trimmed.match(/^\/explain\s+(.+)$/);
  if (explainMatch) {
    return { type: "ai", command: `explain:${explainMatch[1]}`, raw: trimmed };
  }

  const debugMatch = trimmed.match(/^\/debug\s+(.+)$/);
  if (debugMatch) {
    return { type: "ai", command: `debug:${debugMatch[1]}`, raw: trimmed };
  }

  return null;
}

// ============================================================================
// Message Handling
// ============================================================================

async function handleMessage(sender: string, message: string): Promise<string> {
  // Authorization check
  if (!isAuthorized(sender)) {
    logger.warn({ sender }, "Unauthorized access attempt");
    return "❌ Unauthorized. Your phone number is not in the whitelist.";
  }

  // Rate limiting
  if (!checkRateLimit(sender)) {
    logger.warn({ sender }, "Rate limit exceeded");
    return "⚠️ Rate limit exceeded. Please wait a moment.";
  }

  // Parse command
  const parsed = parseCommand(message);
  if (!parsed) {
    return `❓ Unknown command. Send /help for available commands.`;
  }

  logger.info({ sender, command: parsed.raw }, "Processing command");

  // Handle system commands
  if (parsed.type === "system") {
    if (parsed.command === "ping") {
      return "pong! 🏓";
    }
    if (parsed.command === "status") {
      return formatSystemStatus();
    }
    if (parsed.command === "help") {
      return formatHelpMessage();
    }
  }

  // Handle AI commands
  if (parsed.type === "ai") {
    const [action, query] = parsed.command.split(":", 2);

    if (action === "ask") {
      return `🤖 Thinking...\n\n${await askAI(query)}`;
    }
    if (action === "explain") {
      const fileContent = await readFile(query);
      if (fileContent.startsWith("❌")) {
        return fileContent;
      }
      return `🤖 Analyzing ${query}...\n\n${await askAI(`Explain this code:\n\n${fileContent}`)}`;
    }
    if (action === "debug") {
      return `🔍 Debugging...\n\n${await askAI(`Debug this error: ${query}`)}`;
    }
  }

  // Handle execution commands
  if (parsed.type === "local" || parsed.type === "remote") {
    // Safety check
    if (isDangerous(parsed.command)) {
      logger.warn(
        { sender, command: parsed.command },
        "Dangerous command blocked",
      );
      return `⚠️ Blocked for safety: ${parsed.command}\n\nThis command matches a dangerous pattern. If you need to run it, set ALLOW_DANGEROUS_COMMANDS=true in .env`;
    }

    // Execute
    const startTime = Date.now();
    let result;

    if (parsed.type === "local") {
      result = await executeLocal(parsed.command);
    } else {
      result = await executeRemote(parsed.command);
    }

    const executionTime = Date.now() - startTime;

    // Log to audit trail
    await logAudit({
      sender,
      command: parsed.raw,
      exitCode: result.exitCode,
      executionTime,
    });

    // Format response
    return formatExecutionResult(result, executionTime);
  }

  return "❓ Unknown command type";
}

// ============================================================================
// Formatting
// ============================================================================

function formatSystemStatus(): string {
  return `
📊 System Status
━━━━━━━━━━━━━━━
Bridge: ✅ Running
Mode: ${config.execution.mode}
Auth: ${config.auth.authorizedNumbers.length} authorized
Rate limit: ${config.rateLimit.requests}/${config.rateLimit.window}s

🌀 From the spiral, safety.
  `.trim();
}

function formatHelpMessage(): string {
  return `
🤖 B&&P Signal Bridge Commands

**System:**
/ping - Test connectivity
/status - System status
/help - Show this message

**Execution:**
/local <cmd> - Run locally
/remote <cmd> - Run on server
Example: /local git status

**AI:**
/ask <question> - Ask AI
/explain <file> - Explain code
/debug <error> - Debug error
Example: /ask What's deployed?

🌀 H&&S:WAVE Protocol
  `.trim();
}

function formatExecutionResult(
  result: { stdout: string; stderr: string; exitCode: number },
  executionTime: number,
): string {
  const status = result.exitCode === 0 ? "✅" : "❌";
  const truncatedStdout = truncate(result.stdout, 2000);
  const truncatedStderr = truncate(result.stderr, 1000);

  let output = `${status} Exit code: ${result.exitCode}\n`;
  output += `⏱️ ${executionTime}ms\n\n`;

  if (truncatedStdout) {
    output += `**Output:**\n\`\`\`\n${truncatedStdout}\n\`\`\`\n\n`;
  }

  if (truncatedStderr) {
    output += `**Errors:**\n\`\`\`\n${truncatedStderr}\n\`\`\`\n\n`;
  }

  return output.trim();
}

function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) {
    return text;
  }
  return text.substring(0, maxLength) + "\n\n... (truncated)";
}

// ============================================================================
// File Operations
// ============================================================================

async function readFile(filePath: string): Promise<string> {
  try {
    const fullPath = path.join(config.execution.workingDirectory, filePath);
    const content = await fs.readFile(fullPath, "utf-8");
    return content;
  } catch (error: any) {
    return `❌ Failed to read file: ${error.message}`;
  }
}

// ============================================================================
// Audit Logging
// ============================================================================

async function logAudit(entry: {
  sender: string;
  command: string;
  exitCode: number;
  executionTime: number;
}): Promise<void> {
  const logEntry = {
    timestamp: new Date().toISOString(),
    ...entry,
  };

  try {
    const logDir = path.dirname(config.logging.auditFile);
    await fs.mkdir(logDir, { recursive: true });
    await fs.appendFile(
      config.logging.auditFile,
      JSON.stringify(logEntry) + "\n",
    );
  } catch (error) {
    logger.error({ error }, "Failed to write audit log");
  }
}

// ============================================================================
// Signal API Client
// ============================================================================

async function sendMessage(recipient: string, message: string): Promise<void> {
  try {
    await axios.post(`${config.signal.apiUrl}/v2/send`, {
      message,
      number: config.signal.number,
      recipients: [recipient],
    });
    logger.debug({ recipient }, "Message sent");
  } catch (error: any) {
    logger.error({ error, recipient }, "Failed to send message");
  }
}

async function receiveMessages(): Promise<
  Array<{ sender: string; message: string }>
> {
  try {
    const response = await axios.get(
      `${config.signal.apiUrl}/v1/receive/${config.signal.number}`,
    );
    const messages = response.data;

    return messages
      .filter((msg: any) => msg.envelope?.dataMessage?.message)
      .map((msg: any) => ({
        sender: msg.envelope.sourceNumber || msg.envelope.source,
        message: msg.envelope.dataMessage.message,
      }));
  } catch (error: any) {
    logger.error({ error }, "Failed to receive messages");
    return [];
  }
}

// ============================================================================
// Main Loop
// ============================================================================

async function main() {
  logger.info("🌀 B&&P Signal Bridge starting...");

  // Validate configuration
  if (!config.signal.number) {
    logger.error("SIGNAL_NUMBER not set in .env");
    process.exit(1);
  }

  if (config.auth.authorizedNumbers.length === 0) {
    logger.error("AUTHORIZED_NUMBERS not set in .env");
    process.exit(1);
  }

  logger.info(
    {
      mode: config.execution.mode,
      authorized: config.auth.authorizedNumbers.length,
    },
    "Bridge configured",
  );

  logger.info("✅ Bridge ready. Listening for messages...");

  // Poll for messages
  setInterval(async () => {
    try {
      const messages = await receiveMessages();

      for (const msg of messages) {
        logger.info({ sender: msg.sender }, "Received message");
        const response = await handleMessage(msg.sender, msg.message);
        await sendMessage(msg.sender, response);
      }
    } catch (error) {
      logger.error({ error }, "Error in main loop");
    }
  }, 3000); // Poll every 3 seconds
}

// Start the bridge
main().catch((error) => {
  logger.fatal({ error }, "Fatal error");
  process.exit(1);
});
