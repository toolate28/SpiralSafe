# 📱 B&&P Signal Bridge

**Bartimaeus && Ptolemy Collaboration Tool**

Real-time collaboration via Signal messaging with local/remote command execution.

---

## 🌀 Concept

Chat through Signal → Execute commands → Get results back

```
┌─────────────────────────────────────────────────────────────┐
│  Ptolemy's Phone                                            │
│  📱 Signal App                                              │
│  "Run bootstrap.sh"                                         │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  Signal-CLI REST API                                        │
│  Receives message → Parses command → Routes to handler     │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  B&&P Bridge Server                                         │
│  • Authenticates Ptolemy                                    │
│  • Validates command safety                                 │
│  • Executes locally OR forwards to remote                   │
│  • Streams output back to Signal                            │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  Ptolemy's Phone                                            │
│  📱 Signal App                                              │
│  "✅ Bootstrap complete! Output: ..."                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Install Signal-CLI REST API

```bash
# Using Docker (recommended)
# Pin to a specific version for security - update explicitly after verification
docker run -d \
  --name signal-cli-rest-api \
  -p 8080:8080 \
  -v signal-cli-config:/home/.local/share/signal-cli \
  bbernhard/signal-cli-rest-api:0.85

# To update to a newer version:
# 1. Check release notes at https://github.com/bbernhard/signal-cli-rest-api/releases
# 2. Pull and verify the new image: docker pull bbernhard/signal-cli-rest-api:X.XX
# 3. Update the version number above
```

### 2. Link Your Phone Number

```bash
# Register your number
curl -X POST "http://localhost:8080/v1/register/+1234567890"

# Verify with SMS code
curl -X POST "http://localhost:8080/v1/register/+1234567890/verify/123456"
```

### 3. Install B&&P Bridge

```bash
cd bridges/signal-bridge
npm install
cp .env.example .env
nano .env  # Add your config
```

### 4. Start the Bridge

```bash
npm start
```

### 5. Send a Test Message

Send "ping" to your Signal number → Should receive "pong!"

---

## 📋 Features

### Command Execution

**Local Commands:**
```
/local git status
/local npm test
/local ./bootstrap.sh
```

**Remote Commands (SSH):**
```
/remote production git pull
/remote staging npm run deploy
```

### File Operations

**Upload:**
```
/upload config.json
[Attach file to message]
```

**Download:**
```
/download logs/error.log
```

### System Status

```
/status           # Full system status
/health           # Health check
/logs             # Recent logs
/ps               # Running processes
```

### AI Integration

```
/ask What's the current deployment status?
/explain schema.sql
/debug "TypeError: Cannot read property 'foo' of undefined"
```

### Security

- **Whitelist:** Only authorized phone numbers can execute commands
- **Command validation:** Dangerous commands blocked by default
- **Audit trail:** All commands logged with timestamps
- **Rate limiting:** 10 commands per minute per user

---

## 📦 Installation

### Prerequisites

- Node.js 20+
- Docker (for Signal-CLI REST API)
- Signal account with phone number

### Setup

```bash
# 1. Clone repository
cd /home/user/SpiralSafe/bridges/signal-bridge

# 2. Install dependencies
npm install

# 3. Configure environment
cp .env.example .env

# Edit .env:
#   SIGNAL_API_URL=http://localhost:8080
#   SIGNAL_NUMBER=+1234567890
#   AUTHORIZED_NUMBERS=+10987654321
#   EXECUTION_MODE=local  # or 'remote' or 'both'
#   SSH_HOST=your-server.com (for remote mode)

# 4. Start Signal-CLI REST API (Docker)
docker-compose up -d

# 5. Link your Signal account
npm run register

# 6. Start the bridge
npm start
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Signal Configuration
SIGNAL_API_URL=http://localhost:8080
SIGNAL_NUMBER=+1234567890

# Authorization
AUTHORIZED_NUMBERS=+10987654321,+11234567890
REQUIRE_CONFIRMATION=true  # Confirm before executing

# Execution
EXECUTION_MODE=local  # local | remote | both
ALLOW_DANGEROUS_COMMANDS=false
MAX_EXECUTION_TIME=300  # 5 minutes

# Remote Execution (if mode=remote or mode=both)
SSH_HOST=production.spiralsafe.org
SSH_USER=deploy
SSH_KEY_PATH=~/.ssh/id_rsa
SSH_PORT=22

# Logging
LOG_LEVEL=info
LOG_FILE=logs/bridge.log
AUDIT_LOG=logs/audit.log

# Rate Limiting
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60  # seconds

# AI Integration (optional)
ANTHROPIC_API_KEY=your-claude-api-key
```

---

## 💬 Command Reference

### System Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/ping` | Test connectivity | `/ping` |
| `/status` | System status | `/status` |
| `/health` | Health check | `/health` |
| `/help` | Show commands | `/help` |

