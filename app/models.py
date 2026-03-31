from typing import Literal, Optional, List, Dict, Any
from pydantic import BaseModel, Field


Category = Literal[
    "billing",
    "shipping",
    "technical",
    "account",
    "security",
    "general"
]

Priority = Literal["low", "medium", "high", "urgent"]

Team = Literal[
    "billing_ops",
    "logistics",
    "tech_support",
    "account_support",
    "security_incident",
    "general_support"
]

ActionType = Literal[
    "classify",
    "set_priority",
    "assign_team",
    "draft_reply",
    "request_info",
    "escalate",
    "resolve"
]


class Ticket(BaseModel):
    ticket_id: str
    customer_tier: Literal["free", "pro", "enterprise"]
    subject: str
    body: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Observation(BaseModel):
    task_id: str
    difficulty: str
    instruction: str
    step_index: int
    max_steps: int
    ticket: Ticket
    current_category: Optional[Category] = None
    current_priority: Optional[Priority] = None
    current_team: Optional[Team] = None
    drafted_reply: Optional[str] = None
    requested_fields: List[str] = Field(default_factory=list)
    escalated: bool = False
    resolved: bool = False
    action_history: List[Dict[str, Any]] = Field(default_factory=list)
    available_actions: List[ActionType] = Field(default_factory=list)


class Action(BaseModel):
    action_type: ActionType
    payload: Dict[str, Any] = Field(default_factory=dict)


class Reward(BaseModel):
    score: float
    components: Dict[str, float] = Field(default_factory=dict)
    message: str = ""


class Info(BaseModel):
    grader_score: Optional[float] = None
    task_complete: bool = False
    mistakes: List[str] = Field(default_factory=list)
    notes: Dict[str, Any] = Field(default_factory=dict)


class EnvironmentState(BaseModel):
    task_id: str
    difficulty: str
    instruction: str
    step_index: int
    max_steps: int
    ticket: Ticket
    current_category: Optional[Category] = None
    current_priority: Optional[Priority] = None
    current_team: Optional[Team] = None
    drafted_reply: Optional[str] = None
    requested_fields: List[str] = Field(default_factory=list)
    escalated: bool = False
    resolved: bool = False
    action_history: List[Dict[str, Any]] = Field(default_factory=list)
    done: bool = False
    cumulative_reward: float = 0.0