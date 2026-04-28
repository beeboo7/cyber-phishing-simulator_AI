
import ollama
import dotenv 
import os
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

dotenv.load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = ollama.Client(
    host="https://api.ollama.com",
    headers={"Authorization": f"Bearer {os.getenv('API_KEY')}"}
)

class ScenarioChoice(BaseModel):
    id: int
    text: str
    isCorrect: bool
    scenarioId: int

class FeedbackRequest(BaseModel):
    scenario_content: str
    scenario_choices: list[ScenarioChoice] = Field(alias='scenarioChoices')
    selected_choice_id: int = Field(alias='selectedChoiceId')


@app.post("/feedback")
def generate_feedback(body: FeedbackRequest):
    correct_action = next(c.text for c in body.scenario_choices if c.isCorrect)
    learner_answer = next(c.text for c in body.scenario_choices if c.id == body.selected_choice_id)
    scenario_content = body.scenario_content

    response = client.chat(model="gemma3:4b", messages=[
        {"role": "system", "content": (
        "You are a cybersecurity awareness trainer evaluating a learner's response to a phishing simulation. "
        "Be educational, constructive and clear. Never be harsh. "
        "Do not offer follow-up suggestions or ask questions at the end of your response."
        )},
        {"role": "user", "content": (
            "A learner has completed a phishing awareness exercise. Evaluate their response and provide feedback.\n\n"
            f"Scenario shown to learner:\n{scenario_content}"
            f"Correct action they should have taken:\n{correct_action}"
            f"Learner's response:\n{learner_answer}"
            "Provide feedback with the following clearly labeled sections:\n"
            "- Score: (a number from 0 to 100)\n"
            "- Explanation: (2-3 sentences on what they got right or wrong)\n"
            "- Tips: (2-3 bullet points of actionable advice)\n"
            "- Red Flags Missed: (bullet list of warning signs they overlooked)\n\n"
            "Do not provide any additional commentary beyond these sections."
        )} 
    ])

    return {"feedback": response.message.content}