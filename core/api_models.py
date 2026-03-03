"""
Government API Data Models
Database schema for scenario storage, user management, and audit logging
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from dataclasses import dataclass, field, asdict
import json


class UserRole(str, Enum):
    """User roles for government system."""
    ANALYST = "analyst"            # Can create, edit own scenarios
    REVIEWER = "reviewer"          # Can review and comment
    APPROVER = "approver"          # Can approve/reject
    ADMIN = "admin"               # Full system access


class ScenarioStatus(str, Enum):
    """Scenario workflow status."""
    DRAFT = "draft"               # Work in progress
    SUBMITTED = "submitted"       # Ready for review
    REVIEWED = "reviewed"         # Reviewed, awaiting approval
    APPROVED = "approved"         # Officially approved
    REJECTED = "rejected"         # Rejected with feedback
    ARCHIVED = "archived"         # Historical


@dataclass
class User:
    """Government user account."""
    user_id: str                  # UUID
    name: str
    email: str
    department: str               # E.g., "Ministry of Energy"
    role: UserRole
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True
    last_login: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (JSON-serializable)."""
        data = asdict(self)
        data['role'] = self.role.value
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        if self.last_login:
            data['last_login'] = self.last_login.isoformat()
        return data


@dataclass
class ScenarioConfig:
    """Scenario configuration snapshot."""
    target_nh3_day: float
    solar_capacity_mw: float
    electrolyser_efficiency: float
    n2_separation_energy: float
    synthesis_energy: float
    catalyst_factor: float
    capacity_factor: float
    water_cost_usd_m3: float
    electricity_cost_usd_kwh: float
    include_urea: bool
    notes: str = ""               # Description of configuration choices
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create from dictionary."""
        return cls(**data)


@dataclass
class ScenarioResults:
    """Computed results for a scenario."""
    cost_usd_per_ton: float
    co2_kg_per_ton: float
    energy_mwh_day: float
    water_m3_day: float
    annual_production_mt: float
    roi_percentage: Optional[float] = None
    payback_years: Optional[float] = None
    irr_percentage: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class Scenario:
    """Stored scenario with metadata and approval tracking."""
    scenario_id: str               # UUID
    name: str
    description: str
    owner_id: str                  # User ID who created it
    status: ScenarioStatus
    config: ScenarioConfig
    results: Optional[ScenarioResults] = None
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    shared_with: List[str] = field(default_factory=list)  # User IDs
    
    # Approval workflow
    submitted_at: Optional[datetime] = None
    submitted_by: Optional[str] = None         # Approver ID
    approval_notes: str = ""
    
    # Visibility
    is_public: bool = False        # Shared with government
    is_archived: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (JSON-serializable)."""
        data = {
            'scenario_id': self.scenario_id,
            'name': self.name,
            'description': self.description,
            'owner_id': self.owner_id,
            'status': self.status.value,
            'config': self.config.to_dict(),
            'results': self.results.to_dict() if self.results else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'shared_with': self.shared_with,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'submitted_by': self.submitted_by,
            'approval_notes': self.approval_notes,
            'is_public': self.is_public,
            'is_archived': self.is_archived,
        }
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create from dictionary."""
        data['config'] = ScenarioConfig.from_dict(data['config'])
        if data.get('results'):
            data['results'] = ScenarioResults(**data['results'])
        # Convert ISO strings to datetime
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        if data.get('submitted_at'):
            data['submitted_at'] = datetime.fromisoformat(data['submitted_at'])
        data['status'] = ScenarioStatus(data['status'])
        return cls(**data)


@dataclass
class AuditLog:
    """Audit trail for compliance and accountability."""
    log_id: str                    # UUID
    timestamp: datetime = field(default_factory=datetime.utcnow)
    user_id: str = ""
    action: str = ""               # 'created', 'modified', 'approved', 'exported'
    resource_type: str = ""        # 'scenario', 'user', 'report'
    resource_id: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    ip_address: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


@dataclass
class ApprovalRequest:
    """Multi-level approval workflow."""
    request_id: str               # UUID
    scenario_id: str
    requestor_id: str             # Who submitted for approval
    status: str = "pending"       # pending, approved, rejected
    created_at: datetime = field(default_factory=datetime.utcnow)
    approver_comments: str = ""
    approver_id: Optional[str] = None
    approved_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        if self.approved_at:
            data['approved_at'] = self.approved_at.isoformat()
        return data


# Helpers for JSON serialization

def serialize_model(obj: Any) -> Dict[str, Any]:
    """Serialize a model to dictionary (for JSON encoding)."""
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def json_dumps(obj: Any) -> str:
    """Serialize object to JSON string."""
    return json.dumps(obj, default=serialize_model, indent=2)


def json_loads_scenario(data: str) -> Scenario:
    """Deserialize JSON string to Scenario object."""
    return Scenario.from_dict(json.loads(data))


# Database schema documentation
DATABASE_SCHEMA = """
-- Users Table
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    department TEXT,
    role TEXT NOT NULL,  -- analyst, reviewer, approver, admin
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Scenarios Table
CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    owner_id TEXT NOT NULL REFERENCES users(user_id),
    status TEXT NOT NULL,  -- draft, submitted, reviewed, approved, rejected
    config_json TEXT,  -- JSON blob of configuration
    results_json TEXT,  -- JSON blob of results
    is_public BOOLEAN DEFAULT FALSE,
    is_archived BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submitted_at TIMESTAMP,
    submitted_by TEXT,
    approval_notes TEXT
);

-- Scenario Sharing
CREATE TABLE scenario_shares (
    share_id TEXT PRIMARY KEY,
    scenario_id TEXT NOT NULL REFERENCES scenarios(scenario_id),
    shared_with_user_id TEXT NOT NULL REFERENCES users(user_id),
    permission TEXT DEFAULT 'view',  -- view, comment, edit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Approval Requests
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

-- Audit Log
CREATE TABLE audit_logs (
    log_id TEXT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id TEXT REFERENCES users(user_id),
    action TEXT NOT NULL,  -- created, modified, approved, exported, etc
    resource_type TEXT,  -- scenario, user, report, etc
    resource_id TEXT,
    details_json TEXT,  -- JSON blob of additional details
    ip_address TEXT
);

-- Indexes
CREATE INDEX idx_scenarios_owner ON scenarios(owner_id);
CREATE INDEX idx_scenarios_status ON scenarios(status);
CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp);
CREATE INDEX idx_approval_scenario ON approval_requests(scenario_id);
"""
