import yaml
from crewai import Agent
from llm import load_mistral_llm

with open("config/agents.yaml", "r") as f:
    agent_cfg = yaml.safe_load(f)["writing_examiner"]

# Force CrewAI to use Mistral LLM explicitly, no LiteLLM fallback
mistral_llm = load_mistral_llm()

writing_examiner = Agent(
    role=agent_cfg["role"],
    goal=agent_cfg["goal"],
    backstory=agent_cfg["backstory"],
    verbose=agent_cfg["verbose"],
    allow_delegation=agent_cfg["allow_delegation"],
    llm=mistral_llm,
    fallback_to_litellm=False  # <-- important
)
