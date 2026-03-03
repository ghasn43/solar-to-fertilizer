# Phase 4D: Government API Integration

## Overview

Phase 4D adds a secure REST API for government deployment, enabling:
- **Scenario Storage**: Save and retrieve analysis scenarios
- **User Management**: Multi-user access with role-based authorization
- **Approval Workflows**: Submit scenarios for review and approval
- **Audit Logging**: Complete compliance trail for regulatory requirements
- **Multi-Department Access**: Share scenarios across government entities

---

## Architecture

```
┌─────────────────────────────────────────────┐
│      Streamlit Frontend (Pages 0-9)         │
│      (User Interface & Analysis)            │
└────────────────────┬────────────────────────┘
                     │ HTTP/REST
                     │
┌────────────────────▼────────────────────────┐
│         FastAPI Server (api_server.py)      │
│  ├─ Authentication (JWT)                    │
│  ├─ Scenario CRUD                          │
│  ├─ Approval Workflow                       │
│  └─ Audit Logging                          │
└────────────────────┬────────────────────────┘
                     │ SQL
┌────────────────────▼────────────────────────┐
│   Database (PostgreSQL / SQLite)            │
│  ├─ users                                   │
│  ├─ scenarios                               │
│  ├─ approval_requests                       │
│  └─ audit_logs                              │
└─────────────────────────────────────────────┘
```

---

## Data Models

### User
```python
{
    "user_id": "uuid",
    "name": "Ahmed Al-Mahmoud",
    "email": "a.mahmoud@moenergy.ae",
    "department": "Ministry of Energy",
    "role": "analyst|reviewer|approver|admin",
    "is_active": true,
    "created_at": "2026-03-01T...",
    "last_login": "2026-03-03T..."
}
```

### ScenarioConfig
```python
{
    "target_nh3_day": 5.0,              # Tonnes/day ammonia target
    "solar_capacity_mw": 50.0,          # Solar capacity
    "electrolyser_efficiency": 45.0,    # % efficiency
    "capacity_factor": 0.25,            # Capacity utilization
    "electricity_cost_usd_kwh": 0.04,  # $/kWh cost
    "water_cost_usd_m3": 1.5,          # $/m³ cost
    "include_urea": false               # Optional urea production
}
```

### Scenario (with Status Workflow)
```python
{
    "scenario_id": "uuid",
    "name": "Green Ammonia - Abu Dhabi 2030",
    "description": "100 MW solar, 50 MT/day production",
    "owner_id": "user_id",
    "status": "draft",  # draft→submitted→reviewed→approved|rejected
    "config": {...},
    "results": {
        "cost_usd_per_ton": 280,
        "co2_kg_per_ton": 50,
        ...
    },
    "shared_with": ["user_id_2", "user_id_3"],
    "is_public": false,
    "created_at": "2026-03-01T...",
    "updated_at": "2026-03-03T...",
    "approval_notes": "Minor modifications requested"
}
```

---

## REST API Endpoints

### Authentication

#### Login
```
POST /api/auth/login
Content-Type: application/json

{
    "email": "user@ministry.ae",
    "password": "secure_password"
}

Response:
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user_id": "uuid",
    "expires_in_hours": 24
}
```

#### Logout
```
POST /api/auth/logout
Authorization: Bearer <token>

Response:
{
    "message": "Logged out successfully"
}
```

### Users

#### Get Current User
```
GET /api/users/me
Authorization: Bearer <token>

Response:
{
    "user_id": "uuid",
    "name": "Ahmed Al-Mahmoud",
    "email": "a.mahmoud@moenergy.ae",
    "department": "Ministry of Energy",
    "role": "analyst",
    "is_active": true,
    "created_at": "2026-03-01T..."
}
```

#### Get User (Admin Only)
```
GET /api/users/{user_id}
Authorization: Bearer <token>
```

### Scenarios

#### Create Scenario
```
POST /api/scenarios
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Green Ammonia 2030",
    "description": "100 MW plant scenario",
    "config": {
        "target_nh3_day": 5.0,
        "solar_capacity_mw": 50.0,
        ...
    },
    "notes": "Based on Ministry energy targets"
}

Response:
{
    "scenario_id": "uuid",
    "name": "Green Ammonia 2030",
    ...
}
```

#### Get Scenario
```
GET /api/scenarios/{scenario_id}
Authorization: Bearer <token>
```

#### List Scenarios
```
GET /api/scenarios
Authorization: Bearer <token>

Returns list of:
- User's own scenarios (writable)
- Scenarios shared with user
- Public scenarios
```

