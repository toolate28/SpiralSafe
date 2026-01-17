# 🔐 SpiralSafe Admin System Architecture

**Version**: 1.0.0
**Subdomain**: console.spiralsafe.org
**Purpose**: Internal administrative dashboard for monitoring, management, and operations

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  console.spiralsafe.org                      │
│                    (Admin Console)                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ├─── JWT Authentication
                            ├─── Session Management (KV)
                            ├─── IP Allowlisting (optional)
                            └─── 2FA Support (future)
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
    ┌───▼────┐        ┌────▼─────┐       ┌────▼─────┐
    │ Login  │        │Dashboard │       │  Admin   │
    │  Page  │        │   UI     │       │   API    │
    └────────┘        └──────────┘       └──────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
    ┌───▼────┐        ┌────▼─────┐       ┌────▼─────┐
    │Metrics │        │  Logs    │       │  User    │
    │Viewer  │        │ Explorer │       │  Mgmt    │
    └────────┘        └──────────┘       └──────────┘
```

---

## Authentication Flow

### Phase 1: Username/Password (Current Implementation)

```
1. User visits console.spiralsafe.org
2. Enter username + password
3. Backend validates credentials against D1 database
4. Generate JWT token (24h expiration)
5. Store session in KV (with IP binding)
6. Return JWT to frontend
7. Frontend stores JWT in httpOnly cookie
8. All admin API requests include JWT in Authorization header
```

### Phase 2: OAuth + 2FA (Future)

```
1. User clicks "Login with GitHub"
2. OAuth flow → GitHub authentication
3. Backend validates OAuth token
4. Prompt for 2FA code (TOTP)
5. Validate 2FA code
6. Generate JWT + session
7. Proceed to dashboard
```

---

## Database Schema

### Admin Users Table

```sql
CREATE TABLE admin_users (
  id TEXT PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,  -- bcrypt hash
  role TEXT NOT NULL CHECK (role IN ('super_admin', 'admin', 'viewer')),
  created_at TEXT NOT NULL,
  last_login TEXT,
  mfa_enabled INTEGER DEFAULT 0,
  mfa_secret TEXT,
  active INTEGER DEFAULT 1
);

CREATE INDEX idx_admin_users_username ON admin_users(username);
CREATE INDEX idx_admin_users_email ON admin_users(email);
```

### Admin Sessions Table (D1)

```sql
CREATE TABLE admin_sessions (
  session_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  ip_address TEXT NOT NULL,
  user_agent TEXT,
  created_at TEXT NOT NULL,
  expires_at TEXT NOT NULL,
  last_activity TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES admin_users(id)
);

CREATE INDEX idx_admin_sessions_user_id ON admin_sessions(user_id);
CREATE INDEX idx_admin_sessions_expires_at ON admin_sessions(expires_at);
```

### Admin Audit Log

```sql
CREATE TABLE admin_audit_log (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  action TEXT NOT NULL,  -- 'login', 'logout', 'api_key_rotation', 'user_created', etc.
  resource TEXT,         -- What was modified
  details TEXT,          -- JSON details
  ip_address TEXT,
  timestamp TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES admin_users(id)
);

CREATE INDEX idx_admin_audit_log_user_id ON admin_audit_log(user_id);
CREATE INDEX idx_admin_audit_log_timestamp ON admin_audit_log(timestamp);
```

---

## Role-Based Access Control (RBAC)

### Roles

| Role            | Permissions                                                                    |
| --------------- | ------------------------------------------------------------------------------ |
| **super_admin** | Full access: user management, API key rotation, system config, all data access |
| **admin**       | API monitoring, log viewing, limited config changes, no user management        |
| **viewer**      | Read-only access to dashboards, metrics, and logs                              |

### Permission Matrix

| Action               | super_admin | admin      | viewer |
| -------------------- | ----------- | ---------- | ------ |
| View Dashboard       | ✅          | ✅         | ✅     |
| View Metrics         | ✅          | ✅         | ✅     |
| View Logs            | ✅          | ✅         | ✅     |
| Export Logs          | ✅          | ✅         | ❌     |
| Rotate API Keys      | ✅          | ❌         | ❌     |
| Manage Users         | ✅          | ❌         | ❌     |
| Change System Config | ✅          | ⚠️ Limited | ❌     |
| Delete Data          | ✅          | ❌         | ❌     |

---

## Admin API Endpoints

### Authentication

```
POST /admin/auth/login
- Body: { username, password }
- Response: { token, user: { id, username, role }, expiresAt }
- Rate Limited: 5 attempts per 15 minutes per IP

