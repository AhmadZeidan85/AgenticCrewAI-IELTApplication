import yaml
from crewai import Task
from agents.writing_examiner import writing_examiner

with open("config/tasks.yaml", "r") as f:
    task_cfg = yaml.safe_load(f)["evaluate_writing"]

evaluate_writing_task = Task(
    description=task_cfg["description"],
    agent=writing_examiner
)
