import streamlit as st
import pandas as pd
from data.scenarios import SCENARIOS
from agents.simple_reflex import SimpleReflexAgent
from agents.model_based_reflex import ModelBasedReflexAgent
from agents.goal_based import GoalBasedAgent
from agents.utility_based import UtilityBasedAgent
from agents.learning_agent import LearningAgent
from agents.llm_agent import LLMToolAgent

st.set_page_config(page_title="Smart Campus IT Helpdesk Agents", layout="wide")

st.title("🎓 Smart Campus IT Helpdesk & Ticket Prioritization Assistant")
st.caption("Comparative Multi-Agent System: Five Classical AI Architectures vs. Local Ollama Tool-Calling LLM")

with st.sidebar:
    st.header("⚙️ Configuration")
    selected_scenario_name = st.selectbox("Select Test Scenario", list(SCENARIOS.keys()))
    ollama_model = st.text_input("Local Ollama Model Name", value="qwen3", help="e.g., qwen3, llama3.2, mistral")
    
    st.divider()
    st.subheader("🧠 Learning Agent Feedback Loop")
    st.write("Simulate post-ticket resolution feedback to update the Learning Agent's experience history:")
    feedback_cat = st.selectbox("Ticket Category", [
        "AV / Classroom Hardware",
        "Software / Licensing",
        "Network / Wi-Fi"
    ])
    feedback_outcome = st.radio("Observed Outcome", [
        "Success (Valid Escalation)",
        "False Alarm (Over-Escalated)",
        "SLA Breach (Under-Escalated)"
    ])
    if st.button("Update Learning Experience"):
        la = LearningAgent()
        la.record_feedback(feedback_cat, feedback_outcome)
        st.success(f"Updated '{feedback_cat}' with: {feedback_outcome}")

ticket = SCENARIOS[selected_scenario_name]

st.subheader(f"📩 Incoming Ticket: {ticket['ticket_id']} — {ticket['title']}")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Category", ticket["category"])
col2.metric("Affected Users", ticket["affected_users"])
col3.metric("Mins to Event", ticket["minutes_until_event"])
col4.metric("Report Clarity", f"{ticket['report_completeness']:.0%}")
col5.metric("Workaround?", "Yes" if ticket["has_workaround"] else "No")

with st.expander("View Raw Scenario JSON Input (Shared Across All 6 Agents)", expanded=False):
    st.json(ticket)

st.divider()

if st.button("🚀 Run All 6 Agents on Selected Scenario", type="primary"):
    with st.spinner("Evaluating ticket across 5 classical agents and querying local Ollama LLM..."):
        agents = [
            SimpleReflexAgent(),
            ModelBasedReflexAgent(),
            GoalBasedAgent(),
            UtilityBasedAgent(),
            LearningAgent(),
            LLMToolAgent(model_name=ollama_model)
        ]
        decisions = [agent.act(ticket) for agent in agents]

    st.subheader("📊 Side-by-Side Agent Comparison Table")
    df = pd.DataFrame([
        {
            "Agent": d.agent_name,
            "Decision Mechanism": d.architecture_type,
            "Priority": d.priority,
            "Recommended Action": d.action,
            "Assigned Queue": d.assigned_team,
            "Evidence / Tools Used": ", ".join(d.evidence_used)
        }
        for d in decisions
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.subheader("🔍 Detailed Agent Reasoning & Architecture Breakdown")
    cols = st.columns(2)
    for idx, d in enumerate(decisions):
        with cols[idx % 2]:
            with st.container(border=True):
                st.markdown(f"### {d.agent_name}")
                st.markdown(f"**Architecture:** `{d.architecture_type}` | **Priority:** `{d.priority}`")
                st.markdown(f"**Action:** {d.action} → *{d.assigned_team}*")
                st.info(f"**Reasoning:** {d.reasoning}")
                st.caption(f"**Evidence / Tool Trace:** {', '.join(d.evidence_used)}")
