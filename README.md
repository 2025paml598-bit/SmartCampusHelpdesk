# Smart Campus IT Helpdesk & Ticket Prioritization Assistant

## Overview
This project implements and compares six AI agent architectures on a simulated college IT helpdesk triage task:
1. **Simple Reflex Agent** (Stateless condition-action rules)
2. **Model-Based Reflex Agent** (Internal world-state tracking for partial observability)
3. **Goal-Based Agent** (SLA & operational goal lookahead)
4. **Utility-Based Agent** (Multi-attribute expected utility maximization)
5. **Learning Agent** (Experience-driven threshold adaptation using historical false-alarm and SLA breach rates)
6. **LLM-Based Tool-Calling Agent** (Local Ollama model via LangChain invoking read-only campus IT tools)

> **Safety Constraint:** All tools and agents operate strictly on simulated read-only data (`data/scenarios.py` and `data/knowledge_base.py`). No real campus accounts, devices, or network services are modified.

---

## Setup & Execution Instructions (PyCharm / Terminal)

### 1. Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/) installed locally with `qwen3` (or another tool-capable model) pulled:
  ```bash
  ollama pull qwen3
  ollama serve
  ```

### 2. Install Dependencies
Open the PyCharm Terminal and run:
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit UI
```bash
streamlit run app.py
```

### 4. Run Automated Scenario Tests (CLI)
```bash
python run_tests.py
```

---

## Comparison Table & Why Decisions Differ

| Scenario | Simple Reflex | Model-Based Reflex | Goal-Based | Utility-Based | Learning Agent | LLM Tool Agent |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A: Critical Projector Failure** (120 users, 10m to class) | **P1 - Critical** (Immediate Dispatch) | **P1 - Critical** (Dispatch w/ Spare Hardware) | **P1 - Critical** (Deploy Backup Projector) | **P1 - Critical** (Highest EU = 63.76) | **P1 - Critical** (Learned Fast-Track) | **P1 - Critical** (Grounded in `DEGRADED` status & KB-401) |
| **B: Normal Laptop Software** (1 user, workaround exists) | **P3 - Normal** (Send KB Guide) | **P3 - Normal** (Standard Tier-1) | **P3 - Normal** (Send KB-112) | **P3 - Normal** (Lowest resource cost wins) | **P3 - Normal** (Suppress escalation due to 70% false-alarm history) | **P3 - Normal** (Grounded in `OPERATIONAL` status & KB-112) |
| **C: Ambiguous Wi-Fi Outage** (45 users, 35% clarity) | **P2 - High** (Blindly escalates on user count) | **P2 - High** (Correlates building outage state + warning telemetry) | **P2 - High** (Runs ping sweep before Tier-2 dispatch) | **P2 - High** (Penalizes P1 EU due to 0.35 confidence) | **P2 - High** (Learned caution from 40% Wi-Fi false alarms) | **P2 - High** (Calls `check_service_status`, sees packet loss, requests room numbers) |

### Why Decisions Differ Across Architectures
- **Handling Partial Observability (Scenario C):** The **Simple Reflex Agent** reacts solely to `affected_users = 45` and ignores that the reports are 65% incomplete. In contrast, the **Model-Based Agent** checks internal building state, the **Utility-Based Agent** discounts P1 expected utility by multiplying by `confidence = 0.35`, and the **LLM Agent** inspects `check_service_status()` to confirm high packet loss before requesting missing room numbers.
- **Lookahead vs. Immediate Rules (Scenario A):** While Simple Reflex triggers a generic dispatch, the **Goal-Based Agent** compares the known fix duration (12 mins) against the class countdown (10 mins) and specifically plans to deploy a *backup projector* to guarantee zero lost lecture time.
- **Adaptation Over Time:** Only the **Learning Agent** changes its behavior across runs when post-ticket outcomes (false alarms vs. SLA breaches) are recorded in `data/experience_store.json`.

---

## Limitations Acknowledged
1. **Static Heuristic Weights:** The Utility-Based agent uses hand-tuned weights (`0.45` impact, `0.40` urgency) rather than learned weights.
2. **Simple Frequency Learning:** The Learning Agent updates category-level counters rather than contextual multi-feature reinforcement learning.
3. **LLM Latency & Hardware Dependency:** The local Ollama agent requires local GPU/CPU resources and strict JSON adherence, whereas classical agents execute deterministically in `<1 ms`.