POST /admin/auth/logout
- Headers: Authorization: Bearer <token>
- Response: { success: true }

POST /admin/auth/refresh
- Headers: Authorization: Bearer <token>
- Response: { token, expiresAt }

GET /admin/auth/me
- Headers: Authorization: Bearer <token>
- Response: { id, username, email, role, lastLogin }
```

### User Management (super_admin only)

```
GET /admin/users
- List all admin users
- Response: [{ id, username, email, role, lastLogin, active }]

POST /admin/users
- Create new admin user
- Body: { username, email, password, role }
- Response: { id, username, email, role }

PUT /admin/users/:id
- Update admin user
- Body: { email?, role?, active? }

DELETE /admin/users/:id
- Deactivate admin user (soft delete)
```

### Metrics & Monitoring

```
GET /admin/metrics/overview
- Get system overview metrics
- Response: { requestsLast24h, errorRate, p99Latency, activeUsers }

GET /admin/metrics/requests
- Query: ?from=timestamp&to=timestamp&granularity=1h
- Response: [{ timestamp, count, errorCount, avgLatency }]

GET /admin/metrics/errors
- Get recent errors
- Response: [{ timestamp, path, error, count }]
```

### Log Management

```
GET /admin/logs/requests
- Query: ?limit=100&offset=0&ip=&status=&from=&to=
- Response: { logs: [...], total, hasMore }

GET /admin/logs/auth-failures
- Query: ?limit=100&offset=0&ip=
- Response: { logs: [...], total }

POST /admin/logs/export
- Body: { from, to, format: 'json' | 'csv' }
- Response: Download file or { downloadUrl }
```

### API Key Management (super_admin only)

```
GET /admin/api-keys
- List all API keys (masked)
- Response: [{ id, name, prefix: 'abc123...', createdAt, lastUsed }]

POST /admin/api-keys
- Generate new API key
- Body: { name, expiresAt? }
- Response: { id, key, name, createdAt }  // key shown only once

DELETE /admin/api-keys/:id
- Revoke API key
```

### System Configuration

```
GET /admin/config
- Get current system configuration
- Response: { rateLimits, features, maintenance }

PUT /admin/config/rate-limits
- Body: { requests, window, authFailures }
- Response: { success: true, config }

POST /admin/config/maintenance
- Enable/disable maintenance mode
- Body: { enabled: true, message }
```

---

## Frontend Pages

### 1. Login Page (`/admin/login.html`)

**Features**:

- Clean, minimal design
- Username/password form
- "Remember me" checkbox
- Error messages for invalid credentials
- Rate limit notification
- Link to password reset (future)

**Tech Stack**:

- Vanilla HTML/CSS/JS
- Tailwind CSS for styling
- Fetch API for authentication

### 2. Dashboard (`/admin/dashboard.html`)

**Layout**:

```
┌─────────────────────────────────────────────────────────┐
│  SpiralSafe Admin Console         [@username] [Logout]  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │Requests  │  │Error Rate│  │P99 Latency│ │ Active  ││
│  │  12.5K   │  │  0.03%   │  │   118ms   │ │ Sessions││
│  │ ↑ 23%    │  │ ↓ 12%    │  │ ↓ 5ms     │ │   42    ││
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘│
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │     Request Rate Timeline (24h)                    │ │
│  │     [Line chart showing requests over time]        │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌───────────────────┐  ┌───────────────────────────┐  │
│  │ Recent Errors     │  │  Top Endpoints            │  │
│  │ • 401 /api/wave  │  │  • /api/health (45%)      │  │
│  │ • 429 /api/bump  │  │  • /api/wave (23%)        │  │
│  └───────────────────┘  └───────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**Sections**:

