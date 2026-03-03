"""
Government API Server - Phase 4D
FastAPI-based REST API for scenario storage, user management, and approval workflows
Designed for government deployment with security, audit logging, and compliance

Run with: uvicorn api_server:app --reload --host 0.0.0.0 --port 8000
Production: gunicorn -w 4 -b 0.0.0.0:8000 api_server:app
"""
import os
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from uuid import uuid4
import logging

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from pydantic import BaseModel, Field
import jwt

from core.api_models import (
    User, UserRole, Scenario, ScenarioStatus, ScenarioConfig, 
    ScenarioResults, AuditLog, ApprovalRequest
)

# Configuration
API_VERSION = "1.0.0"
SECRET_KEY = os.getenv("API_SECRET_KEY", "dev-key-change-in-production")
ALGORITHM = "HS256"
TOKEN_EXPIRY_HOURS = 24

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app setup
app = FastAPI(
    title="S2F-DT Government API",
    description="Decision support toolkit for government energy & agriculture partners",
    version=API_VERSION,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# CORS - restrict to government domains
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8501",  # Streamlit default
    os.getenv("GOVERNMENT_DOMAIN", ""),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o for o in ALLOWED_ORIGINS if o],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# In-memory storage (for demo - use database in production)
# In production, use PostgreSQL or SQLite
users_db: Dict[str, User] = {}
scenarios_db: Dict[str, Scenario] = {}
audit_logs_db: Dict[str, AuditLog] = {}
approval_requests_db: Dict[str, ApprovalRequest] = {}

# ===== AUTHENTICATION =====

def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    if expires_delta is None:
        expires_delta = timedelta(hours=TOKEN_EXPIRY_HOURS)
    
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthCredentials = Depends(security)) -> str:
    """Verify JWT token and return user_id."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ===== PYDANTIC MODELS (API request/response) =====

class LoginRequest(BaseModel):
    """User login request."""
    email: str
    password: str


class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    user_id: str
    expires_in_hours: int = TOKEN_EXPIRY_HOURS


class UserResponse(BaseModel):
    """User response model."""
    user_id: str
    name: str
    email: str
    department: str
    role: str
    is_active: bool
    created_at: str


class ScenarioCreateRequest(BaseModel):
    """Create scenario request."""
    name: str
    description: str
    config: Dict[str, Any]
    notes: str = ""


class ScenarioUpdateRequest(BaseModel):
    """Update scenario request."""
    name: Optional[str] = None
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class ScenarioResponse(BaseModel):
    """Scenario response model."""
    scenario_id: str
    name: str
    description: str
    owner_id: str
    status: str
    config: Dict[str, Any]
    results: Optional[Dict[str, Any]] = None
    created_at: str
    updated_at: str
    is_public: bool


class ApprovalResponse(BaseModel):
    """Approval request response."""
    request_id: str
    scenario_id: str
    status: str
    created_at: str
    approved_at: Optional[str] = None
    approver_comments: str


# ===== HELPER FUNCTIONS =====

def get_current_user(user_id: str = Depends(verify_token)) -> User:
    """Get current authenticated user."""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]


def log_audit(user_id: str, action: str, resource_type: str, 
              resource_id: str, details: Dict[str, Any] = None):
    """Log audit trail (background task)."""
    log_id = str(uuid4())
    audit_log = AuditLog(
        log_id=log_id,
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details or {}
    )
    audit_logs_db[log_id] = audit_log
    logger.info(f"Audit: {action} on {resource_type}/{resource_id} by {user_id}")


# ===== API ENDPOINTS =====

# Health & Info

@app.get("/api/health")
def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": API_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/info")
def api_info() -> Dict[str, Any]:
    """API information endpoint."""
    return {
        "name": "S2F-DT Government API",
        "version": API_VERSION,
        "description": "Decision support for green ammonia production",
        "endpoints": {
            "auth": "/api/auth/...",
            "users": "/api/users/...",
            "scenarios": "/api/scenarios/...",
            "approvals": "/api/approvals/...",
            "audit": "/api/audit/...",
        }
    }


# Authentication

@app.post("/api/auth/login", response_model=TokenResponse)
def login(request: LoginRequest) -> TokenResponse:
    """Authenticate user and return JWT token."""
    # In production: validate against LDAP, OAuth2, or password database
    # For demo: accept any email
    user_id = None
    for uid, user in users_db.items():
        if user.email == request.email:
            user_id = uid
            break
    
    if not user_id:
        # Create test user for demo
        user_id = str(uuid4())
        users_db[user_id] = User(
            user_id=user_id,
            name=request.email.split('@')[0],
            email=request.email,
            department="Demo Department",
            role=UserRole.ANALYST
        )
    
    token = create_access_token(user_id)
    return TokenResponse(
        access_token=token,
        user_id=user_id,
        expires_in_hours=TOKEN_EXPIRY_HOURS
    )


@app.post("/api/auth/logout")
def logout(user_id: str = Depends(verify_token)) -> Dict[str, str]:
    """Logout user (invalidate token server-side in production)."""
    log_audit(user_id, "logout", "user", user_id)
    return {"message": "Logged out successfully"}


# Users

@app.get("/api/users/me", response_model=UserResponse)
def get_current_user_info(user: User = Depends(get_current_user)) -> UserResponse:
    """Get current user info."""
    return UserResponse(
        user_id=user.user_id,
        name=user.name,
        email=user.email,
        department=user.department,
        role=user.role.value,
        is_active=user.is_active,
        created_at=user.created_at.isoformat()
    )


@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: str, current_user: User = Depends(get_current_user)) -> UserResponse:
    """Get user by ID (admins only)."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can view other users")
    
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[user_id]
    return UserResponse(
        user_id=user.user_id,
        name=user.name,
        email=user.email,
        department=user.department,
        role=user.role.value,
        is_active=user.is_active,
        created_at=user.created_at.isoformat()
    )