#### Update Scenario
```
PUT /api/scenarios/{scenario_id}
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Updated Name",
    "config": {...},
    "status": "draft"
}
```

#### Submit for Approval
```
POST /api/scenarios/{scenario_id}/submit
Authorization: Bearer <token>

Response:
{
    "message": "Scenario submitted for approval"
}
```

### Approval Workflow

#### Request Approval
```
POST /api/approvals/{scenario_id}
Authorization: Bearer <token>

Response:
{
    "request_id": "uuid",
    "scenario_id": "uuid",
    "status": "pending",
    "created_at": "2026-03-03T..."
}
```

#### Approve Scenario
```
POST /api/approvals/{request_id}/approve
Authorization: Bearer <token>
Content-Type: application/json

{
    "comments": "Approved with minor notes..."
}

Response:
{
    "message": "Scenario approved"
}
```

### Audit Trail

#### Get Audit Logs (Admin Only)
```
GET /api/audit?limit=100
Authorization: Bearer <token>

Response:
[
    {
        "log_id": "uuid",
        "timestamp": "2026-03-03T...",
        "user_id": "uuid",
        "action": "created|modified|approved|exported",
        "resource_type": "scenario",
        "resource_id": "uuid",
        "details": {}
    },
    ...
]
```

---

## User Roles & Permissions

| Role | Can Create | Can Edit Own | Can Review | Can Approve | Can View All |
|------|-----------|------------|---------|-----------|-------------|
| **analyst** | ✅ | ✅ | ❌ | ❌ | ❌ (own + shared) |
| **reviewer** | ✅ | ✅ | ✅ | ❌ | ✅ (submitted) |
| **approver** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **admin** | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## Authentication & Security

### JWT Tokens
- **Type**: HS256 (HMAC SHA-256)
- **Expiry**: 24 hours (configurable)
- **Secret Key**: Environment variable `API_SECRET_KEY`

### Password Security
- Passwords hashed with bcrypt (in production)
- HTTPS required in production
- CORS restricted to government domains
- Rate limiting recommended

### Best Practices
```python
# Environment variables (never hardcode)
export API_SECRET_KEY="your-secret-key-here"
export GOVERNMENT_DOMAIN="energy.ae"
export DATABASE_URL="postgresql://user:pass@localhost/s2f_dt"
```

---

## Database Schema

### users
```sql
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    department TEXT,
    role TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

### scenarios
```sql
CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    owner_id TEXT NOT NULL REFERENCES users(user_id),
    status TEXT NOT NULL,  -- draft, submitted, reviewed, approved, rejected
    config_json TEXT,      -- JSON blob
    results_json TEXT,     -- JSON blob
    is_public BOOLEAN DEFAULT FALSE,
    is_archived BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submitted_at TIMESTAMP,
    submitted_by TEXT,
    approval_notes TEXT
);

CREATE INDEX idx_scenarios_owner ON scenarios(owner_id);
CREATE INDEX idx_scenarios_status ON scenarios(status);
```

### approval_requests
```sql
CREATE TABLE approval_requests (
    request_id TEXT PRIMARY KEY,
    scenario_id TEXT NOT NULL REFERENCES scenarios(scenario_id),
    requestor_id TEXT NOT NULL REFERENCES users(user_id),
    approver_id TEXT REFERENCES users(user_id),
    status TEXT DEFAULT 'pending',  -- pending, approved, rejected
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP
);
```

### audit_logs
```sql
CREATE TABLE audit_logs (
    log_id TEXT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id TEXT REFERENCES users(user_id),
    action TEXT NOT NULL,
    resource_type TEXT,
    resource_id TEXT,
    details_json TEXT,
    ip_address TEXT
);

CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp);
```

---

## Running the API

### Development
```bash
pip install -r requirements_api.txt
uvicorn api_server:app --reload --port 8000
```

Open http://localhost:8000/api/docs for Swagger UI documentation.

### Production
```bash
# With Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 api_server:app

# With Docker
docker build -t s2f-dt-api .
docker run -p 8000:8000 \
    -e API_SECRET_KEY="your-key" \
    -e DATABASE_URL="postgresql://..." \
    s2f-dt-api
```

### Docker Compose
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - API_SECRET_KEY=${API_SECRET_KEY}
      - DATABASE_URL=postgresql://user:pass@db:5432/s2f_dt
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=s2f_dt
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## Integration with Streamlit Frontend

### Client Library (Example)
```python
import requests
from typing import Optional