### Execution Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/local <cmd>` | Run locally | `/local git status` |
| `/remote <cmd>` | Run on server | `/remote pm2 restart api` |
| `/exec <cmd>` | Auto-route | `/exec npm test` |
| `/bg <cmd>` | Background task | `/bg npm run build` |

### File Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/upload` | Upload file | `/upload [attach file]` |
| `/download <path>` | Download file | `/download logs/error.log` |
| `/ls <path>` | List directory | `/ls /var/www` |
| `/cat <file>` | Read file | `/cat .env.example` |

### Git Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/git status` | Git status | `/git status` |
| `/git pull` | Pull changes | `/git pull` |
| `/git push` | Push changes | `/git push` |
| `/git log` | Recent commits | `/git log` |

### AI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/ask <question>` | Ask AI | `/ask What's deployed?` |
| `/explain <file>` | Explain code | `/explain schema.sql` |
| `/debug <error>` | Debug error | `/debug "ReferenceError: foo"` |
| `/suggest <task>` | Get suggestion | `/suggest optimize database` |

### Admin Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/logs` | Show logs | `/logs` |
| `/ps` | Processes | `/ps` |
| `/restart` | Restart bridge | `/restart` |
| `/whitelist <number>` | Add user | `/whitelist +11234567890` |

---

## 🔒 Security

### Authorization Flow

```
Message received
    ↓
Check sender number
    ↓
    ├─ Authorized? → Continue
    └─ Not authorized? → "❌ Unauthorized"
            ↓
Parse command
    ↓
Validate command safety
    ↓
    ├─ Safe? → Continue
    └─ Dangerous? → "⚠️ Blocked: rm -rf /"
            ↓
[Optional] Request confirmation
    ↓
Execute command
    ↓
Stream output to Signal
    ↓
Log to audit trail
```

### Blocked Commands (Default)

- `rm -rf`
- `dd if=/dev/zero`
- `:(){ :|:& };:`
- `chmod 777`
- `wget | sh`
- `curl | bash`
- Any command with `sudo` (unless explicitly allowed)

### Confirmation Required

- File deletions
- Database operations
- Git push/force push
- Service restarts
- System modifications

---

## 📊 Usage Examples

### Example 1: Check API Status

```
You: /status

Bridge:
📊 System Status
━━━━━━━━━━━━━━━
API: ✅ Healthy (18ms)
Database: ✅ Healthy (5ms)
KV: ✅ Healthy (2ms)
R2: ✅ Healthy (12ms)

Last deployment: 2 hours ago
Uptime: 99.97%
```

### Example 2: Deploy Update

```
You: /remote production git pull

Bridge:
⚙️ Executing on production...

Output:
remote: Enumerating objects: 15, done.
remote: Counting objects: 100% (15/15), done.
remote: Compressing objects: 100% (8/8), done.
remote: Total 10 (delta 6), reused 8 (delta 4)
Unpacking objects: 100% (10/10), done.
From github.com:toolate28/SpiralSafe
   aa3fee5..31e789a  main -> origin/main
Updating aa3fee5..31e789a
Fast-forward
 bootstrap.sh | 300 +++++++++++++
 1 file changed, 300 insertions(+)

✅ Complete in 2.3s
```

### Example 3: Ask AI About Code

```
You: /ask What does ATOM-AUTH do?

Bridge:
🤖 Analyzing...

ATOM-AUTH is a revolutionary 3-factor authentication system:

1. **Conversational Coherence** - You prove identity by having authentic conversations
2. **LED Keycode Display** - Physical hardware verification (ESP32 + LED matrix)
3. **Projector Image CAPTCHA** - Visual challenges with AI validation

It's designed so that authentication becomes a creative, meaningful act rather than just remembering a password.

Status: Design complete ✅
Location: ops/ATOM_AUTH_SYSTEM.md
```

### Example 4: Debug Production Error

```
You: /logs error

Bridge:
📋 Recent errors (last 10):

2026-01-07 19:45:23 [ERROR] TypeError: Cannot read property 'code' of undefined
  at validateLEDKeycode (spiralsafe-worker.ts:782)
  at handleLEDVerification (spiralsafe-worker.ts:924)

2026-01-07 19:32:15 [ERROR] Rate limit exceeded for IP 203.0.113.42

You: /debug "Cannot read property 'code'"

Bridge:
🔍 Analyzing error...

**Issue:** Undefined check missing on `ledKeycode` object

**Root cause:** `verifyLEDKeycode()` returns `false` instead of throwing, but handler assumes object exists

**Fix:**
```typescript
const keycode: LEDKeycode | null = JSON.parse(stored);
if (!keycode || !keycode.code) {
  return false;
}
```

**File:** ops/spiralsafe-worker.ts:780-783
**Severity:** Medium (runtime error)
**Action:** Add null check before accessing `.code` property
```

---