# Scenarios

@app.post("/api/scenarios", response_model=ScenarioResponse)
def create_scenario(
    request: ScenarioCreateRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
) -> ScenarioResponse:
    """Create new scenario."""
    scenario_id = str(uuid4())
    config = ScenarioConfig(**request.config)
    
    scenario = Scenario(
        scenario_id=scenario_id,
        name=request.name,
        description=request.description,
        owner_id=current_user.user_id,
        status=ScenarioStatus.DRAFT,
        config=config
    )
    
    scenarios_db[scenario_id] = scenario
    background_tasks.add_task(
        log_audit, 
        current_user.user_id, 
        "created",
        "scenario", 
        scenario_id,
        {"name": request.name}
    )
    
    return ScenarioResponse(**scenario.to_dict())


@app.get("/api/scenarios/{scenario_id}", response_model=ScenarioResponse)
def get_scenario(
    scenario_id: str,
    current_user: User = Depends(get_current_user)
) -> ScenarioResponse:
    """Get scenario by ID (owner or shared with)."""
    if scenario_id not in scenarios_db:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    scenario = scenarios_db[scenario_id]
    
    # Check access
    if scenario.owner_id != current_user.user_id and \
       current_user.user_id not in scenario.shared_with and \
       not scenario.is_public:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return ScenarioResponse(**scenario.to_dict())


@app.get("/api/scenarios", response_model=List[ScenarioResponse])
def list_scenarios(current_user: User = Depends(get_current_user)) -> List[ScenarioResponse]:
    """List user's scenarios and shared scenarios."""
    results = []
    for scenario in scenarios_db.values():
        if scenario.owner_id == current_user.user_id or \
           current_user.user_id in scenario.shared_with or \
           scenario.is_public:
            results.append(ScenarioResponse(**scenario.to_dict()))
    
    return results


@app.put("/api/scenarios/{scenario_id}", response_model=ScenarioResponse)
def update_scenario(
    scenario_id: str,
    request: ScenarioUpdateRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
) -> ScenarioResponse:
    """Update scenario (owner only)."""
    if scenario_id not in scenarios_db:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    scenario = scenarios_db[scenario_id]
    
    if scenario.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Only owner can update")
    
    # Update fields
    if request.name:
        scenario.name = request.name
    if request.description:
        scenario.description = request.description
    if request.config:
        scenario.config = ScenarioConfig(**request.config)
    if request.status:
        scenario.status = ScenarioStatus(request.status)
    
    scenario.updated_at = datetime.utcnow()
    scenarios_db[scenario_id] = scenario
    
    background_tasks.add_task(
        log_audit,
        current_user.user_id,
        "updated",
        "scenario",
        scenario_id
    )
    
    return ScenarioResponse(**scenario.to_dict())