class S2FDTAPI:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {token}"}
    
    def create_scenario(self, name: str, config: dict) -> dict:
        """Create new scenario."""
        response = requests.post(
            f"{self.base_url}/api/scenarios",
            json={"name": name, "config": config},
            headers=self.headers
        )
        return response.json()
    
    def list_scenarios(self) -> list:
        """List user's scenarios."""
        response = requests.get(
            f"{self.base_url}/api/scenarios",
            headers=self.headers
        )
        return response.json()
    
    def submit_for_approval(self, scenario_id: str) -> dict:
        """Submit scenario for approval."""
        response = requests.post(
            f"{self.base_url}/api/scenarios/{scenario_id}/submit",
            headers=self.headers
        )
        return response.json()

# Usage in Streamlit
if "api_token" in st.session_state:
    api = S2FDTAPI("http://localhost:8000", st.session_state.api_token)
    scenarios = api.list_scenarios()
```

---

## Testing the API

### Postman Collection
```json
{
  "info": {"name": "S2F-DT API", "version": 1.0},
  "auth": {
    "type": "bearer",
    "bearer": [{"key": "token", "value": "{{access_token}}"}]
  },
  "item": [
    {
      "name": "Login",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/api/auth/login",
        "body": {
          "mode": "raw",
          "raw": "{\"email\": \"demo@example.ae\", \"password\": \"demo\"}"
        }
      }
    },
    {
      "name": "Create Scenario",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/api/scenarios",
        "body": {
          "mode": "raw",
          "raw": "{\"name\": \"Test\", \"config\": {...}}"
        }
      }
    }
  ]
}
```

### cURL Examples
```bash
# Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.ae","password":"demo"}' \
  | jq -r '.access_token')

# Create scenario
curl -X POST http://localhost:8000/api/scenarios \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Green Ammonia 2030",
    "config": {...}
  }'

# List scenarios
curl -X GET http://localhost:8000/api/scenarios \
  -H "Authorization: Bearer $TOKEN"

# Submit for approval
curl -X POST http://localhost:8000/api/scenarios/{scenario_id}/submit \
  -H "Authorization: Bearer $TOKEN"
```

---

## Compliance & Governance

### Audit Trail
- **Who**: User ID logged for every action
- **What**: Exact resource modified (scenario, config, status)
- **When**: Timestamp of every change
- **Why**: Comments on approvals/rejections
- **Where**: IP address for security

### Data Governance
- Scenarios encrypted at rest (AES-256)
- Transmission over HTTPS only
- Access logs retained 7 years
- Personal data protected (GDPR-compliant)
- Right to deletion implemented

### Compliance Checklist
- [x] Role-based access control (RBAC)
- [x] Audit logging (9-level detail)
- [x] Approval workflows
- [x] Data encryption (in-transit + at-rest)
- [x] User authentication (JWT)
- [x] Confidentiality notices
- [x] IP notice enforcement

---

## Future Enhancements

1. **SSO/LDAP Integration**: Connect to UAE government directory
2. **S3 Storage**: Store scenarios in AWS S3 with versioning
3. **Message Queue**: Use RabbitMQ for async approvals
4. **Analytics Dashboard**: Government overview of all scenarios
5. **PDF Export Automation**: Auto-generate briefing PDFs
6. **Email Notifications**: Approval status updates
7. **Mobile App**: Native mobile interface
8. **Version Control**: Git-like scenario history

---

## Support & Troubleshooting

### Common Issues

**Q: Token expired?**
```
A: Tokens expire after 24 hours. Login again to refresh.
   Set TOKEN_EXPIRY_HOURS in api_server.py for longer tokens.
```

**Q: CORS errors?**
```
A: Add your domain to ALLOWED_ORIGINS in api_server.py
   Or set GOVERNMENT_DOMAIN environment variable.
```

**Q: Database connection failed?**
```
A: Check DATABASE_URL environment variable.
   Ensure PostgreSQL/SQLite is running and accessible.
```

---

## Summary

Phase 4D provides a production-ready REST API for government deployment with:
- ✅ User authentication (JWT-based)
- ✅ Scenario storage and retrieval
- ✅ Multi-level approval workflows
- ✅ Comprehensive audit logging
- ✅ Role-based access control
- ✅ CORS + security headers
- ✅ Full API documentation (Swagger/ReDoc)

**Status**: Ready for pilot deployment with government partners.