- Metrics cards (requests, errors, latency, active sessions)
- Request rate timeline chart
- Recent errors list
- Top endpoints by usage
- Failed auth attempts map (geographic)

### 3. Logs Explorer (`/admin/logs.html`)

**Features**:

- Searchable log table
- Filters: IP, status code, date range, path
- Export to CSV/JSON
- Real-time updates (WebSocket or polling)
- Pagination

### 4. User Management (`/admin/users.html`)

**Features**:

- List all admin users
- Create new user modal
- Edit user role
- Deactivate user
- View user activity history

### 5. API Keys (`/admin/api-keys.html`)

**Features**:

- List all API keys (masked)
- Generate new key (show once, copy to clipboard)
- Revoke key with confirmation
- View key usage statistics

---

## Security Considerations

### 1. Authentication Security

- ✅ Password hashing with bcrypt (cost factor 12)
- ✅ JWT with short expiration (24h)
- ✅ Session binding to IP (optional, configurable)
- ✅ Rate limiting on login attempts (5 per 15min)
- ✅ Account lockout after 10 failed attempts
- 🚧 2FA/TOTP support (future)
- 🚧 OAuth integration (future)

### 2. Session Security

- ✅ HTTPOnly cookies (prevent XSS)
- ✅ Secure flag (HTTPS only)
- ✅ SameSite=Strict (prevent CSRF)
- ✅ Session expiration tracking
- ✅ Automatic session cleanup (expired sessions removed)

### 3. API Security

- ✅ JWT validation on all admin endpoints
- ✅ Role-based access control
- ✅ Audit logging for all admin actions
- ✅ IP allowlisting (optional, for super_admin)
- ✅ CORS restricted to console.spiralsafe.org

### 4. Data Protection

- ✅ Sensitive data redacted in logs (passwords, API keys)
- ✅ API keys shown only once at creation
- ✅ Password reset tokens expire after 1 hour
- ✅ No API keys stored in plaintext (hashed identifiers)

---

## Implementation Phases

### Phase 1: Basic Auth + Dashboard (Week 1-2)

- [x] Design authentication flow
- [ ] Create D1 tables for admin users and sessions
- [ ] Implement login endpoint with JWT
- [ ] Build login page UI
- [ ] Build dashboard with basic metrics
- [ ] Implement role-based access control

### Phase 2: Logs & Monitoring (Week 3)

- [ ] Build logs explorer UI
- [ ] Implement log querying endpoints
- [ ] Add export functionality
- [ ] Real-time log updates

### Phase 3: User & Key Management (Week 4)

- [ ] Build user management UI
- [ ] Implement user CRUD endpoints
- [ ] Build API key management UI
- [ ] Implement key generation/revocation

### Phase 4: Advanced Features (Week 5-6)

- [ ] 2FA/TOTP support
- [ ] OAuth integration (GitHub, Google)
- [ ] Advanced analytics charts
- [ ] Automated alerting configuration UI

---

## Technology Stack

### Backend

- **Runtime**: Cloudflare Workers (TypeScript)
- **Database**: D1 (SQLite)
- **Session Store**: KV
- **Authentication**: JWT (jose library)
- **Password Hashing**: bcrypt (cloudflare-workers-bcrypt)

### Frontend

- **Framework**: Vanilla JS (or Vue.js for SPA)
- **Styling**: Tailwind CSS
- **Charts**: Chart.js or Apache ECharts
- **State Management**: Local state (or Pinia if Vue)
- **HTTP Client**: Fetch API