@app.post("/api/scenarios/{scenario_id}/submit", response_model=Dict[str, str])
def submit_scenario(
    scenario_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
) -> Dict[str, str]:
    """Submit scenario for approval."""
    if scenario_id not in scenarios_db:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    scenario = scenarios_db[scenario_id]
    
    if scenario.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Only owner can submit")
    
    scenario.status = ScenarioStatus.SUBMITTED
    scenario.submitted_at = datetime.utcnow()
    scenario.submitted_by = current_user.user_id
    scenarios_db[scenario_id] = scenario
    
    background_tasks.add_task(
        log_audit,
        current_user.user_id,
        "submitted",
        "scenario",
        scenario_id
    )
    
    return {"message": "Scenario submitted for approval"}


# Approval Workflow

@app.post("/api/approvals/{scenario_id}", response_model=ApprovalResponse)
def request_approval(
    scenario_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
) -> ApprovalResponse:
    """Create approval request."""
    if current_user.role != UserRole.APPROVER and current_user.role != UserRole.ADMIN:
        # Self-submission by analyst
        pass
    
    request_id = str(uuid4())
    approval = ApprovalRequest(
        request_id=request_id,
        scenario_id=scenario_id,
        requestor_id=current_user.user_id
    )
    
    approval_requests_db[request_id] = approval
    
    background_tasks.add_task(
        log_audit,
        current_user.user_id,
        "requested_approval",
        "scenario",
        scenario_id
    )
    
    return ApprovalResponse(**approval.to_dict())


@app.post("/api/approvals/{request_id}/approve", response_model=Dict[str, str])
def approve_scenario(
    request_id: str,
    comments: str = "",
    background_tasks: BackgroundTasks = None,
    current_user: User = Depends(get_current_user)
) -> Dict[str, str]:
    """Approve scenario (approver only)."""
    if current_user.role not in [UserRole.APPROVER, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Only approvers can approve")
    
    if request_id not in approval_requests_db:
        raise HTTPException(status_code=404, detail="Approval request not found")
    
    approval = approval_requests_db[request_id]
    approval.status = "approved"
    approval.approver_id = current_user.user_id
    approval.approver_comments = comments
    approval.approved_at = datetime.utcnow()
    approval_requests_db[request_id] = approval
    
    # Update scenario status
    if approval.scenario_id in scenarios_db:
        scenario = scenarios_db[approval.scenario_id]
        scenario.status = ScenarioStatus.APPROVED
        scenarios_db[approval.scenario_id] = scenario
    
    if background_tasks:
        background_tasks.add_task(
            log_audit,
            current_user.user_id,
            "approved",
            "scenario",
            approval.scenario_id
        )
    
    return {"message": "Scenario approved"}


# Audit Trail

@app.get("/api/audit")
def get_audit_logs(
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """Get audit logs (admins only)."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can view audit logs")
    
    logs = list(audit_logs_db.values())
    logs.sort(key=lambda x: x.timestamp, reverse=True)
    
    return [log.to_dict() for log in logs[:limit]]


# ===== INITIALIZATION =====

def init_demo_data():
    """Initialize demo data for testing."""
    demo_user_id = str(uuid4())
    users_db[demo_user_id] = User(
        user_id=demo_user_id,
        name="Demo Analyst",
        email="demo@example.gov",
        department="Ministry of Energy",
        role=UserRole.ANALYST
    )
    logger.info(f"Initialized demo user: {demo_user_id}")


# Initialize on startup
@app.on_event("startup")
async def startup_event():
    """Run on app startup."""
    init_demo_data()
    logger.info("S2F-DT Government API started")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on app shutdown."""
    logger.info("S2F-DT Government API shut down")


# ===== HOW TO RUN =====
"""
Development:
    pip install fastapi uvicorn pyjwt
    uvicorn api_server:app --reload

Production:
    pip install gunicorn
    gunicorn -w 4 -b 0.0.0.0:8000 api_server:app

Docker:
    docker run -p 8000:8000 s2f-dt-api

API Documentation:
    http://localhost:8000/api/docs (Swagger UI)
    http://localhost:8000/api/redoc (ReDoc)

Example Usage:
    1. Login: POST /api/auth/login
    2. Create scenario: POST /api/scenarios
    3. Submit for approval: POST /api/scenarios/{id}/submit
    4. Approve: POST /api/approvals/{request_id}/approve
"""
