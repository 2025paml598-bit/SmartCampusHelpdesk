from agents.base import AgentDecision

class UtilityBasedAgent:
    def __init__(self):
        self.name = "4. Utility-Based Agent"
        self.arch = "Multi-Attribute Utility Function U(s, a)"

    def act(self, ticket: dict) -> AgentDecision:
        impact_score = min(ticket["affected_users"] / 100.0, 1.0)
        urgency_score = 1.0 if ticket["minutes_until_event"] <= 15 else (0.6 if ticket["minutes_until_event"] <= 60 else 0.1)
        confidence = ticket["report_completeness"]
        workaround_discount = 0.25 if ticket["has_workaround"] else 0.0

        raw_severity = (0.45 * impact_score + 0.40 * urgency_score + 0.15 * confidence - workaround_discount) * 100
        raw_severity = max(0.0, min(100.0, raw_severity))

        eu_p1 = (raw_severity * 0.95 * confidence) - 25.0
        eu_p2 = (raw_severity * 0.80) - 10.0
        eu_p3 = ((100 - raw_severity) * 0.70) - 2.0

        utilities = {
            "P1 - Critical": round(eu_p1, 2),
            "P2 - High": round(eu_p2, 2),
            "P3 - Normal": round(eu_p3, 2)
        }
        best_priority = max(utilities, key=utilities.get)

        action_map = {
            "P1 - Critical": ("Dispatch Senior Technician Immediately", "Field Engineering"),
            "P2 - High": ("Targeted Triage & Escalation", "Tier-2 Support"),
            "P3 - Normal": ("Assign Standard Queue + KB Article", "Tier-1 Helpdesk")
        }
        action, team = action_map[best_priority]

        reasoning = (
            f"Computed Severity={raw_severity:.1f}/100 (Impact={impact_score:.2f}, Urgency={urgency_score:.2f}, "
            f"Confidence={confidence:.2f}). Expected Utilities: P1={utilities['P1 - Critical']}, "
            f"P2={utilities['P2 - High']}, P3={utilities['P3 - Normal']}. Selected {best_priority} to maximize EU."
        )

        return AgentDecision(
            agent_name=self.name,
            architecture_type=self.arch,
            priority=best_priority,
            action=action,
            assigned_team=team,
            reasoning=reasoning,
            evidence_used=[f"severity={raw_severity:.1f}", f"utilities={utilities}"],
            metrics=utilities
        )
