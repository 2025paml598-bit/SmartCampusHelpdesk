from agents.base import AgentDecision
from data.knowledge_base import KNOWN_FIXES

class GoalBasedAgent:
    def __init__(self):
        self.name = "3. Goal-Based Agent"
        self.arch = "Explicit Goal Search & Planning"
        self.goals = [
            "G1: Zero lost instructional minutes in active classes",
            "G2: Prevent false-alarm Tier-2 escalations on incomplete data",
            "G3: Resolve single-user issues via self-service when workaround exists"
        ]

    def act(self, ticket: dict) -> AgentDecision:
        kb = KNOWN_FIXES.get(ticket["category"], {"fix_id": "N/A", "avg_resolution_mins": 30})
        can_fix_before_event = kb["avg_resolution_mins"] <= ticket["minutes_until_event"]

        if ticket["reporter_role"] == "Faculty" and ticket["minutes_until_event"] <= 15:
            active_goal = self.goals[0]
            priority = "P1 - Critical"
            if can_fix_before_event:
                action = f"Execute {kb['fix_id']} On-Site Immediately"
            else:
                action = f"Deploy Backup Projector (Est. fix {kb['avg_resolution_mins']}m > {ticket['minutes_until_event']}m window)"
            team = "AV Emergency Dispatch"
            reasoning = (
                f"Selected Goal: [{active_goal}]. Because estimated fix time ({kb['avg_resolution_mins']}m) exceeds "
                f"time-to-lecture ({ticket['minutes_until_event']}m), goal satisfaction requires immediate hardware swap."
            )
        elif ticket["report_completeness"] < 0.5:
            active_goal = self.goals[1]
            priority = "P2 - High"
            action = "Run Automated Ping Sweep & Request Room Info"
            team = "NOC Diagnostic Queue"
            reasoning = (
                f"Selected Goal: [{active_goal}]. Directly escalating incomplete reports ({ticket['report_completeness']:.0%}) "
                f"violates G2; two-step diagnostic verification achieves goal safely."
            )
        else:
            active_goal = self.goals[2]
            priority = "P3 - Normal"
            action = f"Send Self-Service Fix ({kb['fix_id']})"
            team = "Automated / Tier-1 Queue"
            reasoning = (
                f"Selected Goal: [{active_goal}]. Workaround exists ({ticket['has_workaround']}) and {kb['fix_id']} "
                f"satisfies resolution goal without Tier-2 overhead."
            )

        return AgentDecision(
            agent_name=self.name,
            architecture_type=self.arch,
            priority=priority,
            action=action,
            assigned_team=team,
            reasoning=reasoning,
            evidence_used=[f"active_goal='{active_goal}'", f"kb_fix={kb['fix_id']}", f"est_fix_mins={kb['avg_resolution_mins']}"]
        )
