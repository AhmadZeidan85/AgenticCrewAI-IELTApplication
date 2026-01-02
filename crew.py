from crewai import Crew
from tasks.evaluate_writing import evaluate_writing_task

ielts_writing_crew = Crew(
    agents=[evaluate_writing_task.agent],
    tasks=[evaluate_writing_task],
    verbose=True
)

def evaluate_writing(response: str):
    return ielts_writing_crew.kickoff(
        inputs={"response": response}
    )
