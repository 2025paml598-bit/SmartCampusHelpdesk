import json
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from agents.base import AgentDecision
from data.knowledge_base import KNOWN_FIXES, SERVICE_STATUS, SUPPORT_POLICIES

_CURRENT_TICKET = {}

@tool
def get_ticket_details(ticket_id: str) -> str:
    """Retrieve full metadata, affected user count, and report completeness for the active ticket."""
    return json.dumps(_CURRENT_TICKET, indent=2)

@tool
def search_known_fixes(category: str) -> str:
    """Search the campus IT knowledge base for known fixes and average resolution times by category."""
    fix = KNOWN_FIXES.get(category, {"fix_id": "NONE", "solution": "No documented fix found.", "avg_resolution_mins": 45})
    return json.dumps(fix, indent=2)

@tool
def check_service_status(service_name: str) -> str:
    """Check real-time read-only health telemetry for a campus IT service or building network."""
    status = SERVICE_STATUS.get(service_name, {"status": "UNKNOWN", "active_alerts": 0})
    return json.dumps(status, indent=2)

@tool
def get_support_policy(priority_level: str) -> str:
    """Retrieve official campus IT SLA and escalation policy for P1 - Critical, P2 - High, or P3 - Normal."""
    return json.dumps(SUPPORT_POLICIES, indent=2)

TOOLS = [get_ticket_details, search_known_fixes, check_service_status, get_support_policy]
TOOL_MAP = {t.name: t for t in TOOLS}

class LLMToolAgent:
    def __init__(self, model_name: str = "qwen3"):
        self.name = "6. LLM Agent (Ollama + LangChain)"
        self.arch = f"ReAct Tool-Calling LLM ({model_name})"
        self.model_name = model_name

    def act(self, ticket: dict) -> AgentDecision:
        global _CURRENT_TICKET
        _CURRENT_TICKET = ticket
        tools_called = []

        try:
            from langchain_ollama import ChatOllama

            llm = ChatOllama(model=self.model_name, temperature=0.1)
            llm_with_tools = llm.bind_tools(TOOLS)

            system_prompt = (
                "You are a Smart Campus IT Helpdesk Triage Assistant. You MUST NOT make changes to real accounts or services. "
                "Before making a decision, you MUST call at least two relevant tools (such as get_ticket_details, "
                "check_service_status, search_known_fixes, get_support_policy) to gather evidence. "
                "After receiving tool outputs, respond ONLY with a valid JSON object using these exact keys: "
                '{"priority": "P1 - Critical|P2 - High|P3 - Normal", "action": "...", "assigned_team": "...", "reasoning": "..."}'
            )

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Triage ticket {ticket['ticket_id']}: {ticket['title']} - {ticket['description']}")
            ]

            for _ in range(3):
                response = llm_with_tools.invoke(messages)
                messages.append(response)

                if not getattr(response, "tool_calls", None):
                    break

                for tc in response.tool_calls:
                    t_name = tc["name"]
                    t_args = tc["args"]
                    tools_called.append(f"{t_name}({t_args})")
                    tool_result = TOOL_MAP[t_name].invoke(t_args)
                    messages.append(ToolMessage(content=str(tool_result), tool_call_id=tc["id"]))

            raw_text = response.content.strip()
            if "</think>" in raw_text:
                raw_text = raw_text.split("</think>")[-1].strip()
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_text:
                raw_text = raw_text.split("```")[1].split("```")[0].strip()

            parsed = json.loads(raw_text)
            return AgentDecision(
                agent_name=self.name,
                architecture_type=self.arch,
                priority=parsed.get("priority", "P2 - High"),
                action=parsed.get("action", "Review Ticket"),
                assigned_team=parsed.get("assigned_team", "Tier-2 Support"),
                reasoning=parsed.get("reasoning", raw_text),
                evidence_used=tools_called if tools_called else ["No tools invoked"]
            )

        except Exception as e:
            t1 = get_ticket_details.invoke({"ticket_id": ticket["ticket_id"]})
            t2 = check_service_status.invoke({"service_name": ticket["service_name"]})
            t3 = search_known_fixes.invoke({"category": ticket["category"]})
            tools_called = [
                f"get_ticket_details({ticket['ticket_id']})",
                f"check_service_status({ticket['service_name']})",
                f"search_known_fixes({ticket['category']})"
            ]
            status_obj = json.loads(t2)
            fix_obj = json.loads(t3)

            if ticket["minutes_until_event"] <= 15 and ticket["affected_users"] >= 50:
                prio, act, team = "P1 - Critical", f"Dispatch AV Tech & Apply {fix_obj['fix_id']}", "Field AV Engineering"
            elif ticket["report_completeness"] < 0.5:
                prio, act, team = "P2 - High", f"Correlate {status_obj['status']} & Request Room Details", "Tier-2 Network Ops"
            else:
                prio, act, team = "P3 - Normal", f"Provide {fix_obj['fix_id']} Self-Service Steps", "Tier-1 Helpdesk"

            return AgentDecision(
                agent_name=self.name,
                architecture_type=f"Fallback Simulation (Ollama Error: {type(e).__name__})",
                priority=prio,
                action=act,
                assigned_team=team,
                reasoning=(
                    f"[Ollama Offline Fallback — Ensure `ollama serve` & `ollama pull {self.model_name}` are running]. "
                    f"Grounded in tool outputs: Service status is {status_obj['status']} with {status_obj['active_alerts']} alerts; "
                    f"Known fix {fix_obj['fix_id']} takes ~{fix_obj['avg_resolution_mins']} mins."
                ),
                evidence_used=tools_called
            )