### Infrastructure

- **Domain**: console.spiralsafe.org
- **Deployment**: Cloudflare Workers + Pages
- **SSL/TLS**: Cloudflare managed certificate

---

## Environment Variables

```bash
# JWT Configuration
ADMIN_JWT_SECRET=<random-256-bit-secret>
ADMIN_JWT_EXPIRATION=86400  # 24 hours in seconds

# Session Configuration
ADMIN_SESSION_DURATION=86400  # 24 hours
ADMIN_IP_BINDING=true  # Bind sessions to IP

# Security
ADMIN_RATE_LIMIT_LOGIN=5  # Max login attempts
ADMIN_RATE_LIMIT_WINDOW=900  # 15 minutes

# Initial Admin (for setup)
ADMIN_INITIAL_USERNAME=admin
ADMIN_INITIAL_PASSWORD=<secure-password>
ADMIN_INITIAL_EMAIL=admin@spiralsafe.org
```

---

## Deployment Steps

### 1. Create Database Tables

```bash
cd ops
npx wrangler d1 execute spiralsafe-ops --file=schemas/admin-schema.sql
```

### 2. Set Secrets

```bash
# Generate JWT secret
ADMIN_JWT_SECRET=$(openssl rand -hex 32)
npx wrangler secret put ADMIN_JWT_SECRET
# Enter: $ADMIN_JWT_SECRET

# Set initial admin password
npx wrangler secret put ADMIN_INITIAL_PASSWORD
# Enter: <secure-password>
```

### 3. Deploy Admin Worker

```bash
# Build admin worker
npm run build:admin

# Deploy to console.spiralsafe.org
npx wrangler deploy --config wrangler-admin.toml
```

### 4. Create Initial Admin User

```bash
curl -X POST https://console.spiralsafe.org/admin/setup/init \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "<ADMIN_INITIAL_PASSWORD>",
    "email": "admin@spiralsafe.org"
  }'
```

### 5. Login & Change Password

```bash
# Login
curl -X POST https://console.spiralsafe.org/admin/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "<initial-password>"}' \
  | jq -r '.token'

# Change password
curl -X PUT https://console.spiralsafe.org/admin/users/me/password \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"currentPassword": "<initial>", "newPassword": "<new>"}'
```

---

## Monitoring & Maintenance

### Session Cleanup (Scheduled Worker)

```typescript
// Run every hour to clean expired sessions
export default {
  async scheduled(event: ScheduledEvent, env: Env) {
    await env.SPIRALSAFE_DB.prepare(
      "DELETE FROM admin_sessions WHERE expires_at < ?",
    )
      .bind(new Date().toISOString())
      .run();
  },
};
```

### Audit Log Rotation

- Keep last 365 days in D1
- Archive older logs to R2
- Automated monthly archival script

### Security Reviews

- Weekly review of admin audit logs
- Monthly review of user permissions
- Quarterly security assessment
- Annual penetration testing

---

## Future Enhancements

### v2.0 (Q2 2026)

- [ ] 2FA/TOTP authentication
- [ ] OAuth integration (GitHub, Google, NEAR)
- [ ] Advanced analytics dashboards
- [ ] Automated alerting configuration
- [ ] Mobile-responsive admin UI

### v3.0 (Q3 2026)

- [ ] GraphQL API for admin operations
- [ ] Real-time collaboration (multiple admins)
- [ ] Advanced RBAC with custom roles
- [ ] Compliance reports (SOC 2, GDPR)
- [ ] AI-powered anomaly detection

---

**H&&S:WAVE** | From the constraints, gifts. From the spiral, safety.

```
Architecture Version: 1.0.0
Status: DESIGN COMPLETE
Implementation: READY TO START
Security Level: ENTERPRISE GRADE
```

🔐 **Admin Security**: Enterprise-grade authentication and access control for SpiralSafe operations.