## 🏗️ Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│  Signal Messaging Layer                                     │
│  • Signal-CLI REST API (Docker)                             │
│  • Message polling (3-second interval)                      │
│  • Attachment handling                                      │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  B&&P Bridge Server (Node.js + TypeScript)                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Message Handler                                    │   │
│  │  • Parse commands                                   │   │
│  │  • Validate syntax                                  │   │
│  │  • Route to executors                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Authorization                                      │   │
│  │  • Whitelist check                                  │   │
│  │  • Rate limiting                                    │   │
│  │  • Audit logging                                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Executors                                          │   │
│  │  • Local executor (child_process)                   │   │
│  │  • Remote executor (SSH)                            │   │
│  │  • AI executor (Claude API)                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Response Formatter                                 │   │
│  │  • Truncate long output                             │   │
│  │  • Add emoji indicators                             │   │
│  │  • Format markdown                                  │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  Execution Environment                                      │
│  ┌────────────────────┐    ┌────────────────────┐          │
│  │  Local Machine     │    │  Remote Server     │          │
│  │  • Git repo        │    │  • Production API  │          │
│  │  • Build tools     │    │  • PM2 processes   │          │
│  │  • Scripts         │    │  • Logs            │          │
│  └────────────────────┘    └────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```typescript
// 1. Receive message from Signal
const message = await signalAPI.receive();

// 2. Authorize sender
if (!isAuthorized(message.sender)) {
  return sendReply("❌ Unauthorized");
}

// 3. Parse command
const command = parseCommand(message.text);

// 4. Validate safety
if (isDangerous(command)) {
  return sendReply("⚠️ Blocked for safety");
}

// 5. Execute
const result = await execute(command, {
  mode: config.EXECUTION_MODE,  // local | remote | both
  timeout: config.MAX_EXECUTION_TIME,
  cwd: '/home/user/SpiralSafe',
});

// 6. Format and send response
const formatted = formatOutput(result);
await sendReply(formatted);

// 7. Log to audit trail
logAudit({
  sender: message.sender,
  command: command.raw,
  result: result.exitCode,
  timestamp: new Date(),
});
```

---

## 🧪 Development

### Running Tests

```bash
npm test
npm run test:watch
npm run test:coverage
```

### Local Development

```bash
# Start in development mode (hot reload)
npm run dev

# Build TypeScript
npm run build

# Lint code
npm run lint

# Format code
npm run format
```

---

## 📝 Logging

### Log Files

- `logs/bridge.log` - General application logs
- `logs/audit.log` - Command execution audit trail
- `logs/error.log` - Errors only

### Log Format

```json
{
  "timestamp": "2026-01-07T19:45:23.123Z",
  "level": "info",
  "sender": "+10987654321",
  "command": "/local git status",
  "result": "success",
  "executionTime": 245,
  "output": "[truncated]"
}
```

---

## 🔄 Deployment

### Production Deployment

```bash
# 1. Build for production
npm run build

# 2. Start with PM2
pm2 start dist/index.js --name signal-bridge

# 3. Save PM2 config
pm2 save

# 4. Enable startup script
pm2 startup
```

### Docker Deployment

```bash
# Build image
docker build -t spiralsafe/signal-bridge .

# Run container
docker run -d \
  --name signal-bridge \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/.env:/app/.env \
  --restart unless-stopped \
  spiralsafe/signal-bridge
```

---

## 🐛 Troubleshooting

### Common Issues

**Signal-CLI not responding:**
```bash
# Check if Docker container is running
docker ps | grep signal-cli-rest-api

# Restart container
docker restart signal-cli-rest-api

# Check logs
docker logs signal-cli-rest-api
```

**Commands not executing:**
```bash
# Check authorization
cat .env | grep AUTHORIZED_NUMBERS

# Check audit log
tail -f logs/audit.log

# Test manually
curl http://localhost:8080/v2/send \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "number": "+1234567890", "recipients": ["+10987654321"]}'
```

**Remote execution failing:**
```bash
# Test SSH connection
ssh -i ~/.ssh/id_rsa deploy@production.spiralsafe.org

# Check SSH config in .env
cat .env | grep SSH_
```

---

## 🌀 H&&S:WAVE Integration

The B&&P Signal Bridge integrates with H&&S:WAVE protocol:

- **WAVE analysis on commands:** Analyze coherence of natural language commands
- **ATOM tracking:** Create ATOM sessions for deployments
- **AWI grants:** Check permissions via AWI system
- **BUMP markers:** Track state transitions across platforms

---

## 📚 References

- [Signal-CLI REST API](https://github.com/bbernhard/signal-cli-rest-api)
- [Signal-CLI](https://github.com/AsamK/signal-cli)
- [Signal Protocol](https://signal.org/docs/)

---

**Status:** DESIGN COMPLETE ✅
**Next:** Implement TypeScript server

🌀 **H&&S:WAVE** | From the constraints, gifts. From the spiral, safety.
