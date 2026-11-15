import json
import os
from agents.base import AgentDecision

STORE_PATH = os.path.join("data", "experience_store.json")

DEFAULT_HISTORY = {
    "AV / Classroom Hardware": {"escalations": 12, "false_alarms": 1, "sla_breaches_when_delayed": 5},
    "Software / Licensing": {"escalations": 20, "false_alarms": 14, "sla_breaches_when_delayed": 0},
    "Network / Wi-Fi": {"escalations": 15, "false_alarms": 6, "sla_breaches_when_delayed": 4}
}

class LearningAgent:
    def __init__(self):
        self.name = "5. Learning Agent"
        self.arch = "Experience-Driven Policy Adaptation"
        self.history = self._load_history()

    def _load_history(self) -> dict:
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(STORE_PATH):
            with open(STORE_PATH, "w") as f:
                json.dump(DEFAULT_HISTORY, f, indent=2)
            return DEFAULT_HISTORY.copy()
        with open(STORE_PATH, "r") as f:
            return json.load(f)

    def _save_history(self):
        with open(STORE_PATH, "w") as f:
            json.dump(self.history, f, indent=2)

    def record_feedback(self, category: str, outcome: str):
        stats = self.history.setdefault(category, {"escalations": 1, "false_alarms": 0, "sla_breaches_when_delayed": 0})
        if outcome == "Success (Valid Escalation)":
            stats["escalations"] += 1
        elif outcome == "False Alarm (Over-Escalated)":
            stats["escalations"] += 1
            stats["false_alarms"] += 1
        elif outcome == "SLA Breach (Under-Escalated)":
            stats["sla_breaches_when_delayed"] += 1
        self._save_history()

    def act(self, ticket: dict) -> AgentDecision:
        cat = ticket["category"]
        stats = self.history.get(cat, {"escalations": 1, "false_alarms": 0, "sla_breaches_when_delayed": 0})
        
        false_alarm_rate = stats["false_alarms"] / max(stats["escalations"], 1)
        breach_risk = stats["sla_breaches_when_delayed"]

        if breach_risk >= 4 and ticket["minutes_until_event"] <= 15:
            priority = "P1 - Critical"
            action = "Learned Fast-Track Escalation"
            team = "Senior Field Response"
            lesson = f"Past delays in '{cat}' caused {breach_risk} SLA breaches; lowered P1 threshold."
        elif false_alarm_rate > 0.50:
            priority = "P3 - Normal"
            action = "Auto-Send Self-Help & Suppress Escalation"
            team = "Tier-1 Automated Queue"
            lesson = f"High historical false-alarm rate ({false_alarm_rate:.0%}) in '{cat}'; learned to avoid Tier-2 escalation."
        elif false_alarm_rate >= 0.30 and ticket["report_completeness"] < 0.50:
            priority = "P2 - High"
            action = "Verify Before Tier-2 Dispatch (Learned Caution)"
            team = "Tier-2 Triage Desk"
            lesson = (
                f"Historical false-alarm rate is {false_alarm_rate:.0%} ({stats['false_alarms']}/{stats['escalations']}) "
                f"for '{cat}'. Combined with incomplete report ({ticket['report_completeness']:.0%}), learned policy "
                f"requires verification before full P1 dispatch."
            )
        else:
            priority = "P2 - High"
            action = "Standard Escalation"
            team = "Tier-2 Support"
            lesson = f"Balanced historical performance (false-alarm rate {false_alarm_rate:.0%})."

        return AgentDecision(
            agent_name=self.name,
            architecture_type=self.arch,
            priority=priority,
            action=action,
            assigned_team=team,
            reasoning=f"Experience Stats for '{cat}': {stats}. Policy Adaptation: {lesson}",
            evidence_used=[f"false_alarm_rate={false_alarm_rate:.2f}", f"sla_breaches={breach_risk}"],
            metrics=stats
        )
