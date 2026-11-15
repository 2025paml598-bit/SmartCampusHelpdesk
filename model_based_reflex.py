from agents.base import AgentDecision
from data.knowledge_base import SERVICE_STATUS

class ModelBasedReflexAgent:
    def __init__(self):
        self.name = "2. Model-Based Reflex Agent"
        self.arch = "Internal World State + Condition-Action"
        self.internal_state = {
            "active_building_outages": {"Science & Engineering Hall": True},
            "known_flaky_rooms": ["Lecture Hall 302"]
        }

    def act(self, ticket: dict) -> AgentDecision:
        service = SERVICE_STATUS.get(ticket["service_name"], {"status": "UNKNOWN"})
        completeness = ticket["report_completeness"]
        location = ticket["location"]

        building_flag = self.internal_state["active_building_outages"].get(location, False)
        is_flaky_room = location in self.internal_state["known_flaky_rooms"]

        if completeness < 0.50 and (building_flag or "WARNING" in service["status"]):
            priority = "P2 - High"
            action = "Correlate Outage & Request Diagnostics"
            team = "Tier-2 Network Operations"
            reasoning = (
                f"Report completeness is low ({completeness:.0%}), creating partial observability. "
                f"However, internal world state flags an active anomaly in '{location}' and telemetry shows "
                f"'{service['status']}', preventing premature dismissal."
            )
        elif is_flaky_room and ticket["minutes_until_event"] <= 15:
            priority = "P1 - Critical"
            action = "Dispatch AV Tech with Spare Hardware"
            team = "Classroom AV Rapid Response"
            reasoning = (
                f"Internal state notes '{location}' has recurring hardware faults, combined with imminent lecture "
                f"({ticket['minutes_until_event']} mins) and service status '{service['status']}'."
            )
        else:
            priority = "P3 - Normal"
            action = "Standard Tier-1 Triage"
            team = "Tier-1 Helpdesk"
            reasoning = f"Internal world model shows stable service ('{service['status']}') and adequate report clarity ({completeness:.0%})."

        return AgentDecision(
            agent_name=self.name,
            architecture_type=self.arch,
            priority=priority,
            action=action,
            assigned_team=team,
            reasoning=reasoning,
            evidence_used=[
                f"service_status={service['status']}",
                f"report_completeness={completeness}",
                f"internal_building_flag={building_flag}"
            ]
        )
