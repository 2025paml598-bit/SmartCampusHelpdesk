from data.scenarios import SCENARIOS
from agents.simple_reflex import SimpleReflexAgent
from agents.model_based_reflex import ModelBasedReflexAgent
from agents.goal_based import GoalBasedAgent
from agents.utility_based import UtilityBasedAgent
from agents.learning_agent import LearningAgent
from agents.llm_agent import LLMToolAgent

def run_all_tests():
    agents = [
        SimpleReflexAgent(),
        ModelBasedReflexAgent(),
        GoalBasedAgent(),
        UtilityBasedAgent(),
        LearningAgent(),
        LLMToolAgent(model_name="qwen3")
    ]

    for scenario_name, ticket in SCENARIOS.items():
        print("=" * 80)
        print(f"TEST SCENARIO: {scenario_name} ({ticket['ticket_id']})")
        print(f"Description: {ticket['description']}")
        print("-" * 80)
        for agent in agents:
            res = agent.act(ticket)
            print(f"[{res.agent_name}] -> Priority: {res.priority} | Action: {res.action}")
            print(f"   Reasoning: {res.reasoning}")
            print(f"   Evidence : {res.evidence_used}\n")

if __name__ == "__main__":
    run_all_tests()
