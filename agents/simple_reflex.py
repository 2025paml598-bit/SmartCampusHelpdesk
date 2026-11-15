from agents.base import AgentDecision

class SimpleReflexAgent:
    def __init__(self):
        self.name = "1. Simple Reflex Agent"
        self.arch = "Condition-Action Rules (Stateless)"

    def act(self, ticket: dict) -> AgentDecision:
        users = ticket["affected_users"]
        mins = ticket["minutes_until_event"]

        if users >= 50 or mins <= 15:
            priority = "P1 - Critical"
            action = "Immediate Dispatch"
            team = "On-Site Field Support"
            rule = "IF affected_users >= 50 OR minutes_until_event <= 15 THEN P1"
        elif users >= 10:
            priority = "P2 - High"
            action = "Escalate to Infrastructure"
            team = "Tier-2 Network/Ops"
            rule = "IF affected_users >= 10 THEN P2"
        else:
            priority = "P3 - Normal"
            action = "Send KB Guide & Queue"
            team = "Tier-1 Student Helpdesk"
            rule = "ELSE P3"

        return AgentDecision(
            agent_name=self.name,
            architecture_type=self.arch,
            priority=priority,
            action=action,
            assigned_team=team,
            reasoning=f"Triggered stateless rule: `{rule}`. Ignores report completeness ({ticket['report_completeness']}) and historical context.",
            evidence_used=[f"affected_users={users}", f"minutes_until_event={mins}"]
        )
