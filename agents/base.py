from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class AgentDecision:
    agent_name: str
    architecture_type: str
    priority: str
    action: str
    assigned_team: str
    reasoning: str
    evidence_used: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
